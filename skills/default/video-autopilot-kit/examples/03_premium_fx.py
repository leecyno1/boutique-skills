#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example 03 — premium motion FX on a synthetic stat card, with ZERO real media.

This is the fastest way to see `longform_maker.fx_lib` work: it draws a dark
stat card in PIL, then renders a ~3s clip that demonstrates the "wave-1"
premium stack from `knowledge/premium-motion-fx.md`:

  * count-up number with `ease_out_expo` — final frame is ASSERTED to equal
    the true value (never ship an eased approximation of a real number)
  * double-layer additive bloom (tight 4px + wide 16px) on the number
  * a 45° light sweep right after the counter lands
  * sub-pixel Ken Burns push-in (float AFFINE — the anti-`zoompan`)
  * per-frame film grain + vignette (`texture_pass`)
  * a synthesized whoosh SFX aligned to the start (no audio assets needed)

Run:
    python examples/03_premium_fx.py

Needs: Python 3.9+, Pillow, numpy, and `ffmpeg` on your PATH. Output:
    out/premium_fx_demo.mp4  (1280x720, ~3s, 30fps, with sound)
"""
import os
import sys
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))

from PIL import Image, ImageDraw, ImageFont  # noqa: E402
from longform_maker import fx_lib as fx      # noqa: E402

OUT_DIR = os.path.join(HERE, "out")
FRAMES = os.path.join(OUT_DIR, "_fx_frames")
W, H = 1280, 720
FPS = 30
TRUE_VALUE = 1234567          # the "real" stat this card claims
N_COUNT = int(FPS * 1.2)      # 1.2s count-up
N_TOTAL = int(FPS * 3.0)      # 3s clip


def _font(size):
    """Bundled-font-free: try a common system font, fall back to PIL default."""
    for name in ("arialbd.ttf", "arial.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def draw_card(count_value, glow=0.0, sweep_t=None):
    """One frame of the stat card (2x supersampled for the Ken Burns crop)."""
    im = Image.new("RGB", (W * 2, H * 2), (16, 14, 34))
    d = ImageDraw.Draw(im)
    for x in range(0, W * 2, 160):                       # faint grid
        d.line([(x, 0), (x, H * 2)], fill=(28, 26, 52), width=1)
    d.text((160, 200), "VIEWS — LAST 90 DAYS", font=_font(56), fill=(150, 150, 180))

    # number on its own layer -> bloom -> sweep -> composite
    num = f"{count_value:,}"
    layer = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((150, 300), num, font=_font(220), fill=(255, 210, 63, 255),
                               stroke_width=10, stroke_fill=(40, 26, 5, 255))
    if glow > 0:
        layer = fx.double_bloom(layer, tight=4, wide=16,
                                tight_op=0.6 * glow, wide_op=0.3 * glow)
    if sweep_t is not None:
        layer.alpha_composite(fx.light_sweep(layer, sweep_t))
    base = im.convert("RGBA")
    base.alpha_composite(layer)
    return base.convert("RGB")


def main():
    os.makedirs(FRAMES, exist_ok=True)
    for i in range(N_TOTAL):
        if i < N_COUNT:
            t = (i + 1) / N_COUNT
            val = int(TRUE_VALUE * fx.ease_out_expo(t))
            glow, sweep = 0.0, None
        else:
            val = TRUE_VALUE
            k = i - N_COUNT
            glow = max(0.4, 1.0 - k / 8 * 0.6)                     # pulse 1 -> 0.4
            sweep = (k - 6) / 14 if 6 <= k <= 20 else None         # 0.5s sweep
        if i >= N_COUNT:
            # M10-style gate: a real stat must land EXACTLY on the true value.
            assert f"{val:,}" == "1,234,567"
        card2x = draw_card(val, glow=glow, sweep_t=sweep)
        frame = fx.ken_burns_frame(card2x, i / (N_TOTAL - 1),
                                   z0=1.0, z1=1.05, ease=fx.smootherstep,
                                   out_size=(W, H))
        frame = fx.texture_pass(frame, grain=5, vig=0.14, seed=i)
        frame.save(os.path.join(FRAMES, f"f_{i:04d}.png"))

    whoosh = os.path.join(OUT_DIR, "_whoosh.wav")
    fx.sfx_whoosh(whoosh, dur=0.5)
    out = os.path.join(OUT_DIR, "premium_fx_demo.mp4")
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS),
                    "-i", os.path.join(FRAMES, "f_%04d.png"), "-i", whoosh,
                    "-filter_complex", "[1:a]apad[a]",
                    "-map", "0:v", "-map", "[a]",
                    "-vf", "curves=master='0/0.02 0.5/0.5 1/0.98',format=yuv420p",
                    "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-shortest", out],
                   check=True, capture_output=True, encoding="utf-8", errors="replace")
    for f in os.listdir(FRAMES):
        os.remove(os.path.join(FRAMES, f))
    os.rmdir(FRAMES)
    print("OK ->", out)


if __name__ == "__main__":
    main()
