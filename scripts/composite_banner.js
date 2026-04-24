// composite_banner.js
// Hybrid Script — Functional + Editable
// Builds the neon-noir banner using parallax + weather layers.

const { createCanvas, loadImage } = require("canvas");
const fs = require("fs");

const WIDTH = 1920;
const HEIGHT = 600;
const FRAMES = 4;

async function compositeFrame(i) {
  const canvas = createCanvas(WIDTH, HEIGHT);
  const ctx = canvas.getContext("2d");

  const bg = await loadImage("assets/cityscapes/parallax/background/layer.png");
  const mg = await loadImage("assets/cityscapes/parallax/midground/layer.png");
  const fg = await loadImage("assets/cityscapes/parallax/foreground/layer.png");

  const rain = await loadImage(`assets/cityscapes/weather/rain/frame_${i}.png`);
  const fog = await loadImage(`assets/cityscapes/weather/fog/frame_${i}.png`);
  const shimmer = await loadImage(`assets/cityscapes/weather/shimmer/frame_${i}.png`);

  ctx.drawImage(bg, 0, 0, WIDTH, HEIGHT);
  ctx.drawImage(mg, 0, 0, WIDTH, HEIGHT);
  ctx.drawImage(fg, 0, 0, WIDTH, HEIGHT);
  ctx.drawImage(rain, 0, 0, WIDTH, HEIGHT);
  ctx.drawImage(fog, 0, 0, WIDTH, HEIGHT);
  ctx.drawImage(shimmer, 0, 0, WIDTH, HEIGHT);

  fs.writeFileSync(`assets/banners/banner_frame_${i}.png`, canvas.toBuffer());
}

async function buildBanner() {
  for (let i = 0; i < FRAMES; i++) {
    await compositeFrame(i);
  }
  console.log("Banner frames generated.");
}

buildBanner();
