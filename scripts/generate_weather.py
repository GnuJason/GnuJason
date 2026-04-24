# generate_weather.py
# Hybrid Script — Functional + Editable
# Generates neon-noir weather loops: rain, fog, shimmer.

from PIL import Image, ImageDraw
import numpy as np
import os

BASE_W = 1920
BASE_H = 600
FRAMES = 12

OUTPUT = "assets/cityscapes/weather"

PALETTE = {
    "rain": (0, 229, 255),
    "fog": (169, 112, 255),
    "shimmer": (255, 46, 245)
}

def ensure_dirs():
    os.makedirs(f"{OUTPUT}/rain", exist_ok=True)
    os.makedirs(f"{OUTPUT}/fog", exist_ok=True)
    os.makedirs(f"{OUTPUT}/shimmer", exist_ok=True)

def generate_rain():
    for i in range(FRAMES):
        img = Image.new("RGBA", (BASE_W, BASE_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        for _ in range(300):
            x = np.random.randint(0, BASE_W)
            y = np.random.randint(0, BASE_H)
            draw.line([(x, y), (x+3, y+10)], fill=PALETTE["rain"] + (180,), width=1)

        img.save(f"{OUTPUT}/rain/frame_{i}.png")

def generate_fog():
    for i in range(FRAMES):
        img = Image.new("RGBA", (BASE_W, BASE_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        fog_x = int((i / FRAMES) * BASE_W)
        draw.rectangle([fog_x - 400, 0, fog_x + 400, BASE_H],
                       fill=PALETTE["fog"] + (40,))

        img.save(f"{OUTPUT}/fog/frame_{i}.png")

def generate_shimmer():
    for i in range(FRAMES):
        img = Image.new("RGBA", (BASE_W, BASE_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        for _ in range(50):
            x = np.random.randint(0, BASE_W)
            y = np.random.randint(0, BASE_H)
            alpha = np.random.randint(80, 160)
            draw.rectangle([x, y, x+2, y+2], fill=PALETTE["shimmer"] + (alpha,))

        img.save(f"{OUTPUT}/shimmer/frame_{i}.png")

if __name__ == "__main__":
    ensure_dirs()
    generate_rain()
    generate_fog()
    generate_shimmer()
    print("Weather loops generated.")
