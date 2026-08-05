# Content Pipeline（模板）— 你的內容類型 + 發布前 checklist

> 複製成 `profiles/content_pipeline.md` 再填。
> 這取代了原作者私有的 `content_routing.py`（綁了個人 pipeline 規則）——
> 你在這裡定義**你自己的**內容類型、預設值、發布前檢查。

## 你做哪些內容類型？（每種定義一組）

### 類型 A：`______`（例：教學長片 / vlog / 開箱 …）
- 平台 / 比例：`______`（YT 16:9 / Shorts 9:16 …）
- 預設 BGM：`______`（你的檔名）
- 字幕風格：`[ ] 基本  [ ] 花字`
- 開頭 hook 模式：`______`
- 結尾：用你的 `profiles/brand.md` outro

### 類型 B：`______`
- （同上）

## 發布前 checklist（通用骨架 — 加你自己的條目）
- [ ] 素材 fps 對齊 timeline（不然播放速度會跑掉）
- [ ] b-roll 已去背景音（只留你要的 BGM/旁白）
- [ ] **畫面跟旁白對得上**（你講什麼就show什麼 — 演示型內容尤其重要）
- [ ] **通用素材占比 < 你的主素材**（產品/實拍是主菜，stock 是調味）
- [ ] 通用素材不重複（同一支 clip 不要一直出現）
- [ ] BGM 短於影片時 → loop 填滿 + 平滑接縫（不要中途靜音）
- [ ] timeline 修剪到旁白真結尾（不要留空白尾巴）
- [ ] 匯出 player-safe（需要的話 libx264 + 無 B-frame）

> 上面這些 checklist 對應 `src/` 裡的 helper（`audit_broll_main_ratio` / `narration_broll_sync_report` /
> `detect_voice_end` / `force_mix_bgm` …）—— 你可以用程式自動驗，不用靠眼睛數。
