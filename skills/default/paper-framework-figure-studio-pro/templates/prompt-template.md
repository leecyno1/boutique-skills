# Prompt Template v3.2.15c

## S0 prompt

请使用 paper-framework-figure-studio-pro skill，进入并只执行 S0-PAPER-FOUNDATION。

本轮纯文字：只执行文字、state、manifest、brief、audit、guidance 或 checkpoint 写入；不要生成任何图片。

## S0-to-S1 non-copyable first-round surface-style note

S0 must show the following as prose outside the copyable S1 prompt block. Do not insert it into the suggested S1 prompt:

非复制表面风格提示：第一轮 S2 默认表面风格为正式出版风格；这只约束渲染表面，不等同于候选图的叙事、布局或处理方案。若要修改，请在下一轮 S1 请求中另行明确写入表面风格选择或取消默认表面风格；请不要把本说明复制进默认提示词块。可写例如“第一轮采用 ACM/IEEE/AAAI 双栏论文 line-art schematic 表面风格”，也可以写“取消默认表面风格，请 S1 根据论文实际需要自行设置表面风格”。可选表面风格包括：正式出版风格、低保真草图、白板线框、干净扁平极简线稿、正式 schematic 布局草案、轻量蓝图精密稿、轻量科学插画、轻量界面隐喻、轻量等距结构、轻量信息图板、手绘故事板、ACM/IEEE/AAAI 双栏论文 line-art schematic。

## S1 prompt

请使用 paper-framework-figure-studio-pro skill，根据当前状态和 S0 产物，进入并只执行 S1-FIGURE-STRATEGY。S1 必须内置完成原 S1-embedded S2 preparation 的职责，生成 S2 prompt-index 和候选 prompt packages；必须对每个生图 prompt 做严格契约审核与最多 3 次修复循环，检查所有箭头/连线的论文证据、连接线去重/合并、变量在线上/port/tag 表达、模块化不碎片化、内部示意图简洁通用、workflow 不重复、背景只占小部分；不要生成图片。

本轮纯文字：只执行文字、state、manifest、brief、audit、guidance 或 checkpoint 写入；不要生成任何图片。

## S2 prompt

请使用 paper-framework-figure-studio-pro skill，根据当前状态和 S1 已登记产物，进入并只执行 S2-SKETCH-EXPLORE 的 IMAGE_GENERATE。读取 S1 生成的 S2 prompt-index，逐一读取每个 candidate 的 prompt_path，并按同一行 candidate_id 生成/登记对应 target_image_path；candidate_id、prompt_path、target_image_path、状态文件、artifact 和 checkpoint 必须一致。只生成图像，不写审计、排名、解释、修复、聚合或下一步文本。

## S1-to-S2 non-copyable first-round surface-style options note

S1 must show the following as prose outside the copyable S2 prompt block. Do not insert it into the suggested S2 prompt:

非复制表面风格提示：第一轮 S2 默认表面风格为正式出版风格，除非 S1 已在 prompt-index 中记录了显式覆盖或取消默认表面风格；S2 只会按该记录生成图片。若想在运行 S2 前修改第一轮表面风格，需要回到 S1 重做 prompt packages，而不是改 S2 生图提示词。可选表面风格包括：正式出版风格、低保真草图、白板线框、干净扁平极简线稿、正式 schematic 布局草案、轻量蓝图精密稿、轻量科学插画、轻量界面隐喻、轻量等距结构、轻量信息图板、手绘故事板、ACM/IEEE/AAAI 双栏论文 line-art schematic。可在重新执行 S1 时另行写入例如“第一轮采用 轻量蓝图精密稿 表面风格”或“取消默认表面风格，请 S1 根据论文实际需要自行设置表面风格”。

## S3 prompt

请使用 paper-framework-figure-studio-pro skill，根据当前状态、S0/S1 产物和 S2 已生成图像，进入并只执行 S3-DIRECTION-SELECT。S3 必须先内置完成原 S3 review of S2 outputs 和 aggregate 的职责，再做方向选择；用户可在本提示中指定倾向的一个或多个第一轮候选图 ID 作为参考信号，但 S3 仍需基于论文证据和契约审核选择方向；S3 必须把第二轮可选表面风格说明放在 S4 复制提示词之外；不要生成图片。

本轮纯文字：只执行文字、state、manifest、brief、audit、guidance 或 checkpoint 写入；不要生成任何图片。

## S3-to-S4 non-copyable second-round surface-style note

S3 must show the following as prose outside the copyable S4 prompt block. Do not insert it into the suggested S4 prompt:

可选第二轮表面风格：S5 正式候选默认由 S4 根据论文需要设置表面风格；表面风格只约束渲染层，不改变候选图的论文语义、布局骨架、连线证据和密度预算。若希望指定第二轮表面风格，请在下一轮 S4 请求中另行写入“第二轮采用 <表面风格名> 表面风格”。可选项包括：正式出版风格、干净扁平极简线稿、轻量蓝图精密稿、轻量科学插画、轻量界面隐喻、轻量等距结构、轻量信息图板、ACM/IEEE/AAAI 双栏论文 line-art schematic。也可以写“取消默认表面风格，请 S4 根据论文实际需要自行设置 S5 表面风格”。低保真草图、白板线框、手绘故事板默认只适合第一轮探索；若要用于第二轮，必须在 S4 请求中明确说明它仍需保持 formal candidate 可读性。

## S4 prompt

请使用 paper-framework-figure-studio-pro skill，根据当前状态和 S3 方向选择结果，进入并只执行 S4-CANDIDATE-BRIEF。S4 必须内置完成原 S4-embedded S5 preparation 的职责，生成 S5 prompt-index 和 formal candidate prompt packages；必须对每个生图 prompt 做严格契约审核与最多 3 次修复循环，检查所有箭头/连线的论文证据、连接线去重/合并、变量在线上/port/tag 表达、模块化不碎片化、内部示意图简洁通用、workflow 不重复、背景只占小部分；不要生成图片。

本轮纯文字：只执行文字、state、manifest、brief、audit、guidance 或 checkpoint 写入；不要生成任何图片。

## S4-to-S5 surface-style reminder rule

S4 must not show a second-round surface-style reminder beside or inside the copyable S5 prompt. After S4, the next public prompt is S5 image-only.

## S5 prompt

请使用 paper-framework-figure-studio-pro skill，根据当前状态和 S4 已登记产物，进入并只执行 S5-CANDIDATE-IMAGE 的 IMAGE_GENERATE。读取 S4 生成的 S5 prompt-index，逐一读取每个 candidate 的 prompt_path，并按同一行 candidate_id 生成/登记对应 target_image_path；candidate_id、prompt_path、target_image_path、状态文件、artifact 和 checkpoint 必须一致，不要把 F01-F06 或 prompt-index 中的其他 ID 改写成 C01-C06 或数字序号。只生成图像，不写审计、排名、解释、修复、聚合、最终 caption 或下一步文本。S5 生图后 assistant workflow 结束。

## Terminal answer

```text
我的任务已经完成，剩下由人类来决策。
```
