"""Keep the header and footer identical across every page.

index.html holds the canonical <header> and <footer>.  Every other page carries
a `<!--HEADER:its-own-filename-->` and `<!--FOOTER-->` marker (or an already
expanded block, which is replaced in place).  Run this after editing the header
or footer in index.html:

    python scripts/sync-chrome.py

The output is plain, complete HTML - this is a maintenance helper, not a build
step, and the committed files are always ready to serve as-is.
"""
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SOURCE = "index.html"

# page file -> the nav href that should carry aria-current="page"
CURRENT = {
    "index.html": "/",
    "b2b.html": "b2b.html",
    "team.html": "team.html",
    "philosophie.html": "philosophie.html",
    "engagement.html": "engagement.html",
    "kontakt.html": "kontakt.html",
    "impressum.html": None,
    "datenschutz.html": None,
    "404.html": None,
}

# 404.html is served from arbitrary URLs, so its links must be absolute
ABSOLUTE = {"404.html"}

HEADER_RE = re.compile(r"<header class=\"site-header\">.*?</header>", re.S)
FOOTER_RE = re.compile(r"<footer class=\"site-footer\">.*?</footer>", re.S)
MARK_HEADER_RE = re.compile(r"<!--HEADER:[^>]*-->|<header class=\"site-header\">.*?</header>", re.S)
MARK_FOOTER_RE = re.compile(r"<!--FOOTER-->|<footer class=\"site-footer\">.*?</footer>", re.S)


def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return f.read()


def write(name, text):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


src = read(SOURCE)
header = HEADER_RE.search(src).group(0)
footer = FOOTER_RE.search(src).group(0)


def personalise(block, page, mark_current=True):
    # move aria-current to this page's own nav entry
    block = block.replace(' aria-current="page"', "")
    target = CURRENT.get(page) if mark_current else None
    if target:
        block = re.sub(
            r'(<a href="%s")' % re.escape(target),
            r'\1 aria-current="page"',
            block,
            count=1,
        )
    if page in ABSOLUTE:
        block = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#|/)', r'\1="/', block)
    return block


changed = 0
for page in CURRENT:
    if page == SOURCE:
        continue
    text = read(page)
    updated = MARK_HEADER_RE.sub(lambda _: personalise(header, page), text, count=1)
    updated = MARK_FOOTER_RE.sub(lambda _: personalise(footer, page, mark_current=False), updated, count=1)
    if updated != text:
        write(page, updated)
        changed += 1
        print("  synced %s" % page)

print("header/footer synced into %d page(s)" % changed)
