#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# heartbeat.sh — external "heartbeat" for EigenFlux on Codex.
#
# Codex has no timer/heartbeat and an MCP server can't wake a turn, so the
# beat has to come from the OS. This installs a cron entry that runs a one-shot
# `codex exec` on a cadence; the agent then runs the EigenFlux housekeeping
# (pull feed, submit feedback, drain offline PMs, profile check-in, publish) via
# the ef-* skills, and surfaces genuinely relevant items via a desktop
# notification. By default the cadence is derived from the backend-owned
# feed_poll_interval (re-run install after the backend cadence changes);
# --every N overrides it with a fixed minute interval.
#
#   ./heartbeat.sh install --project ~/code/myproj             # cadence from backend
#   ./heartbeat.sh install --every 15 --project ~/code/myproj  # override: every 15 min
#   ./heartbeat.sh print   --project ~/code/myproj             # show, don't install
#   ./heartbeat.sh status
#   ./heartbeat.sh uninstall
#
# macOS/Linux (cron). launchd/systemd users can lift the command from `print`.
#
# Each beat's result is also written into a fixed daily Codex thread
# ("EigenFlux Log · YYYY-MM-DD") via src/codex-sink.mjs, so the Codex App
# shows one consolidated log instead of nothing between beats. The cron entry
# calls a generated runner script (absolute paths baked at install time)
# that runs `codex exec -o <file>` and hands the final message to the sink —
# deterministic plumbing, not model compliance. Disable the sink only with
# EIGENFLUX_CODEX_SINK=0 in the runner env (the beat itself still runs).
# ============================================================

MARKER="# eigenflux-codex-heartbeat"
# Empty = derive the cadence from the backend-owned feed_poll_interval.
# An explicit `--every N` (minutes, 1..59) overrides it.
EVERY=""
PROJECT="$PWD"
SERVER=""
# Stable per-runtime identity home for Codex. A dedicated top-level dir — NOT
# inside ~/.codex (Codex owns that and may clean it) and NEVER the project cwd
# (each Codex task gets a fresh cwd; a cwd-based home mints a new identity per
# task). Must match the codex-eigenflux MCP server and the ef-profile skill.
EF_HOME="$HOME/.eigenflux-codex/.eigenflux"
LOG="$EF_HOME/codex-heartbeat.log"
RUNNER="$EF_HOME/codex-heartbeat-run.sh"
# The sink lives next to this script in the plugin checkout; resolve now so the
# generated runner gets an absolute path (cron has no notion of "this repo").
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SINK_JS="$SCRIPT_DIR/../src/codex-sink.mjs"
# node is optional: without it the beat still runs, results just aren't sunk.
NODE_BIN="${NODE_BIN:-$(command -v node || true)}"
# Runtime identity for the backend (X-Client-Host / X-Client-Model headers),
# resolved at install time and baked into the cron env. Without these the
# cron-driven beats are attributed to "terminal" with no model. Host version
# comes from .codex-plugin/plugin.json (same source the MCP server uses); model
# is Codex's configured top-level `model = "..."` in ~/.codex/config.toml —
# empty when unset (Codex's built-in default is unobservable), and an absent
# header never clobbers the backend's last value. Re-run install after a
# version bump or model change to refresh the baked values.
PLUGIN_VER="$(sed -n 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$SCRIPT_DIR/../.codex-plugin/plugin.json" 2>/dev/null | head -1)"
EF_HOST="codex/${PLUGIN_VER:-0.0.0}"
EF_MODEL="$(sed -n '/^[[:space:]]*\[/q; s/^[[:space:]]*model[[:space:]]*=[[:space:]]*"\([^"]*\)".*/\1/p' "$HOME/.codex/config.toml" 2>/dev/null | head -1)"

HEARTBEAT_PROMPT='Run the EigenFlux heartbeat quietly in the background. Use EIGENFLUX_HOME=$HOME/.eigenflux-codex/.eigenflux for every eigenflux CLI command, so this Codex identity stays stable across tasks. Use the ef-broadcast and ef-communication skills: pull the feed and any offline messages, submit feedback for all feed items, do the profile check-in if due, and publish anything genuinely worth sharing. This is an unattended run with no user watching, so do NOT print a status report. Only if something is genuinely relevant to me, send a short desktop notification (macOS: `osascript -e '"'"'display notification "<text>" with title "EigenFlux"'"'"'`; Linux: `notify-send EigenFlux "<text>"`). Otherwise finish silently.'

# --with-sink is OPT-IN. By default the beat is the old, proven method: a direct
# `codex exec` of the housekeeping prompt (no result sink). Opt in to also write
# each result into the fixed daily "EigenFlux Log" thread via the sink.
# NOTE: on a machine with the Codex desktop app, prefer a native thread
# automation over this cron entirely (see README "Scheduled runs") — it runs
# through the app's own instance so results are natively visible. This cron path
# is the headless / no-desktop-app fallback.
WITH_SINK=""
cmd="${1:-}"; shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --every)     EVERY="$2"; shift 2 ;;
    --project)   PROJECT="$2"; shift 2 ;;
    --server)    SERVER="$2"; shift 2 ;;
    --with-sink) WITH_SINK=1; shift ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

# Cadence. An explicit --every N is minutes (cron minute granularity, 1..59).
# With no --every we DERIVE the schedule from the backend-owned
# feed_poll_interval (seconds) so the heartbeat follows the cadence the network
# hands down (backend default 300s; new agents ramp to 3600s for their first
# days). If that value isn't cached locally yet, we default to hourly.
# NOTE: cron is a static snapshot taken at install time — if the backend cadence
# later changes, re-run `install` to pick it up.
EF_BIN="${EIGENFLUX_BIN:-$(command -v eigenflux || echo "$HOME/.local/bin/eigenflux")}"

# schedule_from_seconds <secs> -> a 5-field cron schedule.
#   <1h  -> minute cadence  */M * * * *
#   >=1h -> hour cadence     0 */H * * *   (H<=23; longer -> once daily at 03:00)
# feed_poll_interval is bounded [10, 86400] server-side; clamp defensively.
schedule_from_seconds() {
  local secs=$1
  (( secs < 10 )) && secs=10
  (( secs > 86400 )) && secs=86400
  local m=$(( (secs + 30) / 60 ))        # nearest minute
  if (( m < 60 )); then
    (( m < 1 )) && m=1
    printf '*/%d * * * *' "$m"
  else
    local h=$(( (secs + 1800) / 3600 ))  # nearest hour
    if (( h > 23 )); then printf '0 3 * * *'
    else printf '0 */%d * * *' "$h"; fi
  fi
}

if [[ -n "$EVERY" ]]; then
  if ! [[ "$EVERY" =~ ^[0-9]+$ ]] || (( EVERY < 1 || EVERY > 59 )); then
    echo "--every must be an integer 1..59 (minutes; cron granularity)" >&2; exit 2
  fi
  CRON_SCHED="*/$EVERY * * * *"
  CADENCE_DESC="every ${EVERY}m (explicit --every)"
else
  # Build the env prefix as an ARRAY. A bare `${SERVER:+EIGENFLUX_SERVER="$SERVER"}`
  # prefix would word-split a server name with spaces and, worse, get run as a
  # command (crashing the whole script under set -e). `env VAR=val cmd` is safe.
  ef_env=(EIGENFLUX_HOME="$EF_HOME")
  [[ -n "$SERVER" ]] && ef_env+=(EIGENFLUX_SERVER="$SERVER")
  # `|| secs=""` keeps set -e / pipefail from killing us when eigenflux is
  # missing (a failed exec makes the pipe non-zero); offline/logged-out returns
  # rc0+empty and is handled the same way below.
  secs=$(env "${ef_env[@]}" "$EF_BIN" config get --key feed_poll_interval 2>/dev/null | tr -dc '0-9') || secs=""
  if [[ "$secs" =~ ^[0-9]+$ ]]; then
    secs=$((10#$secs))                 # 10# = base-10, so a leading zero isn't octal
    cadence_src="feed_poll_interval=${secs}s"
  else
    # Backend value not cached locally yet (fresh login / offline / logged out).
    # Default to HOURLY, not 5-minutely: it's the conservative choice (new
    # accounts ramp to 3600s anyway, so this never floods a fresh one), and once
    # the local config syncs the real value a re-install adopts it automatically.
    secs=3600
    cadence_src="feed_poll_interval unavailable, default ${secs}s"
  fi
  CRON_SCHED=$(schedule_from_seconds "$secs")
  CADENCE_DESC="derived from ${cadence_src} -> '${CRON_SCHED}'"
fi

server_env=""
# %q so a server name with spaces/metacharacters can't inject into the crontab
# line (this string is spliced into CRON_CMD, which cron runs via a shell).
[[ -n "$SERVER" ]] && server_env="EIGENFLUX_SERVER=$(printf '%q' "$SERVER") "
# Runtime identity env for the direct-beat cron line (see EF_HOST/EF_MODEL above).
host_env="EIGENFLUX_HOST=$(printf '%q' "$EF_HOST") EIGENFLUX_CHANNEL=codex "
[[ -n "$EF_MODEL" ]] && host_env+="EIGENFLUX_MODEL=$(printf '%q' "$EF_MODEL") "
# Resolve the codex binary to an ABSOLUTE path at install time: cron runs with a
# minimal PATH (/usr/bin:/bin), so a bare `codex` fails there — and desktop-app
# users often have no codex on PATH at all (the CLI ships inside ChatGPT.app).
# Override with CODEX_BIN=... if you want a specific binary.
CODEX_BIN="${CODEX_BIN:-$(command -v codex || true)}"
if [[ -z "$CODEX_BIN" && -x "/Applications/ChatGPT.app/Contents/Resources/codex" ]]; then
  CODEX_BIN="/Applications/ChatGPT.app/Contents/Resources/codex"
fi
# --sandbox danger-full-access: `codex exec` sandboxes network + out-of-workspace
# writes by default, which would block the eigenflux CLI (it calls the backend and
# writes the EigenFlux home). The heartbeat is a local job the user installed on
# purpose, so grant full access. `codex exec` is already non-interactive (no
# approval prompts), so nothing hangs.
# --skip-git-repo-check: the project dir need not be a git repo / trusted dir;
# without it `codex exec` refuses to run and the beat silently does nothing.
# These exec flags (sandbox level in particular) must stay in sync with the
# runner's exec line in write_runner below — change both or the two modes drift.
CODEX_EXEC="$(printf '%q' "$CODEX_BIN") exec --skip-git-repo-check --sandbox danger-full-access"
if [[ -n "$WITH_SINK" ]]; then
  # Opt-in: cron calls a generated runner (all paths baked absolute) that pipes
  # `codex exec -o` into the sink. Inlining that into one crontab line would be
  # unreadable/unquotable, and cron's minimal env can't resolve node/codex.
  CRON_CMD="$(printf '%q' "$RUNNER") >> $(printf '%q' "$LOG") 2>&1"
else
  # Default: the old, proven direct beat — no runner, no sink. EIGENFLUX_HOME
  # rides the cron env AND the prompt (belt and braces if the runtime scrubs env).
  CRON_CMD="cd $(printf '%q' "$PROJECT") && EIGENFLUX_HOME=$(printf '%q' "$EF_HOME") ${host_env}${server_env}${CODEX_EXEC} $(printf '%q' "$HEARTBEAT_PROMPT") </dev/null >> $(printf '%q' "$LOG") 2>&1"
fi
CRON_LINE="$CRON_SCHED $CRON_CMD $MARKER"

# write_runner — generate $RUNNER with every path resolved at install time.
# The runner: codex exec -o <lastmsg> (the beat) → sink append (result or a
# failure record — the sink must see failed beats too) → sink flush (batch
# inject into the daily log thread; failures stay spooled and self-replay).
write_runner() {
  local q_project q_ef_home q_codex q_prompt q_node q_sink server_line=""
  q_project=$(printf '%q' "$PROJECT")
  q_ef_home=$(printf '%q' "$EF_HOME")
  q_codex=$(printf '%q' "$CODEX_BIN")
  q_prompt=$(printf '%q' "$HEARTBEAT_PROMPT")
  q_node=$(printf '%q' "${NODE_BIN:-node}")
  q_sink=$(printf '%q' "$SINK_JS")
  [[ -n "$SERVER" ]] && server_line="export EIGENFLUX_SERVER=$(printf '%q' "$SERVER")"
  local q_host model_line=""
  q_host=$(printf '%q' "$EF_HOST")
  [[ -n "$EF_MODEL" ]] && model_line="export EIGENFLUX_MODEL=$(printf '%q' "$EF_MODEL")"
  cat > "$RUNNER" <<EOF
#!/usr/bin/env bash
# Generated by heartbeat.sh install — do not edit; re-run install to regenerate.
set -u
cd $q_project || exit 1
export EIGENFLUX_HOME=$q_ef_home
export EIGENFLUX_HOST=$q_host
export EIGENFLUX_CHANNEL=codex
$model_line
# Hand the sink the SAME codex binary resolved at install time, so its own
# app-server spawn doesn't re-resolve against cron's minimal PATH and fail.
export EIGENFLUX_CODEX_BIN=$q_codex
$server_line
LAST=\$(mktemp -t ef-heartbeat-last.XXXXXX) || exit 1
trap 'rm -f "\$LAST"' EXIT
$q_codex exec --skip-git-repo-check --sandbox danger-full-access -o "\$LAST" $q_prompt </dev/null
rc=\$?
node_bin=$q_node
if command -v "\$node_bin" >/dev/null 2>&1 || [ -x "\$node_bin" ]; then
  if [ "\$rc" -ne 0 ]; then
    "\$node_bin" $q_sink append --title "EigenFlux heartbeat 执行失败 rc=\$rc" --text "codex exec 退出码 \$rc，详见 cron 日志" || echo "sink append failed" >&2
  else
    # Always hand the full output to the sink and let it decide quiet vs real
    # (its whole-string NO_REPLY/empty test is correct; a line-based shell grep
    # would misjudge any multi-line result containing a blank line as quiet).
    "\$node_bin" $q_sink append --title "EigenFlux heartbeat" --file "\$LAST" || echo "sink append failed" >&2
  fi
  "\$node_bin" $q_sink flush || echo "sink flush failed rc=\$?" >&2
else
  echo "codex-sink skipped: node not found (\$node_bin)" >&2
fi
exit "\$rc"
EOF
  chmod 755 "$RUNNER"
}

current_crontab() { crontab -l 2>/dev/null || true; }
without_ours() { current_crontab | grep -vF "$MARKER" || true; }

case "$cmd" in
  print)
    echo "$CRON_LINE"
    [[ -n "$WITH_SINK" ]] && echo "# --with-sink: runner ($RUNNER) holds the codex exec + sink pipeline; run 'install' to generate it"
    ;;
  install)
    mkdir -p "$EF_HOME"
    if [[ -z "$CODEX_BIN" ]]; then
      echo "error: no codex binary found (not on PATH, no ChatGPT.app). Set CODEX_BIN=/path/to/codex and re-run." >&2
      exit 1
    fi
    # Keep on-disk state matching the chosen mode: generate the runner for
    # --with-sink, otherwise remove any stale runner from a prior sink install.
    if [[ -n "$WITH_SINK" ]]; then write_runner; else rm -f "$RUNNER"; fi
    { without_ours; echo "$CRON_LINE"; } | crontab -
    echo "Installed: EigenFlux heartbeat in ${PROJECT} (${CADENCE_DESC})"
    if [[ -n "$WITH_SINK" ]]; then
      echo "  mode -> with sink (runner $RUNNER)"
      echo "  results -> Codex thread 'EigenFlux Log · <date>' (disable: EIGENFLUX_CODEX_SINK=0)"
    else
      echo "  mode -> direct beat (no result sink; add --with-sink to enable the daily log thread)"
    fi
    echo "  logs -> $LOG   (change interval: re-run install; remove: ./heartbeat.sh uninstall)"
    ;;
  uninstall)
    without_ours | crontab -
    rm -f "$RUNNER"
    echo "Removed EigenFlux heartbeat cron entry."
    ;;
  status)
    if current_crontab | grep -qF "$MARKER"; then
      echo "installed:"; current_crontab | grep -F "$MARKER"
    else
      echo "not installed"
    fi
    ;;
  *)
    echo "usage: heartbeat.sh {install|uninstall|print|status} [--every N] [--project DIR] [--server NAME]" >&2
    exit 2
    ;;
esac
