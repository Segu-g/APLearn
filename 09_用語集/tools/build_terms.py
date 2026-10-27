#!/usr/bin/env python3
"""用語集データ（09_用語集/data/*.json）から Markdown と用語ドリル用データを生成する。

生成物:
  09_用語集/NN_<中分類>.md          … 中分類ごとの用語集
  09_用語集/00_最重要用語まとめ.md   … 全分野の★★★だけを集めた直前用の一覧
  09_用語集/README.md                … 目次と使い方
  06_インタラクティブ教材/data/terms.js … 用語ドリル（terms.html）用

使い方: python3 09_用語集/tools/build_terms.py
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.join(ROOT, "09_用語集")
DATA = os.path.join(BASE, "data")
KEYS = os.path.join(ROOT, "08_過去問解説", "科目A", "answer_keys.json")
TERMS_JS = os.path.join(ROOT, "06_インタラクティブ教材", "data", "terms.js")

FIELDS = {"tech": "テクノロジ系", "mgmt": "マネジメント系", "strat": "ストラテジ系"}
STARS = {3: "★★★", 2: "★★", 1: "★"}


def load():
    cats = []
    for path in sorted(glob.glob(os.path.join(DATA, "*.json"))):
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        d["file"] = os.path.splitext(os.path.basename(path))[0] + ".md"
        cats.append(d)
    return cats


def short_label(label):
    """'令和6年度春期' → 'R6春'、'平成31年度春期' → 'H31春'、'令和2年度10月' → 'R2秋'"""
    m = re.match(r"(令和|平成)(元|\d+)年度(春期|秋期|10月)", label)
    era = "R" if m.group(1) == "令和" else "H"
    year = "1" if m.group(2) == "元" else m.group(2)
    season = {"春期": "春", "秋期": "秋", "10月": "秋"}[m.group(3)]
    return f"{era}{year}{season}"


def past_order(p):
    """新しい順に並べるためのキー。'2025r07a-12' → (2025, 1, 12)（同じ年度は秋が春より新しい）"""
    sid, no = p.rsplit("-", 1)
    return (int(sid[:4]), 0 if sid.endswith("h") else 1, int(no))


def past_links(past, labels, prefix):
    out = []
    for p in sorted(past, key=past_order, reverse=True):
        sid, no = p.rsplit("-", 1)
        out.append(f"[{short_label(labels[sid])}問{int(no)}]({prefix}08_過去問解説/科目A/{sid}.md#q{no})")
    return " ".join(out)


def cell(s):
    return s.replace("|", "｜").replace("\n", " ")


def term_cell(t, prefix):
    s = f"**{cell(t['term'])}**"
    if t.get("src"):
        s += f" [📖]({prefix}{t['src']})"
    if t.get("en"):
        s += f"<br><sub>{cell(t['en'])}</sub>"
    return s


def desc_cell(t):
    s = cell(t["desc"])
    if t.get("point"):
        s += f"<br>💡 {cell(t['point'])}"
    return s


def subs_in_order(terms):
    out = []
    for t in terms:
        if t["sub"] not in out:
            out.append(t["sub"])
    return out


def anchor(text):
    """GitHub 風の見出しアンカー（小文字化・記号除去・空白→ハイフン）"""
    a = text.strip().lower()
    a = re.sub(r"[^\w\- ぁ-んァ-ヶー一-龥々〆〇]", "", a)
    return a.replace(" ", "-")


def build_category(d, labels, nav):
    terms = d["terms"]
    n3 = [t for t in terms if t["imp"] == 3]
    n2 = sum(1 for t in terms if t["imp"] == 2)
    n1 = sum(1 for t in terms if t["imp"] == 1)
    npast = sum(1 for t in terms if t.get("past"))
    subs = subs_in_order(terms)
    prev_link, next_link = nav
    L = []
    L.append(f"# 用語集 {d['no']:02d} {d['category']}")
    L.append("")
    L.append(f"> シラバス Ver.7.2「中分類{d['no']}：{d['category']}」（{FIELDS[d['field']]}）の用語 **{len(terms)}語**。"
             f"重要度 ★★★ {len(n3)}語 / ★★ {n2}語 / ★ {n1}語。科目A過去問（13回分）で問われた語は {npast}語です。")
    L.append("")
    L.append(f"**効率のよい使い方**：①「★★★ 最重要用語」を読む → ②[用語ドリル](../06_インタラクティブ教材/terms.html#c{d['no']})"
             f"で中分類「{d['category']}」を4択テスト → ③間違えた語を下の小分類の表で確認、の順に進めます。"
             "📖 は詳しい解説がある章へのリンク、過去問の欄は実際に問われた問題（解説つき）へのリンクです。")
    L.append("")
    L.append(f"[← 用語集の目次](README.md)" + (f" ｜ [前：{prev_link[1]}]({prev_link[0]})" if prev_link else "")
             + (f" ｜ [次：{next_link[1]}]({next_link[0]})" if next_link else ""))
    L.append("")
    L.append("## 目次")
    L.append("")
    L.append(f"- [★★★ 最重要用語（{len(n3)}語）](#最重要用語)")
    for s in subs:
        cnt = sum(1 for t in terms if t["sub"] == s)
        L.append(f"- [{s}（{cnt}語）](#{anchor(s)})")
    if d.get("pairs"):
        L.append(f"- [まぎらわしい用語（{len(d['pairs'])}組）](#まぎらわしい用語)")
    L.append(f"- [一問一答（★★★）](#一問一答)")
    L.append("")
    L.append("---")
    L.append("")
    L.append('<a id="最重要用語"></a>')
    L.append("")
    L.append("## ★★★ 最重要用語")
    L.append("")
    L.append("まずはこの表の用語を、説明を見ずに言えるようにしましょう。")
    L.append("")
    L.append("| 用語 | 説明・ポイント | 過去問 |")
    L.append("|---|---|---|")
    for t in sorted(n3, key=lambda t: -len(t.get("past", []))):
        L.append(f"| {term_cell(t, '../')} | {desc_cell(t)} | {past_links(t.get('past', []), labels, '../')} |")
    L.append("")
    for s in subs:
        L.append(f"## {s}")
        L.append("")
        L.append("| 重要度 | 用語 | 説明・ポイント | 過去問 |")
        L.append("|---|---|---|---|")
        for t in terms:
            if t["sub"] != s:
                continue
            L.append(f"| {STARS[t['imp']]} | {term_cell(t, '../')} | {desc_cell(t)} | {past_links(t.get('past', []), labels, '../')} |")
        L.append("")
    if d.get("pairs"):
        L.append('<a id="まぎらわしい用語"></a>')
        L.append("")
        L.append("## まぎらわしい用語")
        L.append("")
        L.append("| 用語 | 用語 | 違い |")
        L.append("|---|---|---|")
        for p in d["pairs"]:
            L.append(f"| **{cell(p['a'])}** | **{cell(p['b'])}** | {cell(p['diff'])} |")
        L.append("")
    L.append('<a id="一問一答"></a>')
    L.append("")
    L.append("## 一問一答（★★★）")
    L.append("")
    L.append("説明を読んで用語を答えてください。クリックすると答えが開きます。")
    L.append("")
    for i, t in enumerate(n3, 1):
        L.append(f"<details><summary>Q{i}. {cell(t['desc'])}</summary>")
        L.append("")
        L.append(f"**{cell(t['term'])}**" + (f"（{cell(t['en'])}）" if t.get("en") else ""))
        L.append("</details>")
        L.append("")
    L.append("---")
    L.append("")
    L.append("出典：用語の範囲は IPA「応用情報技術者試験（レベル3）シラバス Ver.7.2」。過去問は IPA 公表の科目A（旧午前）問題。")
    return "\n".join(L) + "\n"


def build_top(cats, labels):
    L = ["# 最重要用語まとめ（全分野の★★★）", ""]
    total = sum(1 for d in cats for t in d["terms"] if t["imp"] == 3)
    L.append(f"> 23の中分類から重要度 ★★★ の用語 **{total}語** を集めました。試験直前の総チェックや、通勤中の見直しに使ってください。"
             "各分野の全用語は [用語集の目次](README.md) から。")
    L.append("")
    L.append("## 目次")
    L.append("")
    for f, name in FIELDS.items():
        L.append(f"- **{name}**：" + "、".join(f"[{d['category']}](#{d['no']:02d}-{anchor(d['category'])})" for d in cats if d["field"] == f))
    L.append("")
    for d in cats:
        L.append(f"## {d['no']:02d} {d['category']}")
        L.append("")
        L.append(f"[この分野の用語集（全{len(d['terms'])}語）]({d['file']})")
        L.append("")
        L.append("| 用語 | 説明・ポイント |")
        L.append("|---|---|")
        for t in d["terms"]:
            if t["imp"] == 3:
                L.append(f"| {term_cell(t, '../')} | {desc_cell(t)} |")
        L.append("")
    return "\n".join(L) + "\n"


def build_readme(cats):
    total = sum(len(d["terms"]) for d in cats)
    s3 = sum(1 for d in cats for t in d["terms"] if t["imp"] == 3)
    s2 = sum(1 for d in cats for t in d["terms"] if t["imp"] == 2)
    pairs = sum(len(d.get("pairs", [])) for d in cats)
    npast = sum(1 for d in cats for t in d["terms"] if t.get("past"))
    L = ["# 用語集 — 分野別に用語と説明をまとめた資料", ""]
    L.append(f"シラバス Ver.7.2 の全23中分類について、用語を **1行の説明＋試験のポイント** でまとめました。全 **{total}語**、"
             f"そのうち重要度 ★★★ が {s3}語、★★ が {s2}語です。科目A過去問（13回・1,040問）で実際に問われた {npast}語には、その問題へのリンクを付けています。")
    L.append("")
    L.append("## 効率よく覚える3ステップ")
    L.append("")
    L.append("1. **★★★ から覚える**：まず [最重要用語まとめ](00_最重要用語まとめ.md)（全分野の★★★）か、各分野の冒頭の「★★★ 最重要用語」を読む。科目Aの用語問題の多くはここから出ます。")
    L.append("2. **テストで確かめる**：[用語ドリル](../06_インタラクティブ教材/terms.html) の4択テスト・カードで、説明 → 用語、用語 → 説明の両方向で答えられるか確認する。間違えた語は自動で「苦手」に入ります。")
    L.append("3. **★★ → ★ と広げる**：★★★ が8割言えるようになったら ★★ へ。まぎらわしい用語の表で違いを説明できるようにする。")
    L.append("")
    L.append("💡 **★の付け方**：過去13回の科目Aで繰り返し問われた語や、科目Bの前提になる基本語が ★★★、1回問われた語・定番の知識が ★★、それ以外のシラバス用語が ★ です。"
             "★ の語も出題範囲ですが、時間が限られているなら後回しにして構いません。")
    L.append("")
    L.append("## 分野別の用語集")
    L.append("")
    for f, name in FIELDS.items():
        L.append(f"### {name}")
        L.append("")
        L.append("| 中分類 | 語数 | ★★★ | ★★ | まぎらわしい用語 |")
        L.append("|---|---|---|---|---|")
        for d in cats:
            if d["field"] != f:
                continue
            t = d["terms"]
            L.append(f"| [{d['no']:02d} {d['category']}]({d['file']}) | {len(t)} | {sum(1 for x in t if x['imp'] == 3)} | "
                     f"{sum(1 for x in t if x['imp'] == 2)} | {len(d.get('pairs', []))}組 |")
        L.append("")
    L.append("## ほかの教材との関係")
    L.append("")
    L.append("| 教材 | 使い分け |")
    L.append("|---|---|")
    L.append("| この用語集 | 用語の意味を素早く確認・暗記する（辞書・単語帳） |")
    L.append("| [各章の解説](../README.md#目次)（`01`〜`03`） | 仕組みや計算を理解する。用語集の 📖 から該当箇所に飛べます |")
    L.append("| [頻出略語・用語集](../05_まとめ・横断資料/02_頻出略語・用語集.md) / [略語カード](../06_インタラクティブ教材/flashcards.html) | 英字略語（291語）の正式名称を覚える |")
    L.append("| [過去問解説](../08_過去問解説/README.md) | 用語が実際にどう問われるかを確認する |")
    L.append("")
    L.append(f"まぎらわしい用語の組は全分野で {pairs}組あります。")
    L.append("")
    L.append("## 作り方・修正のしかた")
    L.append("")
    L.append("元データは `data/*.json` です。修正したら `python3 09_用語集/tools/build_terms.py` で Markdown と用語ドリルを作り直します。詳しくは [README_DEV.md](README_DEV.md)。")
    return "\n".join(L) + "\n"


def build_js(cats, labels):
    data = {
        "sessions": {sid: short_label(lab) for sid, lab in labels.items()},
        "cats": [{"no": d["no"], "name": d["category"], "field": d["field"], "file": d["file"], "pairs": d.get("pairs", [])} for d in cats],
        "terms": [],
    }
    for d in cats:
        for t in d["terms"]:
            row = {"c": d["no"], "t": t["term"], "d": t["desc"], "i": t["imp"], "s": t["sub"]}
            for k, key in (("en", "e"), ("point", "p"), ("past", "x"), ("src", "r")):
                if t.get(k):
                    row[key] = sorted(t[k], key=past_order, reverse=True) if k == "past" else t[k]
            data["terms"].append(row)
    with open(TERMS_JS, "w", encoding="utf-8") as f:
        f.write("// 自動生成: 09_用語集/tools/build_terms.py（手で編集しないこと）\n")
        f.write("window.APL_DATA_TERMS = ")
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")


def main():
    with open(KEYS, encoding="utf-8") as f:
        labels = {sid: v["label"] for sid, v in json.load(f).items()}
    cats = load()
    for i, d in enumerate(cats):
        prev_link = (cats[i - 1]["file"], cats[i - 1]["category"]) if i > 0 else None
        next_link = (cats[i + 1]["file"], cats[i + 1]["category"]) if i + 1 < len(cats) else None
        with open(os.path.join(BASE, d["file"]), "w", encoding="utf-8") as f:
            f.write(build_category(d, labels, (prev_link, next_link)))
    with open(os.path.join(BASE, "00_最重要用語まとめ.md"), "w", encoding="utf-8") as f:
        f.write(build_top(cats, labels))
    with open(os.path.join(BASE, "README.md"), "w", encoding="utf-8") as f:
        f.write(build_readme(cats))
    build_js(cats, labels)
    total = sum(len(d["terms"]) for d in cats)
    print(f"用語集: {len(cats)}分野 {total}語 → Markdown {len(cats) + 2}ファイル, terms.js {os.path.getsize(TERMS_JS) // 1024}KB")


if __name__ == "__main__":
    main()
