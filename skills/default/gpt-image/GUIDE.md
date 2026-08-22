# GPT Image 2 生成/编辑使用指南

## 1. 功能定位
- GPT-Image2 文生图、参考图编辑、inpainting 的 Agent runbook：内置 24 类参考图库（Reference Gallery）与 craft 提示词工艺文档，按规范调用打包 CLI 完成生成/编辑。
- 默认档位: 扩展档默认安装
- 仓库目录: `skills/default/gpt-image`
- 安装后目录: `~/.openclaw/skills/gpt-image`

## 2. 使用前准备
- `OPENAI_API_KEY`（大模型厂商 key，属豁免类）
- 可选二进制: `gpt-image` / `uv` / `uvx`（Python 3.11+）

## 3. 配置步骤
1. 导出 `OPENAI_API_KEY`（或写入 `.env`）。
2. 无需安装即用：技能内 `scripts/generate.py` 会自动解析 CLI 路径（本地 src → 已安装 gpt-image → PATH → uvx 兜底）。

## 4. 推荐提问方式
- 用 gpt-image 生成一张 2k 宽幅产品图，提示词用风格库模板。
- 用 gpt-image 对这张参考图做 inpainting，只替换背景。

## 5. 手动验证
```bash
uv run skills/default/gpt-image/scripts/generate.py -p "a red apple on white background" -f /tmp/apple.png
```

## 6. 上游同步
- 上游: https://github.com/wuyoscar/GPT-Image2-Skill （MIT）
- 上游更新 references 或 CLI 后，重新拷贝 `skills/gpt-image` 目录并更新 SOURCE.txt 的 commit 记录。
