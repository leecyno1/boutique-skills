# codex-responses-tooling 使用指南

## 1. 功能定位
- 高级版默认生图技能，用于通过本机 Codex Responses API 配置发起流式工具调用。
- 典型场景是生成图片：读取本机 Codex 配置中的 `base_url`，调用 Responses 的 `image_generation` 工具，并把返回的 base64 图片结果保存为文件。
- 仓库目录：`skills/default/codex-responses-tooling`
- 安装后目录：`~/.openclaw/skills/codex-responses-tooling`

## 2. 使用前准备
- 需要目标环境已完成 Codex/OpenAI 兼容访问配置。
- 技能会优先读取 `~/.codex/config.toml` 中 `[model_providers.OpenAI].base_url`。
- 需要本机存在有效 Codex 认证信息；不要在对话、日志或截图中暴露 token。

## 3. 推荐使用方式
- 请使用高级版默认生图技能生成一张产品宣传图，比例 16:9，风格科技感。
- 请用 Codex Responses 生图工具生成一张公众号封面，保留标题留白。
- 请生成一张红蓝配色的 OpenClaw/Hermes 技术架构图，输出图片文件路径。

## 4. 工作流程
1. 读取本机 Codex 配置和认证信息。
2. 使用配置里的 OpenAI 兼容 `base_url` 拼接 `POST {base_url}/responses`。
3. 以 SSE 流式方式读取 Responses 输出。
4. 监听 `image_generation_call` 的最终结果。
5. 将 base64 图片内容解码并保存为 `.png` 或 `.jpg`。

## 5. 注意事项
- 不要硬编码网关地址，必须优先使用本机配置。
- 不要打印、记录或返回认证 token。
- 不要依赖最终 JSON body 读取图片，图片结果来自流式事件中的工具调用结果。
- 如果当前环境没有 Codex 认证或 Responses 生图权限，应明确提示用户先完成模型/API 配置。

## 6. 手动验证
```bash
ls -la ~/.openclaw/skills/codex-responses-tooling
```

## 7. 参考资料
- 本技能说明：`SKILL.md`
- 本仓库来源：https://github.com/leecyno1/boutique-skills/tree/main/skills/default/codex-responses-tooling
