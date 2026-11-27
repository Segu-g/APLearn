#!/usr/bin/env python3
"""略語カードのデータ（data/glossary.js）の各語に、解説資料へのリンク ref を付ける。

  1. 用語ドリルのデータ（data/terms.js）に、略語と同じ名前（または英語名）の用語があれば、その用語の解説リンクを使う
  2. なければ、カテゴリに対応する解説資料の中で、その略語が最初に出てくる節の見出しにリンクする
  3. それもなければ、解説資料の先頭にリンクする

ref は「リポジトリのルートからのパス#アンカー」。用語集や解説資料を直したら再実行する。
使い方: python3 06_インタラクティブ教材/tools/link_glossary.py
"""
import json
import os
import re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(HERE)
GLOSSARY_JS = os.path.join(HERE, "data", "glossary.js")
TERMS_JS = os.path.join(HERE, "data", "terms.js")
CHAPTER = {
    "基礎理論・AI": "01_テクノロジ系/01_基礎理論.md",
    "コンピュータ構成要素・ハードウェア": "01_テクノロジ系/03_コンピュータ構成要素.md",
    "システム構成要素・ソフトウェア": "01_テクノロジ系/04_システム構成要素.md",
    "データベース": "01_テクノロジ系/06_データベース.md",
    "ネットワーク": "01_テクノロジ系/07_ネットワーク.md",
    "情報セキュリティ": "01_テクノロジ系/08_情報セキュリティ.md",
    "システム開発技術": "01_テクノロジ系/09_システム開発技術.md",
    "プロジェクトマネジメント": "02_マネジメント系/01_プロジェクトマネジメント.md",
    "サービスマネジメント": "02_マネジメント系/02_サービスマネジメント.md",
    "システム監査・内部統制": "02_マネジメント系/03_システム監査.md",
    "システム戦略・調達": "03_ストラテジ系/01_システム戦略.md",
    "経営戦略・マーケティング": "03_ストラテジ系/02_経営戦略とマーケティング.md",
    "企業活動・会計": "03_ストラテジ系/03_企業活動と会計.md",
    "法務・標準化": "03_ストラテジ系/04_法務.md",
}


def load_js_array(path, start):
    text = open(path, encoding="utf-8").read()
    i = text.index(start) + len(start)
    return text, json.loads(text[i:text.rindex("]") + 1].strip().rstrip(";"))


def slug_headings(md_text):
    """GitHub と同じ規則で見出しのアンカーを作り、(行番号, アンカー) の一覧を返す（コードブロック内は除く）"""
    seen, out, in_code = {}, [], False
    for n, line in enumerate(md_text.split("\n")):
        if line.startswith("```"):
            in_code = not in_code
            continue
        m = None if in_code else re.match(r"^#{1,6}\s+(.+?)\s*#*$", line)
        if not m:
            continue
        h = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", m.group(1))
        h = re.sub(r"[`*_~]|<[^>]+>", "", h).strip().lower()
        a = re.sub(r"[^\w\- ]", "", h).replace(" ", "-")
        k = seen.get(a, 0)
        seen[a] = k + 1
        out.append((n, a if k == 0 else f"{a}-{k}"))
    return out


def parts(abbr):
    """'PL / P/L' → ['PL', 'P/L']、'SLA（契約）' → ['SLA']"""
    abbr = re.sub(r"（.*?）", "", abbr)
    return [p.strip() for p in re.split(r"\s+/\s+", abbr) if p.strip()]


def token_re(word):
    return re.compile(r"(?<![A-Za-z0-9])" + re.escape(word) + r"(?![A-Za-z0-9])")


def main():
    text = open(TERMS_JS, encoding="utf-8").read()
    data = json.loads(text[text.index("{"):text.rindex("}") + 1])
    terms = [t for t in data["terms"] if t.get("r")]
    by_name = {}
    for t in terms:
        for key in [t["t"], re.sub(r"（.*?）", "", t["t"]), t.get("e", "")]:
            for p in re.split(r"[／/]", key) if "／" in key else [key]:
                p = p.strip()
                if p and p not in by_name:
                    by_name[p] = t["r"]

    src, gl = load_js_array(GLOSSARY_JS, "window.APL_DATA_GLOSSARY =")
    chapters = {}
    stats = {"用語": 0, "節": 0, "章": 0}
    for g in gl:
        ref = next((by_name[p] for p in parts(g["abbr"]) if p in by_name), None)
        if ref:
            stats["用語"] += 1
        else:
            path = CHAPTER[g["category"]]
            if path not in chapters:
                md = open(os.path.join(ROOT, path), encoding="utf-8").read()
                chapters[path] = (md.split("\n"), slug_headings(md))
            lines, heads = chapters[path]
            # 目次の節（「## 目次」から次の見出しまで）はリンクの一覧なので探さない
            toc = next((i for i, (n, a) in enumerate(heads) if a == "目次"), None)
            body_from = heads[toc + 1][0] if toc is not None and toc + 1 < len(heads) else 0
            hit = None
            for p in parts(g["abbr"]):
                r = token_re(p)
                hit = next((n for n, line in enumerate(lines) if n >= body_from and r.search(line)), None)
                if hit is not None:
                    break
            anchor = next((a for n, a in reversed(heads) if hit is not None and n <= hit), None)
            ref = f"{path}#{anchor}" if anchor else path
            stats["節" if anchor else "章"] += 1
        g["ref"] = ref

    head = src[:src.index("window.APL_DATA_GLOSSARY =")]
    head = head.replace("形式: { abbr, full, meaning, category }", "形式: { abbr, full, meaning, category, ref }\n"
                        " * ref（解説資料へのリンク）は tools/link_glossary.py が付ける。") \
        if "ref }" not in head else head
    body = ",\n".join("  " + json.dumps(g, ensure_ascii=False) for g in gl)
    with open(GLOSSARY_JS, "w", encoding="utf-8") as f:
        f.write(head + "window.APL_DATA_GLOSSARY = [\n" + body + "\n];\n")
    print(f"{len(gl)}語に ref を付けました（用語の解説 {stats['用語']}・章内の節 {stats['節']}・章の先頭 {stats['章']}）")


if __name__ == "__main__":
    main()
