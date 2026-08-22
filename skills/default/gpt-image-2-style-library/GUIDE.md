# GPT-Image2 Style Library 使用指南

## 1. 功能定位
- 将用户的图像生成意图转化为生产级 GPT-Image2 提示词：模板类目、视觉风格标签、场景标签、避坑要点与示例案例逆向工程（470+ 案例、20+ 工业级模板）。
- 纯提示词工程技能，不调用任何 API，零密钥要求。
- 默认档位: 扩展档默认安装
- 仓库目录: `skills/default/gpt-image-2-style-library`
- 安装后目录: `~/.openclaw/skills/gpt-image-2-style-library`

## 2. 使用前准备
- 无需任何 API key。生成结果为可直接复制的提示词，可交给任意图像模型（gpt-image、gemini-image-service 等）执行。

## 3. 配置步骤
- 无配置。直接向 Agent 提需求即可。

## 4. 推荐提问方式
- 用 gpt-image-2-style-library 为产品海报写一个 GPT-Image2 提示词。
- 帮我把这段绘图需求改成工业级模板提示词，并给出 2-3 个风格选项。

## 5. 手动验证
```bash
head -40 skills/default/gpt-image-2-style-library/references/style-library.md
```

## 6. 上游同步
- 上游: https://github.com/freestylefly/awesome-gpt-image-2 （MIT）
- 上游更新模板后运行其 `npm run generate:style-skill` 重新生成 references，再同步本目录。
