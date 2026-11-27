#!/usr/bin/env python3
"""IPA の過去問題ページから、応用情報技術者試験（AP）の PDF の URL を集めて ipa_pdfs.json に書く。

新しい回が公表されたときだけ手で実行する（ネットワークが必要）。サイト生成や build_past.py は
ネットワークを使わず、ここで作った ipa_pdfs.json だけを読む。

使い方: python3 tools/fetch_ipa_pdfs.py
"""
import json
import os
import re
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "ipa_pdfs.json")
SITE = "https://www.ipa.go.jp"
INDEX = SITE + "/shiken/mondai-kaiotu/index.html"
KINDS = {"am_qs", "am_ans", "pm_qs", "pm_ans", "pm_cmnt"}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (study-notes link collector)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def label(exam_id):
    """'2025r07a' → '令和7年度秋期'、'2019r01a' → '令和元年度秋期'、'2011h23tokubetsu' → '平成23年度特別試験'"""
    m = re.match(r"\d{4}([hr])(\d\d)(h|a|o|tokubetsu)$", exam_id)
    era = "平成" if m.group(1) == "h" else "令和"
    n = int(m.group(2))
    year = f"{era}{'元' if n == 1 else n}年度"
    return year + {"h": "春期", "a": "秋期", "o": "10月", "tokubetsu": "特別試験"}[m.group(3)]


def main():
    pages = sorted(set(re.findall(r'href="(/shiken/mondai-kaiotu/\d{4}[hr]\d\d\.html)"', get(INDEX))))
    exams = {}
    for page in pages:
        html = get(SITE + page)
        for href in re.findall(r'href="([^"]+_ap_[a-z]+_[a-z]+\.pdf)"', html):
            m = re.search(r"/(\d{4}[hr]\d\d(?:h|a|o|tokubetsu))_ap_([a-z]+_[a-z]+)\.pdf$", href)
            if not m or m.group(2) not in KINDS:
                continue
            ex = exams.setdefault(m.group(1), {"id": m.group(1), "label": label(m.group(1)), "page": SITE + page})
            ex[m.group(2)] = href if href.startswith("http") else SITE + href
    order = {"h": 0, "tokubetsu": 1, "o": 1, "a": 2}
    items = sorted(exams.values(), key=lambda e: (e["id"][:4], order[re.sub(r"^\d{4}[hr]\d\d", "", e["id"])]),
                   reverse=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)
        f.write("\n")
    missing = [(e["id"], sorted(KINDS - set(e))) for e in items if KINDS - set(e)]
    print(f"{len(items)}回分を {OUT} に書きました。欠けている PDF：{missing or 'なし'}")


if __name__ == "__main__":
    main()
