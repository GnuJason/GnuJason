# build_footer_loop.py
# Hybrid Script — Functional + Editable
# Builds the footer skyline night loop using parallax + weather layers.

from PIL import Image
import os

FRAMES = 12
WIDTH = 1024
HEIGHT = 320

OUTPUT = "assets/cityscapes"
PARALLAX = "assets/cityscapes/parallax"
WEATHER = "assets/cityscapes/weather"

def load_layer(path):
    return Image.open(path).convert("RGBA")

def build_frame(i):
    bg = load_layer(f"{PARALLAX}/background/layer.png").resize((WIDTH, HEIGHT))
    mg = load_layer(f"{PARALLAX}/midground/layer.png").resize((WIDTH, HEIGHT))
    fg = load_layer(f"{PARALLAX}/foreground/layer.png").resize((WIDTH, HEIGHT))

    rain = load_layer(f"{WEATHER}/rain/frame_{i}.png").resize((WIDTH, HEIGHT))
    fog = load_layer(f"{WEATHER}/fog/frame_{i}.png").resize((WIDTH, HEIGHT))
    shimmer = load_layer(f"{WEATHER}/shimmer/frame_{i}.png").resize((WIDTH, HEIGHT))

    frame = Image.alpha_composite(bg, mg)
    frame = Image.alpha_composite(frame, fg)
    frame = Image.alpha_composite(frame, rain)
    frame = Image.alpha_composite(frame, fog)
    frame = Image.alpha_composite(frame, shimmer)

    return frame

def build_gif():
    frames = [build_frame(i) for i in range(FRAMES)]
    frames[0].save(
        f"{OUTPUT}/skyline-loop.gif",
        save_all=True,
        append_images=frames[1:],
        duration=120,
        loop=0,
        disposal=2
    )

if __name__ == "__main__":
    build_gif()
    print("Footer skyline loop generated.")
