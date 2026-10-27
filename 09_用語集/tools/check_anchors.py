#!/usr/bin/env python3
"""用語集データの src（章へのリンク）のアンカーが実在する見出しを指しているか確認する。"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_cache = {}


def anchors(path):
    """GitHub と同じ規則で見出しのアンカーを作る（小文字化、記号除去、空白→ハイフン、重複は -1, -2）。"""
    if path in _cache:
        return _cache[path]
    seen, out = {}, set()
    text = open(os.path.join(ROOT, path), encoding="utf-8").read()
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    for m in re.finditer(r"^#{1,6}\s+(.+?)\s*#*$", text, flags=re.M):
        h = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", m.group(1))
        h = re.sub(r"[`*_~]|<[^>]+>", "", h).strip().lower()
        a = re.sub(r"[^\w\- ]", "", h).replace(" ", "-")
        n = seen.get(a, 0)
        seen[a] = n + 1
        out.add(a if n == 0 else f"{a}-{n}")
    out.update(re.findall(r'<a (?:id|name)="([^"]+)"', text))
    _cache[path] = out
    return out


def main():
    bad = 0
    for p in sorted(glob.glob(os.path.join(ROOT, "09_用語集", "data", "*.json"))):
        for t in json.load(open(p, encoding="utf-8"))["terms"]:
            src = t.get("src", "")
            if "#" not in src:
                continue
            f, a = src.split("#", 1)
            if a not in anchors(f):
                bad += 1
                print(f"{os.path.basename(p)}: {t['term']} → {src}")
    print("NG" if bad else "OK", bad)


if __name__ == "__main__":
    main()
