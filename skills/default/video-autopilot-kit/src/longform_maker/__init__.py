# -*- coding: utf-8 -*-
"""
longform_maker — ffmpeg-first helpers for teaching long-form video builds.

Ported from a production long-form pipeline (v0.7.0). Three modules:

| Module | What |
|---|---|
| `fx_lib.py` | easing / stagger / grain·vignette·chromatic texture pass / sub-pixel Ken Burns (replaces jittery integer `zoompan`) / glow·bloom·light-sweep / synthesized SFX (whoosh/pop/tick/hit/riser) |
| `word_captions.py` | **M105** word-level caption timing — whisper `word_timestamps` -> smart CJK line-breaking with real word times (never hand-split coarse segments; they drift 2-3 s) + optional per-line keyword emphasis |
| `screen_clean.py` | **M104** screen-recording sanitizer — mandatory head/tail trim (recorder UI lives at both ends) + crop browser/IDE chrome + blur-pad to canvas + strip audio + fixed blur boxes for on-screen names |

Each module is import-light and ships a real-ffmpeg self-test:
`python fx_lib.py` / `python word_captions.py` / `python screen_clean.py`.

Usage:
    from longform_maker import (
        ease_out_expo, ken_burns_frame, texture_pass, double_bloom, light_sweep,
        sfx_whoosh, sfx_pop, sfx_tick, sfx_hit, sfx_riser,
        transcribe_words, group_words, to_master_events, build_ass, emphasize_line,
        clean_screen_recording,
    )
"""
from .fx_lib import (
    ease_linear, ease_out_cubic, ease_out_quint, ease_in_out_sine,
    ease_out_back, ease_out_elastic, ease_out_expo, smootherstep, stagger,
    film_grain, vignette, chromatic_aberration, texture_pass,
    ken_burns_frame, glow_pulse, double_bloom, light_sweep,
    sfx_whoosh, sfx_pop, sfx_tick, sfx_hit, sfx_riser,
)
from .word_captions import (
    BASE_FIXES, EMPHASIS_TERMS,
    apply_fixes_to_words, transcribe_words, fix_text, group_words,
    to_master_events, emphasize_line, chapter_card_tag, build_ass,
)
from .screen_clean import clean_screen_recording, MIN_HEAD_TRIM, MIN_TAIL_TRIM

__all__ = [
    # fx_lib
    "ease_linear", "ease_out_cubic", "ease_out_quint", "ease_in_out_sine",
    "ease_out_back", "ease_out_elastic", "ease_out_expo", "smootherstep", "stagger",
    "film_grain", "vignette", "chromatic_aberration", "texture_pass",
    "ken_burns_frame", "glow_pulse", "double_bloom", "light_sweep",
    "sfx_whoosh", "sfx_pop", "sfx_tick", "sfx_hit", "sfx_riser",
    # word_captions (M105)
    "BASE_FIXES", "EMPHASIS_TERMS",
    "apply_fixes_to_words", "transcribe_words", "fix_text", "group_words",
    "to_master_events", "emphasize_line", "chapter_card_tag", "build_ass",
    # screen_clean (M104)
    "clean_screen_recording", "MIN_HEAD_TRIM", "MIN_TAIL_TRIM",
]
