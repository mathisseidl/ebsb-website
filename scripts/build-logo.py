"""Turn the flat white-background EBSB logo into transparent PNGs.

Produces the full stacked lockup plus the mark and wordmark on their own, so a
slim header can set them side by side.  Also emits the favicon sizes.
"""
import os
from PIL import Image

RAW = ".raw/40a34f_3ae1a03bd1f7451192c2097e52c8b3c4_mv2.jpg"
OUT = "assets/img"

im = Image.open(RAW).convert("RGB")
px = im.load()
w, h = im.size

# knock out the white ground -> alpha
rgba = Image.new("RGBA", (w, h))
out = rgba.load()
for y in range(h):
    for x in range(w):
        r, g, b = px[x, y]
        m = max(r, g, b)
        if m > 244 and (m - min(r, g, b)) < 12:      # near-white, near-grey
            out[x, y] = (255, 255, 255, 0)
        else:
            out[x, y] = (r, g, b, 255)
rgba = rgba.crop(rgba.getbbox())
print("trimmed:", rgba.size)

# find the blank band between the mark and the EBSB wordmark
alpha = rgba.split()[-1]
rows = [alpha.crop((0, y, rgba.width, y + 1)).getbbox() is None for y in range(rgba.height)]
gaps, run = [], None
for y, blank in enumerate(rows):
    if blank and run is None:
        run = y
    elif not blank and run is not None:
        gaps.append((run, y)); run = None
gaps = [g for g in gaps if g[1] - g[0] > 4]
split = sum(gaps[-1]) // 2 if gaps else int(rgba.height * 0.68)
print("gaps:", gaps, "-> split at", split)

def save(im, stem, width):
    im = im.crop(im.getbbox())
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    # PNG only: these are flat-colour marks, where PNG beats WebP and the
    # extra <picture> plumbing is not worth it.
    im.save(os.path.join(OUT, stem + ".png"), "PNG", optimize=True)
    print("  %-18s %dx%d" % (stem, im.width, im.height))

save(rgba, "logo-ebsb", 900)
save(rgba.crop((0, 0, rgba.width, split)), "logo-mark", 400)
save(rgba.crop((0, split, rgba.width, rgba.height)), "logo-wordmark", 500)

# favicon / touch icon: the mark, padded square on white
mark = Image.open(os.path.join(OUT, "logo-mark.png"))
for size, name, bg in ((180, "apple-touch-icon.png", (255, 255, 255, 255)),):
    pad = round(size * 0.12)
    box = size - 2 * pad
    m = mark.copy()
    m.thumbnail((box, box), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), bg)
    canvas.paste(m, ((size - m.width) // 2, (size - m.height) // 2), m)
    canvas.save(name, "PNG", optimize=True)
    print("  %-18s %dx%d" % (name, size, size))
