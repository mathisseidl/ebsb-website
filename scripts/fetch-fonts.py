"""Self-host Inter + Manrope (latin + latin-ext) so no visitor request ever
reaches fonts.googleapis.com / fonts.gstatic.com.  DSGVO: no consent needed.

Writes assets/fonts/*.woff2 and assets/css/fonts.css.
"""
import os, re, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
API = ("https://fonts.googleapis.com/css2?family=Inter:wght@400..700"
       "&family=Manrope:wght@600..800&display=swap")
KEEP = ("latin", "latin-ext")
FONTDIR = "assets/fonts"


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA)).read()


os.makedirs(FONTDIR, exist_ok=True)
css = get(API).decode("utf-8")

blocks = re.findall(r"/\* ([\w-]+) \*/\s*(@font-face \{.*?\})", css, re.S)
seen, rules = {}, []
for subset, block in blocks:
    if subset not in KEEP:
        continue
    fam = re.search(r"font-family: '([^']+)'", block).group(1)
    url = re.search(r"src: url\(([^)]+)\)", block).group(1)
    rng = re.search(r"unicode-range: ([^;]+);", block).group(1)
    name = "%s-%s.woff2" % (fam.lower(), subset)
    if url not in seen:
        with open(os.path.join(FONTDIR, name), "wb") as f:
            f.write(get(url))
        seen[url] = name
        print("  %-24s %6.1f KB" % (name, os.path.getsize(os.path.join(FONTDIR, name)) / 1024))
    rules.append((fam, seen[url], rng))

lines = ["/* Self-hosted variable fonts. Regenerate with scripts/fetch-fonts.py.",
         "   Never link fonts.googleapis.com directly - it sends visitor IPs to Google",
         "   and is a DSGVO problem for a German site. */", ""]
for fam, name, rng in rules:
    lines += ["@font-face {",
              "  font-family: '%s';" % fam,
              "  font-style: normal;",
              "  font-weight: %s;" % ("400 700" if fam == "Inter" else "600 800"),
              "  font-display: swap;",
              "  src: url('../fonts/%s') format('woff2');" % name,
              "  unicode-range: %s;" % rng,
              "}", ""]
open("assets/css/fonts.css", "w", encoding="utf-8").write("\n".join(lines))
print("wrote assets/css/fonts.css (%d faces)" % len(rules))
