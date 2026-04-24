# generate_parallax.py
# Hybrid Script — Functional + Editable
# Generates pixel-art parallax skyline layers for the neon-noir banner.

from PIL import Image, ImageDraw
import numpy as np
import os

OUTPUT_DIR = "assets/cityscapes/parallax"
PALETTE = {
    "cyan": (0, 229, 255),
    "magenta": (255, 46, 245),
    "violet": (169, 112, 255),
    "black": (10, 10, 20),
    "navy": (26, 27, 39)
}

WIDTH = 1920
HEIGHT = 600

def ensure_dirs():
    os.makedirs(f"{OUTPUT_DIR}/foreground", exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/midground", exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/background", exist_ok=True)

def draw_buildings(draw, count, min_h, max_h, color):
    for _ in range(count):
        x = np.random.randint(0, WIDTH)
        w = np.random.randint(20, 80)
        h = np.random.randint(min_h, max_h)
        y = HEIGHT - h
        draw.rectangle([x, y, x + w, HEIGHT], fill=color)

def generate_background():
    img = Image.new("RGB", (WIDTH, HEIGHT), PALETTE["navy"])
    draw = ImageDraw.Draw(img)

    # distant silhouettes
    draw_buildings(draw, 40, 80, 180, PALETTE["black"])

    img.save(f"{OUTPUT_DIR}/background/layer.png")

def generate_midground():
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw_buildings(draw, 30, 120, 260, PALETTE["violet"])

    img.save(f"{OUTPUT_DIR}/midground/layer.png")

def generate_foreground():
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw_buildings(draw, 20, 200, 380, PALETTE["magenta"])

    img.save(f"{OUTPUT_DIR}/foreground/layer.png")

if __name__ == "__main__":
    ensure_dirs()
    generate_background()
    generate_midground()
    generate_foreground()
    print("Parallax layers generated.")
