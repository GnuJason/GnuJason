// build_right_panel.js
// Hybrid Script — Functional + Editable
// Builds the tall right-side panel for the README.

const { createCanvas, loadImage } = require("canvas");
const fs = require("fs");

const WIDTH = 500;
const HEIGHT = 1000;

async function buildPanel() {
  const canvas = createCanvas(WIDTH, HEIGHT);
  const ctx = canvas.getContext("2d");

  const bg = await loadImage("assets/cityscapes/parallax/background/layer.png");
  const mg = await loadImage("assets/cityscapes/parallax/midground/layer.png");
  const fg = await loadImage("assets/cityscapes/parallax/foreground/layer.png");

  ctx.drawImage(bg, 0, 0, WIDTH, HEIGHT);
  ctx.drawImage(mg, 0, 0, WIDTH, HEIGHT);
  ctx.drawImage(fg, 0, 0, WIDTH, HEIGHT);

  fs.writeFileSync("assets/cityscapes/tall-right-panel.gif", canvas.toBuffer());
  console.log("Right panel generated.");
}

buildPanel();
