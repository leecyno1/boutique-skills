---
name: social-auto-upload-bridge
description: Use when Dasheng Publish needs a bridge to the external social-auto-upload project for video upload packages across Bilibili, Xiaohongshu, Douyin, Kuaishou, WeChat Channels, Baijiahao, TikTok, or YouTube.
---

# Social Auto Upload Bridge

## Role

Use external `social-auto-upload` as a multi-platform video uploader bridge. It is an external dependency, not vendored and not version-locked.

Default root:

```bash
${SOCIAL_AUTO_UPLOAD_ROOT:-/Volumes/PSSD/social-auto-upload}
```

## When To Use

- Publish has a completed video `channel_pack.json`.
- The target platform is B站、小红书、抖音、快手、视频号、百家号、TikTok, or YouTube.
- A platform-specific Dasheng skill is missing or failed and `fallback_export` is acceptable.

## Inputs

- `channel_pack.json`
- Final MP4 path
- Title, description, tags, cover if available
- Platform account/session already configured in the external project

## Workflow

1. Check upstream registry:
   ```bash
   python3 scripts/check_publish_upstreams.py --name social-auto-upload
   ```
2. Check local external repo exists and is healthy.
3. Convert `channel_pack.json` into the external project's expected upload config.
   ```bash
   python3 scripts/build_video_upload_package.py --channel-pack <channel_pack.json>
   ```
4. Run preview/dry-run when supported.
5. Run upload only after explicit user confirmation.
6. Write results back under `产物/07_发布执行/<run_id>/channel_packs/...`.

## Hard Rules

1. Never copy generated videos or credentials into `skills/`.
2. Never vendor `social-auto-upload` into this repo.
3. Never click or execute final publish without explicit current-session confirmation unless the target channel pack says `auto_confirm: true`.
4. If login, CAPTCHA, cookie, or upload permission fails, export a manual package and mark the execution `fallback_export`.
5. Always run Publish Guard or platform-specific verification before reporting success.

## Upstream

Tracked in:

```bash
configs/publish/upstream_repos.json
```
