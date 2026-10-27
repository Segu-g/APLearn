#!/usr/bin/env python3
"""各章末の「📋 シラバス用語チェックリスト」から用語を抜き出し、09_用語集/data/NN_<中分類>.json の初版を作る（初回だけ使う）。

使い方: python3 09_用語集/tools/extract_from_chapters.py [--force]
既存の data/*.json があるときは、--force を付けない限り上書きしない。
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "09_用語集", "data")

# シラバス Ver.7.2 の中分類（番号, 名前, 分野）
CATEGORIES = [
    (1, "基礎理論", "tech"), (2, "アルゴリズムとプログラミング", "tech"), (3, "コンピュータ構成要素", "tech"),
    (4, "システム構成要素", "tech"), (5, "ソフトウェア", "tech"), (6, "ハードウェア", "tech"),
    (7, "ユーザーインタフェース", "tech"), (8, "情報メディア", "tech"), (9, "データベース", "tech"),
    (10, "ネットワーク", "tech"), (11, "セキュリティ", "tech"), (12, "システム開発技術", "tech"),
    (13, "ソフトウェア開発管理技術", "tech"), (14, "プロジェクトマネジメント", "mgmt"),
    (15, "サービスマネジメント", "mgmt"), (16, "システム監査", "mgmt"), (17, "システム戦略", "strat"),
    (18, "システム企画", "strat"), (19, "経営戦略マネジメント", "strat"), (20, "技術戦略マネジメント", "strat"),
    (21, "ビジネスインダストリ", "strat"), (22, "企業活動", "strat"), (23, "法務", "strat"),
]

# 章ファイル → 中分類番号（見出しで振り分ける章は関数）
CHAPTERS = {
    "01_テクノロジ系/01_基礎理論.md": 1,
    "01_テクノロジ系/02_アルゴリズムとプログラミング.md": 2,
    "01_テクノロジ系/03_コンピュータ構成要素.md": 3,
    "01_テクノロジ系/04_システム構成要素.md": 4,
    "01_テクノロジ系/05_ソフトウェア.md": 5,
    "01_テクノロジ系/06_データベース.md": 9,
    "01_テクノロジ系/07_ネットワーク.md": 10,
    "01_テクノロジ系/08_情報セキュリティ.md": 11,
    "01_テクノロジ系/09_システム開発技術.md": 12,
    "01_テクノロジ系/10_ハードウェア.md": 6,
    "01_テクノロジ系/11_ユーザーインタフェースと情報メディア.md": lambda h: 8 if h.startswith("中分類8") else 7,
    "01_テクノロジ系/12_ソフトウェア開発管理技術.md": 13,
    "02_マネジメント系/01_プロジェクトマネジメント.md": 14,
    "02_マネジメント系/02_サービスマネジメント.md": 15,
    "02_マネジメント系/03_システム監査.md": 16,
    "03_ストラテジ系/01_システム戦略.md": lambda h: 18 if h.startswith("中分類18") else 17,
    "03_ストラテジ系/02_経営戦略とマーケティング.md": 19,
    "03_ストラテジ系/03_企業活動と会計.md": 22,
    "03_ストラテジ系/04_法務.md": 23,
    "03_ストラテジ系/05_技術戦略とビジネスインダストリ.md": lambda h: 21 if h.startswith("中分類21") else 20,
    "03_ストラテジ系/06_業務分析とデータ利活用.md": 22,
}

LINK = re.compile(r"\[([^\]]+)\]\(([^)]*)\)")


def clean_sub(h):
    h = re.sub(r"^中分類\d+(-[\d()（）〜]+)*\.?\s*", "", h)
    h = re.sub(r"^\d+\.\s*", "", h)
    return h.strip()


def main():
    force = "--force" in sys.argv
    out = {n: [] for n, _, _ in CATEGORIES}
    for rel, cat in CHAPTERS.items():
        text = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        i = text.find("## 📋 シラバス用語チェックリスト")
        sec = text[i:]
        j = sec.find("\n## ", 5)
        if j > 0:
            sec = sec[:j]
        head = ""
        for line in sec.splitlines():
            if line.startswith("### "):
                head = line[4:].strip()
                continue
            if not line.startswith("| ") or line.startswith("| 用語") or line.startswith("|---"):
                continue
            cells = [c.strip().replace("\\|", "｜") for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
            if len(cells) < 2 or not cells[1]:
                continue
            m = LINK.search(cells[0])
            term = LINK.sub(r"\1", cells[0]).strip()
            anchor = m.group(2) if m else ""
            n = cat(head) if callable(cat) else cat
            out[n].append({
                "term": term,
                "desc": cells[1],
                "sub": clean_sub(head),
                "src": rel + (anchor if anchor.startswith("#") else ""),
            })
    os.makedirs(DATA, exist_ok=True)
    for n, name, field in CATEGORIES:
        path = os.path.join(DATA, f"{n:02d}_{name}.json")
        if os.path.exists(path) and not force:
            print("skip", path)
            continue
        seen, terms = set(), []
        for t in out[n]:
            if t["term"] in seen:
                continue
            seen.add(t["term"])
            terms.append(t)
        doc = {"no": n, "category": name, "field": field, "pairs": [], "terms": terms}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print(f"{n:02d} {name}: {len(terms)}語")


if __name__ == "__main__":
    main()
