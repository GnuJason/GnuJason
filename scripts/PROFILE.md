# Bunker 07 / Profile Artwork

The profile uses original procedural bitmap art and a hand-defined pixel font.
All embedded artwork is stored in this repository; no image-generation keys,
remote badge services, JavaScript, or custom README CSS are required.

## Rebuild

From the repository root, with Python 3.10 or newer:

```sh
python3 -m venv /tmp/gnujason-profile-venv
/tmp/gnujason-profile-venv/bin/pip install -r scripts/requirements-profile.txt
/tmp/gnujason-profile-venv/bin/python scripts/build_profile.py
/tmp/gnujason-profile-venv/bin/python -m unittest discover -s scripts -p 'test_profile.py' -v
```

Use `--still` for a fast banner composition check. A full build is required
afterward to update the GIF and supporting assets. Rendering is deterministic.

Use `--opensuse-only` to rebuild just the 1500 x 224 dedication strip from the
supplied `assets/icons/openSUSW_lizard.png`. The renderer isolates the lizard,
uses the profile purple with cyan and pink circuitry on near-black, and
enlarges a 750 x 112 raster exactly 2x with nearest-neighbor sampling. The
README places it full-width below the transmission banner, scales its height
proportionally on mobile, and links to the main openSUSE site.

## Art Direction

### Korean-American heritage

The supplied full-resolution original is preserved in `assets/Designer.png`.
Its complete 1536 x 1024 composition opens the README before the bunker hero:
this is an identity image, not a project card or a toolchain badge.

Rebuild the heritage assets independently, without regenerating existing art:

```sh
/tmp/gnujason-profile-venv/bin/python scripts/build_heritage.py
/tmp/gnujason-profile-venv/bin/python -m unittest discover -s scripts -p 'test_*.py' -v
```

`assets/heritage/korean-american-heritage-still.png` retains native resolution
and true color. The source already has detailed pixel-style forms. The treatment
settles only low-contrast, dark 2 x 2 clusters onto an existing source color:
each channel must span at most 18 levels, and all channels must stay below 150.
High-contrast edges, bright lights, blossoms and fine structure remain untouched.
Environmental lettering, the lower GNUjason interface, the flag fusion and
Liberty silhouette are explicitly protected. There is no resizing, crop,
global posterization, hue remapping, bloom or generic pixelation filter.

The GIF uses a single source-adaptive 248-color scene palette plus reserved
petal colors, without dithering or per-frame palette changes. This is a GIF
format limitation, not the still's color treatment. The 144 frames at 100 ms
make a 14.4-second infinite loop. Twelve staggered petal paths start on visible
blossom branches, with different path lengths/speeds, two pixel scales, lateral
drift and four hand-drawn tumble poses. Petals fade in at the canopy and fade out
before the bottom interface, so the loop does not reset visibly. There is no
full-scene flicker or additional competing animation. The existing `picture`
pattern selects the complete static PNG for reduced-motion users.

Three static derivatives of the original divider contain 7, 3 and 1 petals:
before Operator Log, Project Bays and Open Channel respectively. The other
dividers are unchanged, with no accents added to badges or project cards.
`assets/heritage/opensuse-petal-footer.png` preserves the original openSUSE strip
except for nine dim fallen petals on a small far-right floor segment, away from
the logo and lettering. All original bunker, Charleston, project, divider and
openSUSE assets remain unchanged. Rebuild this derivative after any intentional
change to the original openSUSE strip.

### College of Charleston panorama

The static `assets/cofc/cofc-montage.png` sits between Operator Log and
Project Bays. Rebuild only this asset with the same environment:

```sh
/tmp/gnujason-profile-venv/bin/python scripts/build_cofc.py
```

It uses the hero's 750 x 250 raster enlarged exactly 4x to 3000 x 1000,
shared pixel font, palette, and bloom. Charleston brick piazzas, an oak canopy,
and a Randolph Hall-inspired portico with paired stairs retain their original
geometry. New lower-roofed brick buildings, a garden gate, walkway, benches,
lamps, and a second oak extend the campus across the former workstation area.
There is no person/computer scene, indoor bay, or large HUD panel in this asset;
the bunker connection is expressed through subtle ground circuitry and cyan/
purple environmental lighting. No buildings are stretched to fill the width.
This is a stylized architectural reference, not
an official college logo or seal. Gold is confined to window light, lanterns,
small stone highlights, and indicators; the purple/near-black world remains
dominant. The opaque PNG works on light and dark pages, needs no motion
fallback, and is displayed at full width with proportional height.

The montage has no large college title: its canopy and uninterrupted night sky
flow across the courtyard, without a separate title band. The small academic
line below identifies the college. README sections use invisible explicit anchors within their
content rather than visible heading/icon rows; existing pixel dividers provide
separation without additional heading underlines or spacer containers.

### Project Bays guardians

Two Korean-inspired, stacked architectural guardian totems frame the existing
linked cards on desktop. Rebuild only these assets with:

```sh
/tmp/gnujason-profile-venv/bin/python scripts/build_guardians.py
/tmp/gnujason-profile-venv/bin/python -m unittest discover -s scripts -p 'test_guardians.py' -v
```

The left uses restrained cyan and the right magenta/violet with cyan accents.
Layered rooflines and ornamental brackets flow into stacked carved guardian
forms; traces and nodes emerge as the faces become hardware panels and
mechanical feet. A small blossom branch appears only on the left and tiny
gold fittings echo Charleston.

The renderer draws each complete totem at 50 x 400 and enlarges it exactly 2x.
It builds four 900 x 400 desktop derivatives by appending 100 x 400 slices
beside the original 800 x 400 card pixels without altering those pixels.
Each derivative remains linked to its original project, and the original
card files, links, alt text and order remain unchanged. At the measured
846 px GitHub profile width the 420 px images fit in two columns, displaying
each totem about 47 px wide and each card about 373 px wide (4.3% below its
previous 390 px width). The frame slices themselves are part of the project's
link, not extra projects.

Below 1280 px, the `picture` elements use the original 390 px cards directly,
with no totems, table, forced columns or custom README CSS. Static sources do
not add motion. Renderers without `picture` support retain the original cards.

### Existing artwork

- Hero: 3000 x 1000, a 750 x 250 pixel scene enlarged exactly 4x.
- Animation: 40 frames at 100 ms, four seconds, infinite loop.
- Palette: graphite bunker walls, purple ambient light, cyan and magenta neon.
- Motion: rain, equalizer bars, cursor, server LEDs, CRT flicker, light pulse,
  and restrained pixel noise. No camera shake or full-frame flashing.
- GIF: shared 128-color palette, no dithering, delta-frame optimization.
- Still-image alternatives: README `picture` elements respect reduced motion
  in renderers that support the media query, including modern browsers.
- Cards: 800 x 400 bitmaps displayed at up to 390 px; inline images wrap
  naturally instead of forcing a desktop-width HTML table onto mobile.
- Text equivalents: HTML title, subtitle, biography, stack, and descriptive
  image alt text remain available even when images do not load.

Edit `scripts/build_profile.py` to change the artwork, project card copy,
badges, or palette. Edit `README.md` for biography and destination links.
The project descriptions were checked against public repositories. The
distributed-systems and automation positioning follows the supplied brief;
the README makes no unverified employment or achievement claims.

## Local Preview

```sh
/tmp/gnujason-profile-venv/bin/python scripts/preview_profile.py --port 8765
```

Open <http://localhost:8765>. The preview approximates GitHub Markdown styling;
GitHub's actual rendering remains authoritative. Choose another port if busy.
The preview server binds to loopback and does not publish the profile.

## Publishing

Commit the README, scripts, and newly generated assets, then push to the
`main` branch of `GnuJason/GnuJason` to update the GitHub profile. Existing
unrelated artwork and sprite-engine source files are preserved.

The old Pac-Man graph is deliberately not embedded: its existing workflow
targets `rafife12`, not `GnuJason`. Correct the workflow and regenerate its
data before reintroducing it. The profile links to the real contribution log.