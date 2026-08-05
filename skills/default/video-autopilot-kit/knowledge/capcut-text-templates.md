# CapCut Text Templates Catalog

> 來自 video-autopilot-kit 開源知識庫 · MIT 授權

> Agent 跑過 + 創作者 review 過的模板評價與心法。Spawn agent 套模板時 reference 這份避免再踩雷。
> 訂閱 CapCut Pro 後，旅行 / 標題 / 標記 / 復古 / 大熱 / 影音部落格分類**全模板可用**（免費版僅部分解鎖）。

## ⚠️ 關鍵概念區分（agent 實測真相）

| 類型 | 中文名 | 套用方式 | 適用 |
|---|---|---|---|
| **花字效果** (text-flower / text-effect) | 文字花字 | **可套到既有 text segment** | 重塑既有 caption 的 style |
| **文字模板** (text-template / 文字範本) | 文字範本 | **必須 ADD 為新 timeline object** — 無法套到既有 segment | 全新做 timeline |

**含意**：
- 已有一批 captions + 要換 style → 用「**花字**」(content.styles[].effectStyle)
- 全新 build → 用「**文字模板**」(text_templates material)
- agent 想套「文字範本」到既有 segment 會卡死，因為**功能 fundamental 不支援**

### 花字效果埋的位置（深 JSON 結構）

```json
"materials": {
  "texts": [{
    "content": "{\"text\":\"DAY 1\",\"styles\":[{
       \"effectStyle\":{
         \"id\":\"<effect-id>\",
         \"path\":\"<...>/Cache/effect/<effect-id>/.../\"
       },
       \"fill\":{
         \"content\":{
           \"render_type\":\"texture\",  ← splash 類用 texture
           \"texture\":{\"path\":\".../splash.png\"}
         }
       }
    }]}"
  }],
  "effects": [{
    "id\": \"effect-material-uuid\",
    "name\": \"<花字名稱>\",
    "effect_id\": \"<effect-id>\"
  }]
}
```

**換花字 JSON edit 必改 3 處**：
1. `text.content.styles[].effectStyle.id` + `.path`（決定哪個花字）
2. `text.content.styles[].fill.content`（splash 類用 texture / crayon 類用 solid color）
3. `materials.effects` list 內對應條目 + `segment.extra_material_refs`

## 一組常用免費花字搭配示意（以 vlog 類型為例）

> 以下為一組常用免費花字的搭配示意，你可以挑類似角色的免費模板自行組合：

| 角色 | 模板 | 分類 | 備註 |
|---|---|---|---|
| DAY marker (3x) | **A DAY IN A LIFE** | 復古 | 粗黑體大字 |
| Location reveal (8x) | **Location + Sub-Location** | 旅行 | Pin icon + 兩行（地點 + 副題） |
| Emphasis stamp (5x) | **SPOKE** | 大熱 | 黃色粗體 + 黑邊（綜藝旅遊節目風）|
| Narrative lower-third (12x) | **YOUR TITLE / The subtitle** | 標記 | 左側 accent bar |

## 🏆 某類型 vlog 的通用花字混搭原則

以下為一組 vlog 花字混搭的通用設定原則（**定版後絕對不要 JSON 改回 uniform**）：

### Effects 混搭（不是套同一個花字）
| Effect 類型 | 數量比例 | 用途 |
|---|---|---|
| **主力花字**（粗黑描邊風）| 最大宗 | 大部分 caption 套這個 |
| **通用花字** (generic) | 次要 | 變化補充 |
| **反白描邊花字** | 補充 | emphasis 用 |
| **特定段花字** | 少量 | 特定片段 |
| **氣泡 (bubble) 花字** | 1-2 個 | speech bubble 場景 |

→ **規則**：vlog caption 應該**混搭 4-5 種花字**，不是套同一個。

⚠️ **教訓（agent 反推誤標）**：靠 mtime / cache 反推 canonical 主力 effect 容易誤標。effect 全 cached at `<CapCut User Data>/Cache/effect/<id>/`，但 cache 只代表「最近用過」不代表「創作者主力」。**主力 effect 一律以創作者手動定版的 JSON 為準**，不要憑反推猜。

### 字體 size + scale 配對（不是固定）
| 用途 | font_size | scale | 範例性質 |
|---|---|---|---|
| Marker (DAY / 開場大字) | 11 | 0.85 | 段落標記 |
| 一般時間戳 main | 7 | 0.85 | 時間戳敘述 |
| **重點強調** | **5** | **1.16-1.43** | 店名 / 關鍵數字 |
| Speech bubble | 8 | 0.63 | 對白氣泡 |

→ **規則**：「重點強調」用 **小字 + 大 scale** 反而 punchier（不是直接 11pt）

### 位置 (clip.transform.x, y)
- Markers 角落：`(-0.46, -0.70)` / `(-0.35, -0.70)` / `(0.30, -0.60)`
- 一般 main 中下：`(0.00, 0.58 ~ 0.66)`
- 重點 / 避開主體：`(0.00, -0.50)` 頂部 / `(0.20, 0.60)` 偏右

### 🌫️ Canvas blur（重要！照片背景延伸）
- 一支 vlog 可套 **10+ 個** segments 用 `canvas_blur`
- 主要套在 **portrait（直式）照片**，把黑邊 letterbox 變成 blur 延伸背景
- JSON 結構：`materials.canvases` entries with `type: "canvas_blur", blur: 1.0`
- 這是 vlog 看起來專業的關鍵之一 — **你可以在 build 時預設套到所有 portrait 照片**

## 🌟 找創作者 favorited 花字 SOP

**Navigation flow**：
1. 文字 (TI 圖示) toolbar tab
2. 右側 panel 找「**花字**」sub-tab（在「基礎 / 泡泡音 / 花字」3 個切換中）
3. 點 ⭐ **星星 icon** filter → 切到「我的最愛」view
4. 顯示 favorited collection（通常 8-10 個）
5. 找有 **turquoise border + 小 ⭐ on top-right** 的 icon = 當前 highlighted target

**Disk 對應位置**：
- favorites 不存在 `Cache/effect/<ID>/`（那是「最近用過」cache）
- 也不在 `ressdk_db rp.db favorite_effect` 表（empty / 不用這個）
- 真實 favorited list 存在 **CapCut cloud account**（user login Pro）→ 無法 disk parse
- **要 agent 跑去 GUI 看 panel 才能確認 ID**

**❌ mtime 反推不可靠**（實測證實錯誤）：
- 用 mtime 排序猜 favorite → 結果與創作者真實選擇不符
- favorites 跨裝置 sync **cloud-stored**，local cache mtime 不代表 favorites 排序

**唯一可靠**：spawn agent reverse engineer → 套到 1 個 segment → diff JSON 抓 effect_id

**Reverse engineer 公式**：
```
1. Backup draft 全 JSON → before/
2. Agent: 套 highlighted 花字 到任意 1 個 segment + Ctrl+S
3. Copy after → after/
4. Diff: NEW materials.effects entry → 抓 effect_id
   - 通常 name 是中文（如「黑綠描邊背景」這類）
   - category_name = "我的最愛" 表示 favorited
   - 比 bubble 多很多 fields (adjust_params / beauty_* / panel_id 等)
5. JSON 複製 effect entry × N (new UUID each) → segment.extra_material_refs 更新
```

## Pro 旅行 panel 模板（訂閱後解鎖）

| 模板 | 風格 | 推薦用途 |
|---|---|---|
| **Travelling With Me** | 旅行 vlog 開場感 | DAY 1 marker（替代 A DAY IN A LIFE）|
| **LOCATION**（大紅 pin） | 高張力地點 emphasis | 重點地點 reveal |
| **SUMMER IN BALI** | 旅遊大標 | 可改地名 — 開場 Hook |
| **Destination** | 多 text field 含敘述 | 重點 + 詳細的時刻 |
| **CINEMA-VLOG** | 電影風 vlog | DAY marker 替代選項 |
| **City, COUNTRY** | 地名 + 國名 | 可改成目的地 — Hook 後第一張 |
| **Address Location** | 詳細地址 | 餐廳名 / 飯店名 |

## 已試過模板

| 模板名 | CapCut 分類 | Pro? | 評價 | 適用 |
|---|---|---|---|---|
| **Dynamic white crayon hand-drawn** | panel-text-flower (花字) | ✅ Free | ⚠️ 還可接受，但全套同一個會嫌單調 | **單調 — 不要全片套同一個** |
| **Colorful Paint Graffiti** | panel-text-flower (花字) | ✅ Free | ❌ 兒童 splash 風，**沒綜藝感、沒出去玩感覺** | **避免**，不適合旅遊 vlog |
| ~~春日光效~~ | transition (轉場) | ❌ Pro | — | 卡 Export（免費版）|
| ~~自動調整~~ | effects (特效) | ❌ Pro | — | 卡 Export（免費版）|

## 「綜藝感 / 出去玩感」特徵

從創作者吐槽歸納：
1. **多模板變化** — 不要一整片 caption 全套同一花字
2. **顏色對比** — 黃 + 紅 + 黑邊（vs splash 太花）
3. **粗黑體 + 描邊** — 綜藝旅遊節目標配
4. **重點時刻 emphasis stamp** — 「驚!」「天啊!」「竟然!」浮出
5. **時間戳專屬樣式** — 「現在時間 X」用獨立模板

## 找模板 SOP（agent 套之前）

### Phase 1: 探索（screenshot 1 張給創作者 review）
```
左側 toolbar「文字」→「文字模板」
分類順序看：
  1. 字幕條（lower-third 風）
  2. 標題（marker 風）
  3. 綜藝（重點 emphasis）
  4. 字幕（一般 narrative）
  5. 旅行（如有）

每分類**只挑下載 icon ⬇**，菱形💎（Pro）直接跳過

挑 4 個候選 → screenshot 給創作者 review
```

### Phase 2: 多模板分配
不要全片套同一個。建議比例（以約 28 個 caption 為例）：
- **marker (3 個)** — 用「標題」類粗體大字
- **時間戳 main (~10 個)** — 用「字幕條」類 lower-third
- **重點 main (~5 個)** — 用「綜藝」類 emphasis
- **sub (~10 個)** — 用「字幕」類簡潔小字

## 創作者確認後才大規模套

絕對禁止：未經確認就大規模套滿全片 → 套錯重來 1 小時。

```
agent 步驟：
1. 套 4 個 sample（4 個分類各 1 個）
2. Export 試片給創作者看
3. 確認 OK → 套剩餘的
4. NG → 換模板再試
```
