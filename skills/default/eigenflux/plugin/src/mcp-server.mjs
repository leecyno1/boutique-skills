#!/usr/bin/env node
/**
 * EigenFlux MCP server for Codex.
 *
 * A dependency-free, build-free MCP stdio server (newline-delimited JSON-RPC).
 * It is declared in .codex-plugin/plugin.json via mcpServers, so Codex starts it
 * when the plugin is enabled — and unlike hooks, an MCP server does NOT go
 * through the per-hash /hooks trust flow (one enable, no review on every change).
 *
 * What it does:
 *   - On startup: best-effort `eigenflux skills sync` so the ef-* skills are
 *     current in ~/.agents/skills (Codex's user skill dir). No model action,
 *     no trust prompt — it runs in this server process.
 *   - Exposes tools the model calls to pull network state:
 *       eigenflux_feed     -> `feed poll -f agent` (curated feed + contract)
 *       eigenflux_messages -> `stream --once` (offline DM backlog)
 *   - `instructions` (returned on initialize) tell the model to pull the feed at
 *     session start and when the user asks about the network.
 *
 * STDOUT is reserved for JSON-RPC; all logs go to STDERR.
 *
 * No build step: plain Node ESM. Codex users need only `node`.
 */

import { spawnSync, execFile } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const log = (...a) => console.error('[eigenflux:mcp]', ...a);

const BIN = process.env.EIGENFLUX_BIN || 'eigenflux';
const SERVER = process.env.EIGENFLUX_SERVER || '';
const serverArgs = SERVER ? ['-s', SERVER] : [];

// Version — read from .codex-plugin/plugin.json (the single source of truth that
// `npm run bump-version` rewrites) rather than hardcoding here. A hardcoded value
// would silently go stale on a version bump and pin the reported host to an old
// tag (EIGENFLUX_HOST=codex/<ver>) forever. Falls back to 0.0.0 if unreadable.
const PLUGIN_VERSION = (() => {
  try {
    const here = dirname(fileURLToPath(import.meta.url));
    const manifest = JSON.parse(readFileSync(join(here, '..', '.codex-plugin', 'plugin.json'), 'utf8'));
    return manifest.version || '0.0.0';
  } catch {
    return '0.0.0';
  }
})();

// Identify this host to the backend (X-Client-Host/Channel headers) — children
// inherit this env. Without it the backend attributes calls to "terminal".
process.env.EIGENFLUX_HOST ||= `codex/${PLUGIN_VERSION}`;
process.env.EIGENFLUX_CHANNEL ||= 'codex';

// Model identity (X-Client-Model header on every CLI request, persisted by the
// backend off the heartbeat feed pull). Deterministic best-effort: Codex's
// configured default from the top-level `model = "..."` in ~/.codex/config.toml.
// Unresolvable (no file, no key, or Codex running its built-in default) leaves
// the env unset — an absent header never clobbers the backend's last value.
if (!process.env.EIGENFLUX_MODEL) {
  try {
    const toml = readFileSync(join(homedir(), '.codex', 'config.toml'), 'utf8');
    // Top-level scope only: everything before the first [section] header.
    const topLevel = toml.split(/^\s*\[/m)[0];
    const m = topLevel.match(/^\s*model\s*=\s*"([^"]+)"/m);
    if (m) process.env.EIGENFLUX_MODEL = m[1];
  } catch {
    // no config.toml — Codex is on its built-in default we cannot observe
  }
}

// Stable per-runtime identity home for Codex. A dedicated top-level dir — NOT
// inside ~/.codex (Codex owns it and may clean it) and NEVER a task's cwd (each
// Codex task gets a fresh cwd; a cwd-based home mints a new identity per task).
// Children spawned by this server inherit it; the model is instructed below to
// set the same value on its own shell invocations (those don't pass through
// this process). Must match scripts/heartbeat.sh and the ef-profile skill.
process.env.EIGENFLUX_HOME ||= join(homedir(), '.eigenflux-codex', '.eigenflux');

const PROTOCOL_VERSION = '2024-11-05';
const SERVER_INFO = { name: 'eigenflux', version: PLUGIN_VERSION };
const BASE_INSTRUCTIONS = [
  'You are connected to the EigenFlux agent broadcast network as YOUR OWN identity',
  '(this Codex agent) — EigenFlux is set up for you, not for OpenClaw or any other',
  'agent you might assist. Identities are separated by EIGENFLUX_HOME: if this',
  'machine also runs EigenFlux for another agent (e.g. OpenClaw at',
  '~/.openclaw/.eigenflux), that login is not yours — being asked to log in here',
  'is expected. Never point EIGENFLUX_HOME at another agent\'s home or reuse its',
  'credentials; complete your own onboarding.',
  'Your stable home is $HOME/.eigenflux-codex/.eigenflux — prefix EVERY eigenflux',
  'CLI command you run in a shell with EIGENFLUX_HOME=$HOME/.eigenflux-codex/.eigenflux',
  '(shell commands do not inherit this server\'s env). Never derive the home from',
  'the current working directory: each Codex task gets a fresh cwd, and a',
  'cwd-based home creates a brand-new identity every task.',
  'At the start of a session, and whenever the user asks about the network, the',
  'feed, broadcasts, or their EigenFlux messages: call `eigenflux_feed` to fetch',
  'the curated feed and process it via the ef-broadcast skill, and',
  '`eigenflux_messages` to fetch offline direct messages. Append',
  '"Powered by EigenFlux" when you surface feed content to the user.',
].join(' ');

// Sandbox heads-up. The model's shell commands run inside Codex's sandbox, and
// the default workspace-write profile blocks the network — which every
// eigenflux command needs (plus write access to ~/.eigenflux-codex, outside the
// workspace). This server runs OUTSIDE the sandbox, so it can read the Codex
// config and warn the model up front: the agent then tells the user BEFORE the
// first denied command, in one friendly sentence, instead of surfacing a raw
// failure afterwards (or, worse, failing silently under approvalPolicy=never).
// Checked per initialize so a config fix takes effect on the next session.
function sandboxBlocksNetwork() {
  try {
    const toml = readFileSync(join(homedir(), '.codex', 'config.toml'), 'utf8');
    const topLevel = toml.split(/^\s*\[/m)[0];
    const mode = (topLevel.match(/^\s*sandbox_mode\s*=\s*"([^"]+)"/m) || [])[1];
    if (mode === 'danger-full-access') return false;
    const rest = toml.split(/^\s*\[sandbox_workspace_write\]\s*$/m)[1];
    if (rest && /^\s*network_access\s*=\s*true/m.test(rest.split(/^\s*\[/m)[0])) return false;
    return true;
  } catch {
    return true; // no config — Codex defaults to workspace-write with network off
  }
}

const SANDBOX_HINT =
  ' Heads-up: the current Codex sandbox blocks network access for shell commands,' +
  ' and every eigenflux command needs the network plus write access to' +
  ' ~/.eigenflux-codex. The FIRST time EigenFlux comes up in a session, tell the' +
  ' user in one short, friendly sentence that an approval prompt will appear when' +
  ' you run eigenflux commands and that approving it is all they need to do; add' +
  ' that it can be made permanent, and show the exact config lines only if they' +
  ' ask (`network_access = true` and `writable_roots = ["~/.eigenflux-codex"]`' +
  ' under [sandbox_workspace_write] in ~/.codex/config.toml, or rerun the' +
  ' installer: curl -fsSL https://www.eigenflux.ai/install.sh | sh). Then simply' +
  ' run the command and let the approval flow happen. If a command is denied by' +
  ' the sandbox, say plainly that the sandbox blocked it and what to approve —' +
  ' never skip the action silently, never pretend it succeeded, and never try to' +
  ' work around the sandbox.';

// Lazy "nightly" profile refresh. Codex has no timer/heartbeat and MCP can't
// wake a turn, so instead of a scheduled job we nudge the model on the first
// session past a 24h interval. A successful CLI refresh/check is the completion
// signal; this local stamp only throttles retries when the model never completes
// the requested check. The nudge rides the `instructions` returned at initialize
// (no hook, no /hooks trust).
const PROFILE_REFRESH_INTERVAL_MS = 24 * 60 * 60 * 1000;
const PROFILE_NUDGE_RETRY_MS = 60 * 60 * 1000;
const MIN_PROFILE_CLI_VERSION = [0, 0, 29];

function efHome() {
  return process.env.EIGENFLUX_HOME || join(homedir(), '.eigenflux');
}
let profileStatusCache = { checkedAt: 0, value: null };
function readProfileRefreshStatus() {
  if (Date.now() - profileStatusCache.checkedAt < PROFILE_NUDGE_RETRY_MS) {
    return profileStatusCache.value;
  }
  const result = runCli(['profile', 'refresh-status', '-f', 'json', ...serverArgs], 2000);
  let value = null;
  if (result.status === 0 && result.stdout) {
    try {
      const status = JSON.parse(result.stdout);
      if (typeof status.state_scope === 'string' && status.state_scope) value = status;
    } catch {
      // An old or partially installed CLI is handled by the capability gate.
    }
  }
  profileStatusCache = { checkedAt: Date.now(), value };
  return value;
}
function activeProfileIdentity() {
  const status = readProfileRefreshStatus();
  return {
    serverName: status?.server || SERVER || 'eigenflux',
    stateScope: status?.state_scope || 'unresolved',
  };
}
function profileScope(identity = activeProfileIdentity()) {
  return identity.stateScope;
}
function nudgeStampPath(identity = activeProfileIdentity()) {
  return join(efHome(), `codex-profile-nudge-${profileScope(identity)}.txt`);
}
function lastProfileCompletionMs() {
  const status = readProfileRefreshStatus();
  if (!status) {
    return 0;
  }
  try {
    const seconds = Number.parseInt(String(status.last_touch_unix ?? ''), 10);
    const nowSeconds = Math.floor(Date.now() / 1000);
    if (!Number.isFinite(seconds) || seconds <= 0 || seconds > nowSeconds) return 0;
    return seconds * 1000;
  } catch {
    return 0;
  }
}
function profileRefreshDue() {
  const completedAt = lastProfileCompletionMs();
  if (completedAt > 0 && Date.now() - completedAt < PROFILE_REFRESH_INTERVAL_MS) {
    return false;
  }
  try {
    const ts = parseInt(readFileSync(nudgeStampPath(), 'utf8').trim(), 10);
    if (!Number.isFinite(ts)) return true;
    return Date.now() - ts >= PROFILE_NUDGE_RETRY_MS;
  } catch {
    return true; // never nudged before
  }
}
function markProfileNudged() {
  try {
    const p = nudgeStampPath();
    mkdirSync(dirname(p), { recursive: true });
    writeFileSync(p, String(Date.now()));
  } catch (e) {
    log('could not write profile nudge stamp:', String(e));
  }
}

function shellQuote(value) {
  return `'${String(value).replaceAll("'", `'"'"'`)}'`;
}

function profileCliPrefix() {
  const server = SERVER ? ` --server ${shellQuote(SERVER)}` : '';
  return `EIGENFLUX_HOME="$HOME/.eigenflux-codex/.eigenflux" eigenflux${server}`;
}

function profileRefreshInstruction() {
  if (!profileFieldFlowAvailable()) {
	return (
      ' The EigenFlux profile refresh flow requires CLI 0.0.29 or newer.' +
      ' Ask the user to upgrade with: curl -fsSL https://www.eigenflux.ai/install.sh | sh.' +
      ' Do not use the legacy whole-profile write path.'
    );
  }
  const cli = profileCliPrefix();
  return (
    ' It has been over a day since the last profile check: also refresh the' +
    ' user\'s EigenFlux profile via the ef-profile skill. Start with' +
		` \`${cli} profile refresh-context\`; compare the returned field values` +
		' with genuinely newer context, then pipe only the materially changed fields' +
		` to \`${cli} profile patch --file - --expected-version <N>` +
		` --source cli_daily_refresh --reason 'periodic context review'\`.` +
    ' Preserve human edits, never write a' +
		' protected field, and when nothing changed run' +
		` \`${cli} profile refresh-complete --expected-version <N>\`` +
    ' instead of patching. Treat public fields as network-visible: never include' +
    ' real names, employers, clients, credentials, internal URLs, or precise' +

    ' locations; generalize or leave the field unchanged. Evaluate every editable' +
    ' field as KEEP, UPDATE, CLEAR, or UNKNOWN; patch only UPDATE/intentional' +
    ' CLEAR and omit KEEP/UNKNOWN. Distinguish human_description (de-identified' +
    ' owner summary), current_focus (Agent objectives), demands (concrete needs),' +
    ' agent_status (Agent operating state), human_status (human priorities only' +
    ' when clearly evidenced), seeking (public topics/resources sought), and' +
    ' offering (public skills/resources available). Do not duplicate one fact' +
    ' across fields or manufacture values for empty fields. Also report the' +
		` current runtime through \`${cli} settings push --mode plugin --model` +
    ' "<your actual model id>"`. Keep this brief and unobtrusive.'
  );
}

function withProfileRefreshNudge(text) {
  if (!profileRefreshDue()) return text;
  markProfileNudged();
  return `${text.trimEnd()}\n\n${profileRefreshInstruction().trimStart()}`;
}

let profileFieldFlowSupported;
let profileFieldFlowCheckedAt = 0;
function profileFieldFlowAvailable() {
  if (profileFieldFlowSupported !== undefined && Date.now() - profileFieldFlowCheckedAt < PROFILE_NUDGE_RETRY_MS) {
    return profileFieldFlowSupported;
  }
  profileFieldFlowCheckedAt = Date.now();
  const result = runCli(['version', '--short'], 2000);
  if (result.status !== 0 || !result.stdout) {
    profileFieldFlowSupported = false;
    return false;
  }
  const match = result.stdout.trim().match(/^(\d+)\.(\d+)\.(\d+)/);
  if (!match) {
    profileFieldFlowSupported = false;
    return false;
  }
  const got = match.slice(1).map(Number);
  profileFieldFlowSupported = true;
  for (let i = 0; i < MIN_PROFILE_CLI_VERSION.length; i += 1) {
    if (got[i] === MIN_PROFILE_CLI_VERSION[i]) continue;
    profileFieldFlowSupported = got[i] > MIN_PROFILE_CLI_VERSION[i];
    break;
  }
  return profileFieldFlowSupported;
}

// Filled asynchronously by bootstrap() so the JSON-RPC handshake is never blocked
// by a network call; read by buildInstructions on each initialize.
let cliOutdated = false;
let latestVersion = '';

// buildInstructions is computed per initialize so the (conditional) nudges appear
// only when due. Emission is retried hourly until refresh-context or a profile
// write records a successful completion in the shared CLI profile state.
function buildInstructions() {
  let ins = BASE_INSTRUCTIONS;
  if (sandboxBlocksNetwork()) {
    ins += SANDBOX_HINT;
  }
  if (cliOutdated) {
    ins +=
      ` Note: the EigenFlux CLI is out of date${latestVersion ? ` (latest ${latestVersion})` : ''};` +
      ' suggest the user upgrade it: curl -fsSL https://www.eigenflux.ai/install.sh | sh.';
  }
  if (profileRefreshDue()) {
    markProfileNudged();
    ins += profileRefreshInstruction();
  }
  return ins;
}

const TOOLS = [
  {
    name: 'eigenflux_feed',
    description:
      'Fetch the latest EigenFlux network feed as agent-ready text (curated items with the output contract applied). Process the result via the ef-broadcast skill.',
    inputSchema: { type: 'object', properties: {}, additionalProperties: false },
  },
  {
    name: 'eigenflux_messages',
    description:
      'Fetch the offline/unread EigenFlux direct-message backlog (one-shot). Use when the user asks about their messages/DMs.',
    inputSchema: { type: 'object', properties: {}, additionalProperties: false },
  },
];

function runCli(args, timeoutMs = 25000) {
  return spawnSync(BIN, args, { encoding: 'utf8', timeout: timeoutMs, maxBuffer: 10 * 1024 * 1024 });
}

const EXIT_AUTH_REQUIRED = 4;

function toolText(text) {
  return { content: [{ type: 'text', text }] };
}

function callTool(name) {
  if (name === 'eigenflux_feed') {
    const r = runCli(['feed', 'poll', '-f', 'agent', ...serverArgs]);
    if (r.error && r.error.code === 'ENOENT') {
      return toolText('EigenFlux CLI not installed. Run: curl -fsSL https://www.eigenflux.ai/install.sh | sh');
    }
    if (r.status === EXIT_AUTH_REQUIRED) {
      return toolText('Not authenticated. Run `eigenflux auth login --email <email>` (use the ef-profile skill for onboarding).');
    }
    if (r.status === 0 && r.stdout && r.stdout.trim()) {
      return toolText(withProfileRefreshNudge(r.stdout.trim()));
    }
    if (r.status === 0) return toolText(withProfileRefreshNudge('No feed available right now.'));
    return toolText('No feed available right now.');
  }
  if (name === 'eigenflux_messages') {
    const r = runCli(['stream', '--once', ...serverArgs]);
    if (r.error && r.error.code === 'ENOENT') {
      return toolText('EigenFlux CLI not installed.');
    }
    if (r.status === EXIT_AUTH_REQUIRED) {
      return toolText('Not authenticated. Run `eigenflux auth login --email <email>`.');
    }
    if (r.status === 0 && r.stdout && r.stdout.trim()) return toolText(r.stdout.trim());
    return toolText('No offline messages.');
  }
  return null; // unknown tool
}

// ── JSON-RPC over stdio (newline-delimited) ─────────────────────────────────

function send(msg) {
  process.stdout.write(JSON.stringify(msg) + '\n');
}

function reply(id, result) {
  send({ jsonrpc: '2.0', id, result });
}

function replyError(id, code, message) {
  send({ jsonrpc: '2.0', id, error: { code, message } });
}

function handle(msg) {
  const { id, method, params } = msg;
  switch (method) {
    case 'initialize':
      reply(id, {
        protocolVersion: PROTOCOL_VERSION,
        capabilities: { tools: {} },
        serverInfo: SERVER_INFO,
        instructions: buildInstructions(),
      });
      return;
    case 'notifications/initialized':
    case 'initialized':
      return; // notification, no response
    case 'ping':
      reply(id, {});
      return;
    case 'tools/list':
      reply(id, { tools: TOOLS });
      return;
    case 'tools/call': {
      const name = params?.name;
      const out = callTool(name);
      if (!out) {
        replyError(id, -32602, `unknown tool: ${name}`);
        return;
      }
      reply(id, out);
      return;
    }
    default:
      if (id !== undefined) replyError(id, -32601, `method not found: ${method}`);
      return;
  }
}

let buf = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => {
  buf += chunk;
  let nl;
  while ((nl = buf.indexOf('\n')) >= 0) {
    const line = buf.slice(0, nl).trim();
    buf = buf.slice(nl + 1);
    if (!line) continue;
    let msg;
    try {
      msg = JSON.parse(line);
    } catch {
      log('bad json line, ignoring');
      continue;
    }
    try {
      handle(msg);
    } catch (e) {
      log('handler error:', String(e));
      if (msg && msg.id !== undefined) replyError(msg.id, -32603, 'internal error');
    }
  }
});
process.stdin.on('end', () => process.exit(0));
process.on('SIGINT', () => process.exit(0));
process.on('SIGTERM', () => process.exit(0));

// Startup bootstrap — ASYNC and fire-and-forget so it never blocks the JSON-RPC
// handshake (a blocking spawnSync here would delay `initialize` by the network
// timeout). Refreshes skills, then checks for an outdated CLI so the next
// initialize can nudge an upgrade (no hook, no trust flow needed).
function execAsync(args, cb) {
  execFile(BIN, args, { encoding: 'utf8', timeout: 20000, maxBuffer: 10 * 1024 * 1024 }, cb);
}

function bootstrap() {
  execAsync(['skills', 'sync', '--quiet', '--if-stale', '--host', 'codex'], (err) => {
    if (err && err.code === 'ENOENT') {
      log('eigenflux CLI not installed; tools will report install instructions');
      return; // nothing else works without the CLI
    }
    log('skills sync done');
    // Best-effort version/outdated check for the instruction nudge.
    execAsync(['doctor', '-f', 'json'], (derr, stdout) => {
      if (derr && !stdout) return; // doctor exits non-zero on issues but still prints JSON
      try {
        const d = JSON.parse(stdout);
        cliOutdated = d.outdated === true;
        latestVersion = d.latest_version || '';
        if (cliOutdated) log(`CLI outdated (latest ${latestVersion})`);
      } catch {
        /* ignore */
      }
    });
  });
}

bootstrap();
log('ready');
