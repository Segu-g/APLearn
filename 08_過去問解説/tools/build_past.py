#!/usr/bin/env python3
"""過去問データから解説集とクイズ用データを生成する。

  科目A/data/*.json → 科目A/<id>.md、科目A/分野別索引.md、
                       ../06_インタラクティブ教材/data/past_questions.js
  科目B/data/*.json → 科目B/問NN_<分野>.md、科目B/README.md

使い方: python3 tools/build_past.py
"""
import json
import os
import re
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A_DIR = os.path.join(BASE, "科目A")
B_DIR = os.path.join(BASE, "科目B")
QUIZ_JS = os.path.join(os.path.dirname(BASE), "06_インタラクティブ教材", "data", "past_questions.js")

KANA = "アイウエ"
FIELD_NAME = {"tech": "テクノロジ系", "mgmt": "マネジメント系", "strat": "ストラテジ系"}
CATEGORY_ORDER = [
    "基礎理論", "アルゴリズムとプログラミング", "コンピュータ構成要素", "システム構成要素", "ソフトウェア",
    "ハードウェア", "ユーザーインタフェース", "情報メディア", "データベース", "ネットワーク", "セキュリティ",
    "システム開発技術", "ソフトウェア開発管理技術", "プロジェクトマネジメント", "サービスマネジメント", "システム監査",
    "システム戦略", "システム企画", "経営戦略マネジメント", "技術戦略マネジメント", "ビジネスインダストリ", "企業活動", "法務",
]
B_FIELDS = [
    "情報セキュリティ", "経営戦略", "プログラミング", "システムアーキテクチャ", "ネットワーク", "データベース",
    "組込みシステム開発", "情報システム開発", "プロジェクトマネジメント", "サービスマネジメント", "システム監査",
]


def load_dir(d):
    out = []
    dd = os.path.join(d, "data")
    if not os.path.isdir(dd):
        return out
    for fn in sorted(os.listdir(dd)):
        if fn.endswith(".json"):
            with open(os.path.join(dd, fn), encoding="utf-8") as f:
                out.append(json.load(f))
    # 新しい回から並べる（id は年＋元号年＋期。春 h ＜ 10月 o ＜ 秋 a の順で比較）
    order = {"h": 0, "o": 1, "a": 2}
    out.sort(key=lambda x: (x["id"][:4], order.get(x["id"][-1], 0)), reverse=True)
    return out


def source_label(label):
    """'令和7年度秋期' → '令和7年度 秋期'"""
    return re.sub(r"年度(?=\S)", "年度 ", label)


def source_line(exam, n, area):
    s = f"出典：{source_label(exam['label'])} 応用情報技術者試験 {area} 問{n}"
    return s


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.rstrip() + "\n")


# ---------------------------------------------------------------- 科目A
def build_a(exams):
    by_cat = defaultdict(list)
    for ex in exams:
        lines = [
            f"# {ex['label']} 科目A（旧午前）過去問解説",
            "",
            f"> {source_label(ex['label'])} 応用情報技術者試験 午前（全80問）を書き起こし、オリジナルの解説を付けたものです。"
            "問題の著作権は IPA（独立行政法人 情報処理推進機構）にあります。",
            "> 図を表に書き換えるなど一部改変した問題には、その旨を記載しています。",
            "> インタラクティブ教材の [科目A 四択クイズ](../../06_インタラクティブ教材/quiz.html) では、この回を本番形式（150分）で解けます。",
            "",
            "## 目次",
            "",
            "| 問 | 分野 | 中分類 | キーワード |",
            "|---|---|---|---|",
        ]
        qs = sorted(ex["questions"], key=lambda q: q["no"])
        for q in qs:
            lines.append(f"| [問{q['no']}](#q{q['no']:02d}) | {FIELD_NAME[q['field']]} | {q['category']} | {'、'.join(q['keywords'])} |")
            by_cat[q["category"]].append((ex, q))
        lines.append("")
        for q in qs:
            lines += [f'<a id="q{q["no"]:02d}"></a>', "", f"### 問{q['no']}　〔{q['category']}〕{' 🧮' if q['calc'] else ''}", "", q["q"], ""]
            for f in q["figures"]:
                lines += [f"![問{q['no']}の図]({f})", ""]
            for i, c in enumerate(q["choices"]):
                lines.append(f"- **{KANA[i]}**　{c}")
            lines += [
                "",
                "<details><summary>解答・解説</summary>",
                "",
                f"**正解：{KANA[q['answer']]}**",
                "",
                q["explanation"],
                "",
                "</details>",
                "",
                f"<sub>{source_line(ex, q['no'], '午前')}{'（' + q['modified'] + '）' if q['modified'] else ''}</sub>",
                "",
                "---",
                "",
            ]
        write(os.path.join(A_DIR, ex["id"] + ".md"), "\n".join(lines))

    # 分野別索引
    lines = [
        "# 科目A 過去問 分野別索引",
        "",
        "> シラバス Ver.7.2 の中分類ごとに、過去問を新しい順に並べています。苦手分野をまとめて解くときに使ってください。",
        "",
        "## 出題数（収録した回の合計）",
        "",
        "| 中分類 | 問題数 |",
        "|---|---|",
    ]
    for c in CATEGORY_ORDER:
        if by_cat.get(c):
            lines.append(f"| [{c}](#{c}) | {len(by_cat[c])} |")
    lines.append("")
    for c in CATEGORY_ORDER:
        items = by_cat.get(c)
        if not items:
            continue
        lines += [f"## {c}", "", "| 回 | 問 | キーワード |", "|---|---|---|"]
        for ex, q in items:
            lines.append(f"| {ex['label']} | [問{q['no']}]({ex['id']}.md#q{q['no']:02d}) | {'、'.join(q['keywords'])} |")
        lines.append("")
    write(os.path.join(A_DIR, "分野別索引.md"), "\n".join(lines))

    # クイズ用 JS（パスを 06_インタラクティブ教材/quiz.html から見た形に直す）
    data = []
    for ex in exams:
        for q in sorted(ex["questions"], key=lambda q: q["no"]):
            data.append({
                "id": f"{ex['id']}-{q['no']:02d}",
                "exam": ex["id"],
                "examLabel": ex["label"],
                "no": q["no"],
                "field": q["field"],
                "topic": q["category"],
                "q": q["q"],
                "choices": q["choices"],
                "answer": q["answer"],
                "figures": ["../08_過去問解説/科目A/" + f for f in q["figures"]],
                "calc": q["calc"],
                "keywords": q["keywords"],
                "explanation": q["explanation"].replace("](../../", "](../"),
                "source": source_line(ex, q["no"], "午前") + ("（" + q["modified"] + "）" if q["modified"] else ""),
            })
    os.makedirs(os.path.dirname(QUIZ_JS), exist_ok=True)
    with open(QUIZ_JS, "w", encoding="utf-8") as f:
        f.write("// 自動生成: 08_過去問解説/tools/build_past.py（問題の著作権は IPA）\n")
        f.write("window.APL_DATA_PAST = ")
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    return len(data)


# ---------------------------------------------------------------- 科目B
def build_b(exams):
    by_field = defaultdict(list)
    for ex in exams:
        for p in ex["problems"]:
            by_field[p["field"]].append((ex, p))
    index = [
        "# 科目B（旧午後）過去問 分野別ガイド",
        "",
        "> IPA が公表した過去の午後問題（現在の科目B）を、分野ごとに「何が問われ、どう解くか」の観点で整理しました。"
        "問題文は IPA の PDF を見ながら使ってください（各問にリンクがあります）。解答例は IPA 公表のもの、解き方の解説はオリジナルです。",
        "",
        "| 問 | 分野 | 収録数 | ガイド |",
        "|---|---|---|---|",
    ]
    for i, field in enumerate(B_FIELDS, 1):
        items = by_field.get(field, [])
        fn = f"問{i:02d}_{field}.md"
        index.append(f"| 問{i} | {field} | {len(items)} | [{fn}]({fn}) |")
        if not items:
            continue
        lines = [
            f"# 科目B 問{i} {field} 過去問ガイド",
            "",
            "> 各問は「状況設定 → 設問ごとの解答例と解き方 → 必要な知識 → 採点講評 → 学ぶべきこと」の順に整理しています。"
            "まず IPA の問題冊子 PDF で問題を解き、そのあとこのガイドで答え合わせをしてください。",
            "",
            "## 出題テーマ一覧",
            "",
            "| 回 | タイトル | 難易度 |",
            "|---|---|---|",
        ]
        for ex, p in items:
            lines.append(f"| {ex['label']} | [{p['title']}](#{ex['id']}) | {'★' * int(p.get('difficulty', 2))} |")
        lines.append("")
        for ex, p in items:
            lines += [
                f'<a id="{ex["id"]}"></a>',
                "",
                f"## {ex['label']} 問{p['no']}「{p['title']}」",
                "",
                f"- 問題冊子：[IPA 公式 PDF]({ex['pdf']})（{p['pages']} ページ）",
                f"- 難易度：{'★' * int(p.get('difficulty', 2))}",
                f"- 出題趣旨：{p['theme']}",
                "",
                "### 状況設定",
                "",
                p["situation"],
                "",
                "### 設問と解き方",
                "",
            ]
            for qq in p["questions"]:
                lines += [
                    f"#### {qq['label']}",
                    "",
                    f"- **問われていること**：{qq['ask']}",
                    f"- **解答例**：{qq['answer'].strip().replace(chr(10), '　／　')}",
                    "",
                    f"**解き方**：{qq['howto']}",
                    "",
                ]
            lines += ["### 必要な知識", ""] + [f"- {k}" for k in p["knowledge"]] + [""]
            lines += ["### 採点講評のポイント", "", p["comment"], "", "### この問題から学ぶこと", "", p["lessons"], ""]
            lines += [f"<sub>{source_line(ex, p['no'], '午後')}（解答例は IPA 公表の解答例より）</sub>", "", "---", ""]
        write(os.path.join(B_DIR, fn), "\n".join(lines))
    write(os.path.join(B_DIR, "README.md"), "\n".join(index))


def main():
    na = build_a(load_dir(A_DIR))
    build_b(load_dir(B_DIR))
    print(f"科目A {na}問、科目B を生成しました")


if __name__ == "__main__":
    main()
