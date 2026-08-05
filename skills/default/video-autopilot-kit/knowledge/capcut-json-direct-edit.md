> 來自 video-autopilot-kit 開源知識庫 · MIT 授權

# JSON Direct Edit (Path D, **0 GUI 0 agent token**)

## ⚠️ M41 — 花字效果 JSON 結構

**錯誤假設**（曾撞過）：花字效果 = `materials.effects` + `content.styles[].effectStyle.id`

**真相**：CapCut 渲染花字依賴 **`materials.flowers`** 陣列（這 array 通常空 = 沒花字 / 有 entries = 有花字）。
- 改 `effectStyle.id` **沒用** — CapCut 不認
- 必須在 `materials.flowers` 加 entry + 在 segment.extra_material_refs 指向 flowers entry ID

**Reverse engineer 待做**：
- Spawn agent 在 CapCut GUI 套 1 個花字到 1 個 caption → save → 比對 JSON before/after
- Diff `materials.flowers[]` + `tracks[text].segments[].extra_material_refs` 變化
- 學到正確 structure 後寫進 example 給未來 patch

直到 reverse engineer 完成 — **花字效果 only 可 GUI 套，無法 JSON patch**。

## ⚠️ M18 升級 — JSON edit 必同步 3 處

之前以為改 root `draft_content.json` + `draft_info.json` 就夠了 — **錯**。

CapCut 開專案時優先讀 `Timelines/<UUID>/draft_content.json`，會覆蓋 root 版本。

**JSON edit 強制同步腳本**：
```python
import shutil
from pathlib import Path
DRAFT = Path(...)
root = DRAFT / 'draft_content.json'
for tl in (DRAFT / 'Timelines').iterdir():
    if tl.is_dir():
        tl_dc = tl / 'draft_content.json'
        if tl_dc.exists():
            shutil.copy(root, tl_dc)  # sync from root
```

跟 .bak 一樣 — 不一定要清，但 CapCut 開時可能 fall back 到 .bak，所以最好也同步。

> 比 spawn agent 操作 CapCut GUI 便宜 100x。
> 適用：text content / font / size / position / volume 變更。
> 不適用：套新模板 (template_id 要下載)、加貼圖、新 transition。

## CapCut Draft JSON 結構速查

### File location
```
C:\Users\<USERNAME>\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\<PROJECT>\
├── draft_content.json   ← CapCut 讀這個 render
├── draft_info.json      ← copy of draft_content（M18 規則：同步改 2 個）
├── Resources/
├── Timelines/<UUID>/draft_content.json  ← 也要同步改（M18 規則）
└── ...
```

### 改 caption 文字（**保留花字效果**）

```python
import json
from pathlib import Path

DRAFT = Path(r'C:\Users\<USERNAME>\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\<PROJECT>')

mapping = {
    'old_text_1': 'new_text_1',
    'old_text_2': 'new_text_2',
    # ...
}

for fname in ['draft_content.json', 'draft_info.json']:
    p = DRAFT / fname
    d = json.load(open(p, encoding='utf-8'))
    for t in d.get('materials', {}).get('texts', []):
        content_str = t.get('content', '{}')
        co = json.loads(content_str)
        old = co.get('text', '')
        new = mapping.get(old)
        if new is None: continue
        co['text'] = new
        # IMPORTANT: 更新 styles[].range 對應新 text 長度
        for s in co.get('styles', []):
            if 'range' in s:
                s['range'] = [0, len(new)]
        t['content'] = json.dumps(co, ensure_ascii=False, separators=(',', ':'))
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, separators=(',', ':'))
```

### 改 font / size

```python
for t in texts:
    t['font_path'] = 'C:/Windows/Fonts/NotoSansTC-Black.otf'
    t['font_size'] = 11.0
    # 同步 nested
    co = json.loads(t['content'])
    for s in co.get('styles', []):
        s['size'] = 11.0
        s['font'] = {'path': 'C:/Windows/Fonts/NotoSansTC-Black.otf', 'id': '', 'cn_name': '', 'tw_name': ''}
    t['content'] = json.dumps(co, ensure_ascii=False, separators=(',', ':'))
```

### 改 caption position

```python
# Text track segment 內
for tr in d.get('tracks', []):
    if tr.get('type') != 'text': continue
    for seg in tr.get('segments', []):
        # transform.y: -1=top, 0=center, +1=bottom
        seg.setdefault('clip', {}).setdefault('transform', {})['y'] = -0.85  # 例：top
```

### 改 video audio (mute) — M29 四重 lock

**早期失敗原因**：只設 `volume=0` + `has_sound_separated=True` 不夠 — CapCut Export 仍 fallback 到 raw video audio（B-roll 風聲人聲漏出來）。

**完整 4 重 lock 公式**：
```python
# Material 層 — 關鍵：has_audio=False 告訴 CapCut「這個材質沒有音訊」
for m in d.get('materials', {}).get('videos', []):
    if not m.get('has_audio', False): continue  # skip images (已 False)
    m['has_audio'] = False              # ⭐ 主關鍵
    m['has_sound_separated'] = True     # backup signal

# Segment 層 — triple-lock
for tr in d.get('tracks', []):
    if tr.get('type') != 'video': continue
    for seg in tr.get('segments', []):
        seg['volume'] = 0.0
        seg['last_nonzero_volume'] = 0.0
        seg['intensifies_audio'] = False  # 也關 boost
```

**Verify 必跑**（不能 trust JSON，要看實際 export）：
```bash
ffmpeg -y -i v[N].mp4 -vn -ac 1 -ar 16000 audio.wav
ffmpeg -y -i audio.wav -filter_complex 'showwavespic=s=1920x300:colors=cyan' -frames:v 1 wave.png
```
連續飽和 = BGM only ✅ / 稀疏 spike = B-roll 漏出來 ❌

## ⚠️ Auto-save trap (M20)

CapCut **必須先 kill** 才 edit JSON：
```python
import subprocess
subprocess.run(['powershell', '-NoProfile', '-Command',
                'Get-Process CapCut -ErrorAction SilentlyContinue | Stop-Process -Force'])
```

否則 CapCut 開著時 edit JSON → CapCut auto-save 把 memory state 寫回 → 你的 edit 被覆蓋。

## ⚠️ Path backslash trap (M18)

JSON 內路徑 `\` 存 2 chars (e.g. `\\\\`)，Python source 要 `\\\\\\\\` (8 chars)。
Bash heredoc 處理 `\\` 有 bug → 寫 .py file 跑，不要 inline。

## Post-edit checklist

1. JSON 改完 → 直接讓用戶開 CapCut → load 專案 → 應該顯示新狀態
2. 用戶確認 OK → 點 Export
3. **Export 步驟 spawn Path A agent**（約 4-5 分鐘）or 用戶手動

→ 加總成本：JSON edit (~5K tokens) + Path A agent (~40K tokens) = ~45K tokens  
→ vs spawn Path B agent (~92K tokens) **省 50%+**
