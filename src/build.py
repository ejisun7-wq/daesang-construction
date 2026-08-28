#!/usr/bin/env python3
"""
Build the 대상종합공사 landing page.

Source of truth is src/template.html, which references photos as {{img:name}}.
Two outputs are produced from it:

  index.html        deployed site — photos load from /img/<name>.jpg
  dist/single.html  one self-contained file with every photo inlined as a
                    data: URI (for the Claude artifact, email, or a USB stick)

Run from anywhere:  python src/build.py
"""

import base64
import mimetypes
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "src", "template.html")
IMG_DIR = os.path.join(ROOT, "img")

HEAD = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>대상종합공사 | 대전·충청 우수관·트렌치·렉산·방수 시공</title>
<meta name="description" content="대전·세종·충청 전역 출동. 우수관·빗물받이, 트렌치 배수로, 렉산 캐노피, 옥상방수, 동파방지 열선, 태양광 가로등, 벌목까지 한 팀이 시공합니다. 대상종합공사 010-3996-6004">
<meta name="theme-color" content="#08182D">
<link rel="canonical" href="{site}/">
<meta property="og:type" content="website">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="대상종합공사">
<meta property="og:title" content="대상종합공사 | 현장을 이해하는 시공, 오래가는 마감">
<meta property="og:description" content="300건 이상의 시공 기록, 36개 시·군·구 출동. 사진 한 장 보내주시면 작업 범위를 안내해 드립니다.">
<meta property="og:url" content="{site}/">
<meta property="og:image" content="{site}/img/hero_rope.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%2308182D'/%3E%3Cg fill='none' stroke='%234A7CCF' stroke-width='2.6'%3E%3Cpath d='M9.5 7v13.2a6.5 6.5 0 0 0 13 0V7' stroke-linecap='square'/%3E%3Cpath d='M16 24.4V28'/%3E%3C/g%3E%3C/svg%3E">
"""


def read_template():
    with open(TEMPLATE, encoding="utf-8") as f:
        return f.read()


def wrap(body_and_style, site_url):
    """Split the template at </style> so the CSS lands in <head>."""
    cut = body_and_style.index("</style>") + len("</style>")
    head_css, body = body_and_style[:cut], body_and_style[cut:]
    # the template carries its own <title> for the artifact host; drop it here
    head_css = re.sub(r"<title>.*?</title>\s*", "", head_css, count=1, flags=re.S)
    return HEAD.format(site=site_url) + head_css + "\n</head>\n<body>\n" + body + "\n</body>\n</html>\n"


def build_site(tpl, site_url):
    missing = []

    def sub(m):
        name = m.group(1)
        if not os.path.exists(os.path.join(IMG_DIR, name + ".jpg")):
            missing.append(name)
        return "img/%s.jpg" % name

    html = re.sub(r"\{\{img:([a-z0-9_]+)\}\}", sub, tpl)
    if missing:
        sys.exit("missing images: %s" % sorted(set(missing)))
    out = os.path.join(ROOT, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(wrap(html, site_url))
    return out


def build_single(tpl, site_url):
    cache = {}

    def sub(m):
        name = m.group(1)
        if name not in cache:
            path = os.path.join(IMG_DIR, name + ".jpg")
            mime = mimetypes.guess_type(path)[0] or "image/jpeg"
            with open(path, "rb") as f:
                cache[name] = "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode())
        return cache[name]

    html = re.sub(r"\{\{img:([a-z0-9_]+)\}\}", sub, tpl)
    os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
    out = os.path.join(ROOT, "dist", "single.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(wrap(html, site_url))
    return out


def main():
    site_url = os.environ.get("SITE_URL", "https://daesang-construction.vercel.app").rstrip("/")
    tpl = read_template()
    for path in (build_site(tpl, site_url), build_single(tpl, site_url)):
        size = os.path.getsize(path) / 1024
        print("%-40s %8.0f KB" % (os.path.relpath(path, ROOT).replace("\\", "/"), size))


if __name__ == "__main__":
    main()
