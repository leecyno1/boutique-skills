# TROUBLESHOOTING

## ❗ 剪出來的成品「畫面對不上字幕/旁白」(最常見)

**症狀**：跑 `auto_sequence_brolls()` / b-roll 自動排序後，影片裡的畫面跟旁白在講的東西不一致。

**原因**：b-roll 對位靠「字幕內容 ↔ 素材」配對。配對有兩條路：

1. **filename↔caption 對位（預設，零設定）** — 把 b-roll **用內容命名**就會自動對上：
   - ✅ `coffee-pour.mp4`、`studio-homepage.mp4`、`gameplay.mov`、`sunset-beach.mp4`
   - ❌ `IMG_0423.mp4`、`clip01.mp4`、`a3f9c.mp4`（UUID / 流水號 = 無法對位 → 亂填）
2. **keyword_map（進階，自訂主題）** — 傳你自己的主題表：
   ```python
   MY_MAP = {
       "cooking": {
           "caption_keywords": ["recipe", "cook", "ingredient", "煮", "食材"],
           "broll_keywords":   ["kitchen", "pan", "stove", "廚房"],
           "topic_label": "Cooking",
       },
   }
   auto_sequence_brolls(captions, brolls, total_us, keyword_map=MY_MAP)
   ```

> ⚠️ 不要直接拿內建的 `EXAMPLE_KEYWORD_MAP` 當你自己的 —— 那只是一組中性示意主題（product / feature / food…），你的內容不會 match，反而干擾。**留空用 filename 對位，或抄它的結構寫自己的。**

### 輸入合約（input contract — 沒符合就一定對不上）

| 項目 | 要求 |
|---|---|
| **captions** | 每段要有**真實的** `start_us` / `duration_us`（從旁白時間軸來，例如 CapCut 自動字幕產生的）。沒有真時間 = 無時間軸可對齊 |
| **b-roll** | 用**內容命名**（見上）；fps 先 `batch_normalize_broll_folder()`（`from silent_vlog_maker import batch_normalize_broll_folder`）對齊 timeline（預設 30）；去掉背景音 |
| **語言** | filename 對位**語言無關**（中/英/CJK 都可）；keyword_map 才需配語言 |

### 自我診斷

```python
from capcut_helpers import match_brolls_to_captions
m = match_brolls_to_captions(captions, [b["id"] for b in brolls])
for x in m:
    print(f'{x["score"]:.2f}  {x["caption_text"][:30]!r} -> {x["best_broll"]}')
# 多數 score < 0.3 = 沒對上 → 改檔名 或 給 keyword_map
```
跑 `auto_sequence_brolls()` 時若大量片段沒對上，會直接 `RuntimeWarning` 提醒你。

---

## 🚦 Ship-ready QA — 影片 ship 前自檢（v0.3.3, canon M91–M95）

每支影片 export 後、**還沒 call 它「完成」之前**，跑一次：

```python
from capcut_helpers import final_delivery_qa
final_delivery_qa("FINAL.mp4", voice="voice.wav", contact_out="qa_contact.png")
# [OK]/[WARN] 機械驗 M93 頻閃 + M95 死空檔；接觸表逐格用眼睛看 M91/M92/M94/M68
```

這套是從「同一支片被觀眾抓出 8 輪問題」提煉的 —— **每一條都該剪輯的人自己抓，不是讓觀眾抓**：

| # | 檢查 | 怎麼抓 | helper |
|---|---|---|---|
| **M91** chrome/隱私 | 螢幕錄影/截圖洩漏作業系統外框：工作列、檔案管理員側欄（你的磁碟結構！）、瀏覽器分頁、**後台金額頁（financial dashboards）** | 裁到只剩內容區 + 抽幀逐格看 | `contact_sheet` |
| **M92** 圖片排版 | 非滿版圖用了死黑邊 / `zoompan` 抖動 / 整個視窗外框 | 模糊背景填滿 + 靜止 + 裁內容區 | `still_blurfill` |
| **M93** 頻閃 | 頻閃素材（動作遊戲爆擊 / strobe）或亮度落差 | `blackdetect` 抓「黑↔亮」反覆 | `detect_flash` |
| **M94** 真實 artifact | 旁白點名具體東西（時間軸 / 原始素材 / 上一支影片）卻配 generic stock | 給**真實該物**的畫面 | — |
| **M95** 句間死空檔 | 錄音句子之間停 3–4 秒拖節奏 | `silencedetect` 抓 >1.5s；剪到 ~0.5s | `detect_long_pauses` |

**M95 三軌同步剪死空檔**（人聲 / 畫面 / 字幕用同一組 cut）：
```python
from capcut_helpers import (detect_long_pauses, trim_dead_air_ranges,
                            cut_audio_segments, cut_video_segments, remap_time)
cuts = trim_dead_air_ranges(detect_long_pauses("voice.wav"), keep=0.5)
cut_audio_segments("voice.wav", "voice_cut.wav", cuts)     # ⚠️ atrim+concat（aselect 對音訊常不剪）
cut_video_segments("visual.mp4", "visual_cut.mp4", cuts)   # select+setpts
# 字幕：每個 block.start/end = remap_time(t, cuts)
```

---

## 🧭 CapCut version compatibility & Mac

### 版本相容矩陣 — 哪些版本的草稿可以直改 JSON

| 版本 | draft JSON 格式 | 可直改？ | 備註 |
|---|---|---|---|
| **CapCut 國際版 6.x–9.x**（Win） | 明文 JSON | ✅ | 8.9 本機親測明文（`draft_content.json` 開頭 `{"id":...,"version":360000,...}`）。社群工具對 6.2.8 有完整測試 fixture，8.7+/9.x 標「預期相容」（reported by community, verify on your install） |
| **CapCut 國際版 8.7+**（Win） | 明文 JSON | ⚠️ | 可改，但**只改 root 可能被忽略** — 新版以 `template-2.tmp` / `Timelines/` 鏡像優先（本機 8.9 的 `template-2.tmp` 與 `draft_content.json` 位元組數完全相同，佐證鏡像機制）。**一律用 `save_draft_with_sync()`**（本 kit 已內建 M18 全同步） |
| **剪映專業版（CN）≤ 5.9.x** | 明文 JSON | ✅ | 最後的明文版本線；pyJianYingDraft 官方建議鎖 5.9 並擋自動更新 |
| **剪映專業版（CN）6.0+** | AES 加密二進位 | ❌ | 不再以 `{` 開頭、無法 JSON parse；**沒有官方解密/繞過**。`detect_draft_format()` 會回 `encrypted: True`，`load_draft()` 會 raise 帶指引的錯誤 |
| **剪映 7+**（匯出自動化） | — | ❌ | UI 控件隱藏導致匯出自動化失效（reported by community）；≤6.8 匯出自動化仍可用 |

**撞到加密草稿的三條路**（社群公認，無官方繞法）：

1. 剪映釘在 **5.9.x** 並擋自動更新
2. 改用 **CapCut 國際版**（至今 6.x–9.x 未加密、維持明文）
3. 從剪映 6.0+ **匯出專案**可得明文變體

> ❌「關雲端同步可讓草稿保持明文」— 此說法**查無任何來源**，不要依賴。雲端同步已知的風險是 mobile 模板專案 sync 到桌面時可能壞掉，跟加密無關。

**改 JSON 前先跑偵測**：

```python
from capcut_helpers import detect_draft_format
r = detect_draft_format("my-project")   # 專案名 / 草稿資料夾 / JSON 檔路徑都吃
# {'encrypted': False, 'version_hint': 'version=360000, new_version=169.0.0', 'editable': True, ...}
```

### Mac 草稿路徑

| 平台 | 草稿根目錄 |
|---|---|
| Windows CapCut | `C:\Users\<USERNAME>\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\`（本機親測） |
| macOS CapCut | `~/Movies/CapCut/User Data/Projects/com.lveditor.draft/`（Finder「前往資料夾」可達；reported by community, verify on your install） |
| Windows 剪映專業版 | `C:\Users\<USERNAME>\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft\`（reported by community） |
| macOS 剪映專業版 | `~/Movies/JianyingPro/User Data/Projects/com.lveditor.draft/`（reported by community；只有 app 資料夾名不同，`com.lveditor.draft` 層相同） |

**檔名差異**：macOS 版以 `draft_info.json` 為主要時間軸檔、Windows 以 `draft_content.json` 為主 — 兩者 JSON schema 本質相同、互為鏡像（reported by community + 本機 Windows 兩檔並存大小相近可佐證）。`detect_draft_format()` 給資料夾時兩個檔名都會自動找。

**Mac 上用本 kit**：paths 走 env override 即可 —

```bash
export CAPCUT_USER_DATA="$HOME/Movies/CapCut/User Data"
```

### Mac 自動化限制

- 本 kit 的 **GUI 自動化 SOP（capcut-agent-ops）是 Windows-first** — 座標、流程、paywall 地圖都以 Windows CapCut 校準。
- macOS 通用機制是 AppleScript System Events GUI scripting（需逐 app 授權「輔助使用」），但 **CapCut Mac 沒有 AppleScript dictionary**、UI 是自繪非原生 AppKit — Accessibility 樹能暴露多少控件未經驗證。等效於 Windows computer-use 的做法只剩「螢幕截圖 + 座標點擊」層級，沒有優勢，還多 Accessibility / Screen Recording 兩道授權。
- **Mac 建議直接走 programmatic path**：JSON direct edit（Path D，`detect_draft_format()` 先驗明文）+ 純 ffmpeg（Path E）— 完全不碰 GUI。
- Mac ffmpeg 螢幕錄影（avfoundation）：列裝置 `ffmpeg -f avfoundation -list_devices true -i ""`；錄製例 `ffmpeg -f avfoundation -framerate 30 -capture_cursor 1 -i "Capture screen 0:none" out.mp4`。需在系統設定給終端機 **Screen Recording** 權限。
- 字型坑：macOS 15 Sequoia 起 `/System/Library/Fonts/PingFang.ttc` 消失/搬進 private framework，libass/mpv 開字型會報錯 — **不要 hardcode 系統字型路徑**，自帶字型檔（如 Noto Sans TC）配 `fontsdir`。

### 常見流程坑 FAQ（前 5）

1. **改了 JSON，CapCut 一開又變回舊版？**
   M18 7-file sync：CapCut 開專案時優先讀 `Timelines/<UUID>/draft_content.json`（8.7+ 還有 `template-2.tmp` 鏡像），只改 root 會被舊 copy 覆蓋回去。用 `save_draft_with_sync()`（自動同步全部位置）+ `verify_sync()` 驗證。

2. **CapCut 開著時改 JSON 完全沒生效？**
   M20 auto-save trap：CapCut 開著會把 memory state auto-save 寫回、直接蓋掉你的 edit。**先 kill CapCut 再改**：`from capcut_helpers import safe_kill_then_verify`。

3. **B-roll 明明靜音了，export 出來還是漏聲音？**
   M29 四重 lock：只設 `volume=0` 不夠，CapCut export 會 fallback 到 raw video audio。要 material 層 `has_audio=False` + `has_sound_separated=True`，segment 層 `volume=0` + `last_nonzero_volume=0` + `intensifies_audio=False` — 用 `mute_all_video_segments()` 一次做完，export 後用 waveform 圖驗。

4. **想用 JSON patch 套花字/新模板？**
   M41：花字渲染靠 `materials.flowers` 陣列、模板 `template_id` 需雲端下載 — **JSON patch 做不到**，只能 GUI 套。JSON 可改的範圍：文字內容 / 字體 / 字級 / 位置 / 音量。

5. **Windows 路徑反斜線把 JSON 弄壞？**
   M18 backslash trap：JSON 內路徑 `\` 存 2 chars，Python source 要 4 層跳脫；Bash heredoc 處理 `\\` 有 bug — **寫成 .py 檔跑，不要 inline**。

---

## 其他

- **播放速度怪 / 畫面卡格** → 素材 fps 跟 timeline 不符。先 `from silent_vlog_maker import batch_normalize_broll_folder; batch_normalize_broll_folder(folder)`（對齊 30fps + 去音）。
- **匯出後字幕時間軸對不上 player 顯示** → 用 `reencode_player_safe()`（player-friendly profile）。
- **CapCut 自動化沒反應** → 確認 AI 助手的 **Computer Use 有開**（CapCut 沒 API，靠 AI 操作 GUI）。見 README「需求」。
- **`import` 就報錯** → 確認用的是 v0.2.2+（早期版本在淺 checkout 會 IndexError）。
