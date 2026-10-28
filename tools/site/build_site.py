#!/usr/bin/env python3
"""GitHub Pages 用の静的サイトを _site/ に生成する。

- git 管理下の Markdown をすべて HTML に変換（X.md → X.html、README.md は index.html も作る）
- それ以外のファイル（インタラクティブ教材の HTML・JS、MP3、画像など）はそのままコピー
- 見出しのアンカーは GitHub と同じ規則で付けるので、既存の「X.md#見出し」リンクがそのまま使える
- Mermaid の図はブラウザ側で描画（CDN の mermaid を読み込む）

使い方:
    python3 tools/site/build_site.py            # _site/ に生成
    python3 tools/site/build_site.py --check    # 生成後、サイト内リンク切れを検査
"""
import argparse
import html
import os
import re
import shutil
import subprocess
import sys
from urllib.parse import unquote

from markdown_it import MarkdownIt

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = "_site_assets"
SITE_NAME = "APLearn 応用情報技術者試験"
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs"

md = MarkdownIt("gfm-like", {"html": True, "typographer": False})


def tracked_files():
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
    files = [f for f in out.decode("utf-8").split("\0") if f]
    return [f for f in files if not any(p.startswith(".") for p in f.split("/")) and os.path.isfile(os.path.join(ROOT, f))]


def slug(text, seen):
    """GitHub と同じ規則（09_用語集/tools/check_anchors.py と同じ）。"""
    h = re.sub(r"[`*_~]|<[^>]+>", "", text).strip().lower()
    a = re.sub(r"[^\w\- ]", "", h).replace(" ", "-")
    n = seen.get(a, 0)
    seen[a] = n + 1
    return a if n == 0 else f"{a}-{n}"


def inline_text(token):
    parts = []
    for c in token.children or []:
        if c.type in ("text", "code_inline"):
            parts.append(c.content)
    return "".join(parts)


def rel_root(path):
    depth = path.count("/")
    return "../" * depth if depth else "./"


MD_LINK = re.compile(r'(href)="(?![a-zA-Z][a-zA-Z0-9+.-]*:|//|#)([^"#]*?)\.md((?:#[^"]*)?)"')


def fix_md_links(text):
    return MD_LINK.sub(lambda m: f'{m.group(1)}="{m.group(2)}.html{m.group(3)}"', text)


def render_md(src):
    tokens = md.parse(src)
    seen, title = {}, None
    for i, t in enumerate(tokens):
        if t.type == "heading_open":
            text = inline_text(tokens[i + 1])
            t.attrSet("id", slug(text, seen))
            if title is None and t.tag == "h1":
                title = text.strip()
        elif t.type == "fence" and t.info.strip() == "mermaid":
            t.type = "html_block"
            t.content = '<pre class="mermaid">' + html.escape(t.content) + "</pre>\n"
    body = md.renderer.render(tokens, md.options, {})
    body = re.sub(r"<li>(<p>)?\[([ xX])\] ", lambda m: '<li class="task">' + (m.group(1) or "")
                  + '<input type="checkbox" disabled' + (" checked" if m.group(2) != " " else "") + "> ", body)
    body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    return body, title


def page(path, title, body, has_mermaid):
    root = rel_root(path)
    crumbs = []
    parts = path.split("/")[:-1]
    for i, p in enumerate(parts):
        crumbs.append(f'<a href="{"../" * (len(parts) - i - 1) or "./"}index.html">{html.escape(p)}</a>')
    crumb_html = ' <span aria-hidden="true">/</span> '.join(crumbs)
    mermaid = ""
    if has_mermaid:
        mermaid = f"""<script type="module">
import mermaid from "{MERMAID}";
const dark = matchMedia("(prefers-color-scheme: dark)").matches;
mermaid.initialize({{ startOnLoad: false, theme: dark ? "dark" : "default" }});
await mermaid.run({{ querySelector: "pre.mermaid" }});
</script>"""
    full_title = f"{title} | {SITE_NAME}" if title else SITE_NAME
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<link rel="stylesheet" href="{root}{ASSET_DIR}/site.css">
</head>
<body>
<header class="site-header">
  <a class="site-name" href="{root}index.html">APLearn</a>
  <nav><a href="{root}06_インタラクティブ教材/index.html">インタラクティブ教材</a><a href="{root}09_用語集/index.html">用語集</a><a href="{root}08_過去問解説/index.html">過去問解説</a></nav>
</header>
{f'<div class="crumbs">{crumb_html}</div>' if crumb_html else ''}
<main class="markdown-body">
{body}
</main>
<footer class="site-footer">応用情報技術者試験 学習資料 APLearn ／ 過去問題の著作権は IPA（独立行政法人 情報処理推進機構）にあります ／ 音声合成：VOICEVOX:四国めたん、VOICEVOX:ずんだもん、VOICEVOX:春日部つむぎ、VOICEVOX:冥鳴ひまり</footer>
{mermaid}
</body>
</html>
"""


def dir_index(d, entries):
    rows = []
    for name, is_dir in sorted(entries, key=lambda e: (not e[1], e[0])):
        if is_dir:
            rows.append(f'<li>📁 <a href="{html.escape(name)}/index.html">{html.escape(name)}/</a></li>')
        else:
            target = name[:-3] + ".html" if name.endswith(".md") else name
            rows.append(f'<li><a href="{html.escape(target)}">{html.escape(name)}</a></li>')
    title = d.split("/")[-1]
    return page(d + "/index.html", title, f"<h1>{html.escape(title)}</h1>\n<ul class=\"dir-list\">\n" + "\n".join(rows) + "\n</ul>", False)


def build(out):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    files = tracked_files()
    written, generated = set(), set()
    tracked = set(files)

    def write(rel, text):
        p = os.path.join(out, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        written.add(rel)
        if rel.endswith(".html") and rel not in tracked:
            generated.add(rel)

    for f in files:
        src = os.path.join(ROOT, f)
        if f.endswith(".md"):
            body, title = render_md(open(src, encoding="utf-8").read())
            body = fix_md_links(body)
            text = page(f, title or os.path.basename(f)[:-3], body, 'class="mermaid"' in body)
            write(f[:-3] + ".html", text)
            d = os.path.dirname(f)
            if os.path.basename(f) == "README.md" and os.path.join(d, "index.html").lstrip("/") not in tracked:
                write(os.path.join(d, "index.html").lstrip("/"), text)
        elif f.endswith(".html"):
            text = fix_md_links(open(src, encoding="utf-8").read())
            text = text.replace("</body>", f'<script src="{rel_root(f)}{ASSET_DIR}/mdlinks.js"></script>\n</body>', 1)
            write(f, text)
        else:
            dst = os.path.join(out, f)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
            written.add(f)

    # README も index.html も無いフォルダには一覧ページを作る
    dirs = {}
    for f in written:
        parts = f.split("/")
        for i in range(1, len(parts)):
            d = "/".join(parts[:i])
            dirs.setdefault(d, set())
            child = parts[i]
            dirs[d].add((child, i < len(parts) - 1))
    for d, entries in dirs.items():
        if f"{d}/index.html" not in written:
            src_entries = set()
            for name, is_dir in entries:
                if not is_dir and name.endswith(".html") and f"{d}/{name[:-5]}.md" in tracked:
                    name = name[:-5] + ".md"
                src_entries.add((name, is_dir))
            write(f"{d}/index.html", dir_index(d, src_entries))

    os.makedirs(os.path.join(out, ASSET_DIR), exist_ok=True)
    for a in ("site.css", "mdlinks.js"):
        shutil.copyfile(os.path.join(HERE, a), os.path.join(out, ASSET_DIR, a))
    open(os.path.join(out, ".nojekyll"), "w").close()
    return written, generated


def check(out, generated):
    """サイト内の相対リンク（href/src）が存在するファイル・アンカーを指しているか検査する。
    アンカーは Markdown から生成したページだけ確かめる（教材 HTML の #past などは画面切替用のハッシュ）。"""
    ids = {}

    def ids_of(rel):
        if rel not in ids:
            text = open(os.path.join(out, rel), encoding="utf-8").read()
            ids[rel] = set(re.findall(r'\b(?:id|name)="([^"]+)"', text))
        return ids[rel]

    bad = 0
    for dp, _, fs in os.walk(out):
        for fn in fs:
            if not fn.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(dp, fn), out).replace(os.sep, "/")
            text = open(os.path.join(dp, fn), encoding="utf-8").read()
            for url in re.findall(r'\b(?:href|src)="([^"]+)"', text):
                url = html.unescape(url)
                if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:|//", url) or "'" in url or "+" in url and "%" not in url:
                    continue
                path, _, frag = url.partition("#")
                path = unquote(path.split("?")[0])
                target = os.path.normpath(os.path.join(os.path.dirname(rel), path)).replace(os.sep, "/") if path else rel
                if path.endswith("/") or os.path.isdir(os.path.join(out, target)):
                    target = target.rstrip("/") + "/index.html"
                if not os.path.isfile(os.path.join(out, target)):
                    bad += 1
                    print(f"NG {rel}: {url}")
                elif frag and target in generated and unquote(frag) not in ids_of(target):
                    bad += 1
                    print(f"NG #{rel}: {url}")
    print("リンク検査:", "OK" if bad == 0 else f"{bad} 件のリンク切れ")
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "_site"))
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    written, generated = build(a.out)
    print(f"{len(written)} ファイルを {a.out} に出力")
    if a.check and check(a.out, generated):
        sys.exit(1)


if __name__ == "__main__":
    main()
