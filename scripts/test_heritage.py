"""Regression contracts for composition fidelity, subtle motion and placement."""

import unittest

from PIL import Image, ImageChops, ImageStat

import build_heritage as heritage
from build_profile import ROOT, ASSETS
from test_profile import ReadmeImages


class HeritageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with Image.open(heritage.SOURCE) as source:
            cls.original = source.convert("RGB")
        with Image.open(heritage.OUTPUT / "korean-american-heritage-still.png") as still:
            cls.still = still.convert("RGB")

    def test_native_resolution_and_detail(self):
        self.assertEqual(self.still.size, self.original.size)
        difference = ImageChops.difference(self.original, self.still)
        self.assertIsNotNone(difference.getbbox())
        self.assertLess(max(ImageStat.Stat(difference).rms), 3)
        self.assertLessEqual(max(high for low, high in difference.getextrema()), 18)
        for bounds in heritage.PROTECTED_REGIONS:
            with self.subTest(bounds=bounds):
                self.assertIsNone(difference.crop(bounds).getbbox())
        # Native one-pixel detail must not have been reduced to a coarse grid.
        small = self.still.resize((768, 512), Image.Resampling.NEAREST)
        restored = small.resize(self.still.size, Image.Resampling.NEAREST)
        self.assertIsNotNone(ImageChops.difference(self.still, restored).getbbox())
        self.assertGreater(len(self.still.getcolors(self.still.width * self.still.height)), 10000)

    def test_pixel_treatment_is_reproducible(self):
        self.assertEqual(heritage.pixel_treatment(self.original).tobytes(), self.still.tobytes())
        with self.assertRaises(ValueError):
            heritage.pixel_treatment(Image.new("RGB", (768, 512)))

    def test_animation_and_loop(self):
        path = heritage.OUTPUT / "korean-american-heritage.gif"
        palette = heritage.palette_for(self.still)
        base = self.still.quantize(palette=palette, dither=Image.Dither.NONE)
        self.assertLess(max(ImageStat.Stat(ImageChops.difference(
            self.still, base.convert("RGB"))).rms), 7)
        self.assertLess(path.stat().st_size, 5 * 1024 * 1024)
        with Image.open(path) as gif:
            self.assertEqual(gif.size, heritage.SIZE)
            self.assertEqual(gif.n_frames, heritage.FRAMES)
            self.assertEqual(gif.info["loop"], 0)
            for index in range(gif.n_frames):
                gif.seek(index)
                self.assertEqual(gif.info["duration"], heritage.DURATION)
                actual = gif.convert("RGB")
                expected = heritage.animation_frame(base, palette, index).convert("RGB")
                self.assertEqual(actual.tobytes(), expected.tobytes(), f"frame {index}")
                diff = ImageChops.difference(base.convert("RGB"), actual)
                red, green, blue = diff.split()
                changed = ImageChops.lighter(ImageChops.lighter(red, green), blue)
                changed = changed.point(lambda p: 255 if p else 0).histogram()[255]
                self.assertGreater(changed, 0)
                self.assertLess(changed / (gif.width * gif.height), 0.001)
                for bounds in heritage.TEXT_REGIONS:
                    self.assertIsNone(diff.crop(bounds).getbbox())
        self.assertEqual(heritage.blossom_layer(0).tobytes(),
                         heritage.blossom_layer(heritage.FRAMES).tobytes())
        for petal in heritage.PETALS:
            positions = [heritage.petal_position(petal, f) for f in range(heritage.FRAMES + 1)]
            for a, b in zip(positions, positions[1:]):
                if b[1] < a[1]:
                    self.assertLess(max(a[2], b[2]), 0.10)
                else:
                    self.assertLessEqual(b[1] - a[1], 5)
                    self.assertLessEqual(abs(b[0] - a[0]), 3)

    def test_accents_leave_existing_art_intact(self):
        counts = [len(points) for points in heritage.DIVIDER_PETALS.values()]
        self.assertEqual(counts, [7, 3, 1])
        with Image.open(ASSETS / "ascii-dividers/bunker-divider.png") as source:
            original = source.convert("RGB")
        for level in heritage.DIVIDER_PETALS:
            with Image.open(heritage.OUTPUT / f"petal-divider-{level}.png") as image:
                self.assertEqual(image.size, original.size)
                self.assertEqual(image.tobytes(), heritage.divider(level).tobytes())
                self.assertEqual(image.crop((0, 10, 1500, 14)).tobytes(),
                                 original.crop((0, 10, 1500, 14)).tobytes())
        with Image.open(ASSETS / "opensuse/opensuse-pixel.png") as source:
            original = source.convert("RGB")
        with Image.open(heritage.OUTPUT / "opensuse-petal-footer.png") as image:
            self.assertEqual(image.tobytes(), heritage.footer().tobytes())
            difference = ImageChops.difference(original, image)
            bounds = difference.getbbox()
            self.assertIsNotNone(bounds)
            left, top, right, bottom = bounds
            self.assertGreaterEqual(left, 1056)
            self.assertGreaterEqual(top, 206)
            self.assertLessEqual(right, 1290)
            self.assertLessEqual(bottom, 217)
            self.assertLess(sum(ImageStat.Stat(difference).mean), 1)

    def test_identity_first_and_sparse_transitions(self):
        readme = (ROOT / "README.md").read_text()
        parser = ReadmeImages()
        parser.feed(readme)
        paths = [attrs["src"] for attrs in parser.images]
        self.assertEqual(paths[:2], [
            "assets/heritage/korean-american-heritage.gif",
            "assets/banners/bunker-engineer.gif",
        ])
        self.assertEqual(parser.images[0]["width"], "100%")
        self.assertNotIn("height", parser.images[0])
        self.assertTrue(readme.startswith('<picture>\n  <source media="(prefers-reduced-motion: reduce)" '
                                        'srcset="assets/heritage/korean-american-heritage-still.png">'))
        self.assertEqual(paths.count("assets/ascii-dividers/bunker-divider.png"), 2)
        for level, target in (("near", "operator-log"), ("middle", "project-bays"),
                              ("far", "open-channel")):
            path = f"assets/heritage/petal-divider-{level}.png"
            self.assertEqual(paths.count(path), 1)
            self.assertEqual(next(a for a in parser.images if a["src"] == path)["alt"], "")
            self.assertLess(readme.index(path), readme.index(f'id="{target}"'))
        self.assertEqual(paths[-2:], ["assets/heritage/opensuse-petal-footer.png",
                                     "assets/banners/bunker-footer.png"])
        self.assertEqual(parser.headings, ["h1"])


if __name__ == "__main__":
    unittest.main()
