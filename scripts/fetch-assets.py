"""One-off: pull every image off static.wixstatic.com into assets/img/.

Downloads the untouched originals, then writes web-sized WebP with a
JPEG/PNG fallback next to it. Re-runnable; skips what already exists.
"""
import io, os, sys, urllib.request
from PIL import Image

BASE = "https://static.wixstatic.com/media/"
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
RAW = os.path.join(os.path.dirname(__file__), "..", ".raw")

# name -> (wix id, crop box or None, target width)
SHOTS = {
    "logo-ebsb":            ("40a34f_3ae1a03bd1f7451192c2097e52c8b3c4~mv2.jpg", None, 900),
    "logo-google":          ("40a34f_b9f83f367b0043c4bacb149e23c2ab2f~mv2.png", None, 96),
    "service-foerderung":   ("eb1f19_c3e835ef60b241e6877ad91394153c07~mv2.png", None, 900),
    "service-technologie":  ("eb1f19_57359e716025454497849239349c7c7a~mv2.png", None, 900),
    "service-energie":      ("eb1f19_3958765ffbff4ee8abbc70c47a66c04d~mv2.png", None, 900),
    "b2b-energiewirtschaft":                ("eb1f19_34a2b5d33b9741ae96b7b70577eb7557~mv2.png", None, 900),
    "b2b-elektromobilitaet":                ("eb1f19_3400043426e146d1b15abff7c41a0ee9~mv2.png", None, 900),
    # the only landscape shot of the six service images - cropped to the same
    # portrait proportions as its siblings so the card grid stays even
    "b2b-anlagenbetrieb":                ("eb1f19_57562a0f6f9f4615a1903eb2c17bb236~mv2.png", (222, 0, 939, 896), 900),
    # one sprite sheet holding the three "3 Schritte" comic panels
    "step-1":               ("eb1f19_f3165b19e99746d1b92589c7f598d5d4~mv2.png", (62, 21, 458, 766), 520),
    "step-2":               ("eb1f19_f3165b19e99746d1b92589c7f598d5d4~mv2.png", (467, 30, 850, 766), 520),
    "step-3":               ("eb1f19_f3165b19e99746d1b92589c7f598d5d4~mv2.png", (856, 21, 1256, 766), 520),
    "engagement-tsv-gruenwald":       ("40a34f_30a83738a11b4ee68dd2ddedd97362f1~mv2.jpeg", None, 1000),
    "engagement-sv-strasslach":  ("40a34f_09348c31b0214c96a0a97436249196cf~mv2.jpeg", None, 1000),
    "engagement-special-olympics":  ("40a34f_54a03e7a35fe4a40903640014b9ec509~mv2.jpeg", None, 1000),
    "logo-tsv-gruenwald":   ("eb1f19_2513afbeb63b408f98a7769c4363c638~mv2.png", (235, 106, 647, 509), 400),
}

# the twelve team portraits, in the order the names appear on the Wix page
TEAM = [
    "eb1f19_d91d60791f134195a1a3e8609de9bc15~mv2.jpg",
    "eb1f19_5845a380b1e34c56affba282195e9e69~mv2.jpg",
    "eb1f19_879d8dbf8f924d50ae421790c9b1b079~mv2.jpg",
    "eb1f19_a7c876eafdc5499aa7e1b53434e4ba11~mv2.jpg",
    "eb1f19_f3b48ce16a804d4ab7ad66d57ef2e338~mv2.jpg",
    "eb1f19_78675c58074245deb20e74c1cb94b509~mv2.jpg",
    "eb1f19_3ad6108986304efb97184fa2f847a831~mv2.jpg",
    "eb1f19_a231fab055e142fda03f7f6288dae0a2~mv2.jpg",
    "eb1f19_a40d1539cdd948258a403e4be47691cd~mv2.jpg",
    "eb1f19_86f16a8bd4854b3bbce984c3845b7bb6~mv2.jpg",
    "eb1f19_a262ba5db8524947bfc980441c18dbce~mv2.jpg",
    "eb1f19_4c58f87e6b184ad3956369c83ef0457f~mv2.jpg",
]


def grab(wix_id):
    os.makedirs(RAW, exist_ok=True)
    cached = os.path.join(RAW, wix_id.replace("~", "_"))
    if not os.path.exists(cached):
        req = urllib.request.Request(BASE + wix_id, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as r, open(cached, "wb") as f:
            f.write(r.read())
    return Image.open(cached)


# Photos / comic panels: no meaningful transparency and they render on white,
# so a JPEG fallback beats a ~1.4 MB PNG.
FORCE_JPEG = {"b2b-anlagenbetrieb", "b2b-elektromobilitaet", "b2b-energiewirtschaft",
              "service-energie", "service-foerderung", "service-technologie",
              "step-1", "step-2", "step-3"}


# The six service illustrations sit in identically sized card media boxes, so
# they are normalised to one portrait ratio and one pixel size.  Left at their
# native proportions (0.60 to 0.80) each photo rendered at a different size.
CARD_STEMS = {"service-foerderung", "service-technologie", "service-energie",
              "b2b-energiewirtschaft", "b2b-elektromobilitaet", "b2b-anlagenbetrieb"}
CARD_SIZE = (800, 1067)


def to_card(im):
    target = CARD_SIZE[0] / CARD_SIZE[1]
    w, h = im.size
    if w / h > target:                    # too wide - trim the sides
        nw = round(h * target)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:                                 # too tall - trim top and bottom
        nh = round(w / target)
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return im.resize(CARD_SIZE, Image.LANCZOS)


def write(im, stem, width, subdir=""):
    dest = os.path.join(OUT, subdir)
    os.makedirs(dest, exist_ok=True)
    if stem in CARD_STEMS:
        im = to_card(im)
    elif im.width > width:
        h = round(im.height * width / im.width)
        im = im.resize((width, h), Image.LANCZOS)
    alpha = (im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info))         and stem not in FORCE_JPEG
    if stem in FORCE_JPEG and im.mode in ("RGBA", "LA"):
        flat = Image.new("RGB", im.size, (255, 255, 255))
        flat.paste(im, mask=im.split()[-1])
        im = flat
    im.save(os.path.join(dest, stem + ".webp"), "WEBP", quality=86, method=6)
    if alpha:
        im.convert("RGBA").save(os.path.join(dest, stem + ".png"), "PNG", optimize=True)
        ext = "png"
    else:
        im.convert("RGB").save(os.path.join(dest, stem + ".jpg"), "JPEG", quality=86, optimize=True, progressive=True)
        ext = "jpg"
    print("  %-24s %4dx%-4d  webp+%s" % (stem, im.width, im.height, ext))


print("assets:")
for stem, (wix_id, box, width) in SHOTS.items():
    im = grab(wix_id)
    if box:
        im = im.crop(box)
    write(im, stem, width)

print("team portraits:")
for i, wix_id in enumerate(TEAM, 1):
    write(grab(wix_id), "person-%02d" % i, 620, subdir="team")
