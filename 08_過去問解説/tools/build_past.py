#!/usr/bin/env python3
"""過去問データから解説集とクイズ用データを生成する。

  科目A/data/*.json → 科目A/<id>.md、科目A/分野別索引.md、
                       ../06_インタラクティブ教材/data/past_questions.js
  科目B/data/*.json → 科目B/問NN_<分野>.md（分野別）、科目B/<id>.md（回別）、科目B/README.md
  ipa_pdfs.json      → README.md の「回別一覧」（IPA の問題・解答・採点講評 PDF へのリンク）

使い方: python3 tools/build_past.py
"""
import json
import os
import re
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A_DIR = os.path.join(BASE, "科目A")
B_DIR = os.path.join(BASE, "科目B")
PDF_JSON = os.path.join(BASE, "ipa_pdfs.json")
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


def clean_expl(text):
    """解説の先頭にある「正解：ア」の重複表示を取り除く（正解は別に表示するため）"""
    return re.sub(r"^\*\*正解[：:]\s*[アイウエ]\*\*[ 　]*", "", text.strip())


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
                clean_expl(q["explanation"]),
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
                "explanation": clean_expl(q["explanation"]).replace("](../../", "](../"),
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
KANA_RE = re.compile(r"(?<![ァ-ヶー])([ア-ン])(?![ァ-ヶー])")


def group_of(p, label):
    """設問ラベルが使う解答群（problem["choices"] の要素）を返す。なければ None"""
    for g in p.get("choices", []):
        if label in g["targets"]:
            return g
    return None


def fmt_answer(p, qq):
    """解答例の記号に選択肢の本文を添える（例：'ク' → 'ク（境界防御）'）"""
    ans = qq["answer"].strip().replace("\n", "　／　")
    g = group_of(p, qq["label"])
    if not g:
        return ans
    text = {it["k"]: it["t"] for it in g["items"]}
    return KANA_RE.sub(lambda m: f"{m.group(1)}（{text[m.group(1)]}）" if m.group(1) in text else m.group(1), ans)


def choice_lines(p):
    """解答群の一覧。正解の選択肢に ✅ と設問名を付け、用語の選択肢には説明を付ける"""
    groups = p.get("choices", [])
    if not groups:
        return []
    n_terms = sum(len(g["items"]) for g in groups if g["kind"] == "term")
    summary = "解答群（選択肢" + (f"と、選ばれなかった用語を含む {n_terms} 語の説明" if n_terms else "の一覧") + "）"
    out = [f"<details><summary>{summary}</summary>", ""]
    for g in groups:
        correct = defaultdict(list)
        for qq in p["questions"]:
            if qq["label"] in g["targets"]:
                for k in KANA_RE.findall(qq["answer"]):
                    correct[k].append(qq["label"])
        out += [f"**{'、'.join(g['targets'])} の解答群**", ""]
        for it in g["items"]:
            mark = f"✅ " if it["k"] in correct else ""
            who = f"（{'、'.join(correct[it['k']])} の正解）" if it["k"] in correct and len(g["targets"]) > 1 else ""
            note = f"<br>　{it['note']}" if it.get("note") else ""
            out.append(f"- {mark}**{it['k']}** {it['t']}{who}{note}")
        out.append("")
    out += ["</details>", ""]
    return out


def build_choice_index(exams):
    """全回の解答群に出た用語（kind が term の選択肢）を分野ごとに集めた説明集"""
    terms = defaultdict(dict)  # field -> term -> {"note", "uses": [(ex, p, labels, correct)]}
    for ex in exams:
        for p in ex["problems"]:
            for g in p.get("choices", []):
                if g["kind"] != "term":
                    continue
                for it in g["items"]:
                    ok = [qq["label"] for qq in p["questions"]
                          if qq["label"] in g["targets"] and it["k"] in KANA_RE.findall(qq["answer"])]
                    e = terms[p["field"]].setdefault(it["t"], {"note": it.get("note", ""), "uses": []})
                    e["uses"].append((ex, p, ok))
    total = sum(len(v) for v in terms.values())
    lines = [
        "# 科目B 解答群の用語集",
        "",
        f"> 科目B（旧午後）の過去問 {len(exams)}回分で、解答群（選択肢）に出た用語 {total} 語の説明です。"
        "正解だった用語には ✅ を付けています。正解にならなかった用語も、別の回では正解になったり科目Aで問われたりするので、まとめて覚えておくと効率的です。",
        "> 用語の説明はオリジナルです。選択肢の用語は IPA 公表の問題冊子から引用しています。",
        "",
        "## 目次",
        "",
    ]
    for f in B_FIELDS:
        if terms.get(f):
            lines.append(f"- [{f}（{len(terms[f])}語）](#{f})")
    lines.append("")
    for f in B_FIELDS:
        if not terms.get(f):
            continue
        lines += [f"## {f}", ""]
        for t in sorted(terms[f], key=lambda x: x.casefold()):
            e = terms[f][t]
            mark = "✅ " if any(ok for _, _, ok in e["uses"]) else ""
            src = "、".join(
                f"[{ex['label'].replace('年度', '')} 問{p['no']}{'（' + '・'.join(ok) + ' 正解）' if ok else ''}]({ex['id']}.md#q{p['no']:02d})"
                for ex, p, ok in e["uses"])
            lines.append(f"- {mark}**{t}**：{e['note']}<br>　<sub>出題：{src}</sub>")
        lines.append("")
    write(os.path.join(B_DIR, "解答群の用語集.md"), "\n".join(lines))
    return total


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
                    f"- **解答例**：{fmt_answer(p, qq)}",
                    "",
                    f"**解き方**：{qq['howto']}",
                    "",
                ]
            lines += choice_lines(p)
            lines += ["### 必要な知識", ""] + [f"- {k}" for k in p["knowledge"]] + [""]
            lines += ["### 採点講評のポイント", "", p["comment"], "", "### この問題から学ぶこと", "", p["lessons"], ""]
            lines += [f"<sub>{source_line(ex, p['no'], '午後')}（解答例は IPA 公表の解答例より）</sub>", "", "---", ""]
        write(os.path.join(B_DIR, fn), "\n".join(lines))
    index += [
        "",
        "## 回別（1回分の解答例と採点講評をまとめて見る）",
        "",
        "1回分を通して解いたあとの答え合わせ用です。問1〜問11の解答例と採点講評を1ページにまとめています。",
        "",
    ]
    for ex in exams:
        index.append(f"- [{ex['label']}]({ex['id']}.md)")
        build_b_exam(ex)
    if any(p.get("choices") for ex in exams for p in ex["problems"]):
        n = build_choice_index(exams)
        index += ["", "## 解答群の用語集", "",
                  f"解答群（選択肢）に出た用語 {n} 語を、選ばれなかったものも含めて分野別に説明しています："
                  "[解答群の用語集.md](解答群の用語集.md)"]
    write(os.path.join(B_DIR, "README.md"), "\n".join(index))


def pdf_links(exam_id, area):
    """IPA の PDF へのリンク（area は 'am' か 'pm'）を「問題・解答例・採点講評」の順で返す"""
    e = PDFS.get(exam_id, {})
    names = [("qs", "問題冊子"), ("ans", "解答例" if area == "pm" else "解答")] + ([("cmnt", "採点講評")] if area == "pm" else [])
    return "・".join(f"[{n}]({e[f'{area}_{k}']})" for k, n in names if e.get(f"{area}_{k}"))


def build_b_exam(ex):
    """1回分（問1〜問11）の解答例・採点講評を1ページにまとめる（スマホで答え合わせしやすいよう表を使わない）"""
    a_md = os.path.join(A_DIR, f"{ex['id']}.md")
    lines = [
        f"# {ex['label']} 科目B（午後）解答例と採点講評",
        "",
        "> 1回分の答え合わせ用ページです。各問の **解答例**（IPA 公表）と **採点講評のポイント**（IPA の採点講評の要約）を並べています。"
        "設問の内容と解き方（オリジナル）は「設問と解き方」を開くと読めます。",
        "",
        f"- IPA 公式 PDF：{pdf_links(ex['id'], 'pm')}",
        f"- 同じ回の科目A（午前）：" + (f"[解説集](../科目A/{ex['id']}.md)・" if os.path.exists(a_md) else "")
        + f"IPA {pdf_links(ex['id'], 'am')}",
        "",
        "## 目次",
        "",
    ]
    for p in ex["problems"]:
        sel = "必須" if p["no"] == 1 else "選択"
        lines.append(f"- [問{p['no']} {p['field']}（{sel}）「{p['title']}」](#q{p['no']:02d})")
    lines += ["", "---", ""]
    for p in ex["problems"]:
        i = B_FIELDS.index(p["field"]) + 1
        guide = f"問{i:02d}_{p['field']}.md#{ex['id']}"
        lines += [
            f'<a id="q{p["no"]:02d}"></a>',
            "",
            f"## 問{p['no']} {p['field']}「{p['title']}」",
            "",
            f"問題冊子 {p['pages']} ページ ／ 難易度 {'★' * int(p.get('difficulty', 2))} ／ [分野別ガイドで詳しく]({guide})",
            "",
            "### 解答例",
            "",
        ]
        for qq in p["questions"]:
            lines.append(f"- **{qq['label']}**：{fmt_answer(p, qq)}")
        lines += ["", "<details><summary>設問と解き方</summary>", ""]
        for qq in p["questions"]:
            lines += [
                f"**{qq['label']}**　{qq['ask']}",
                "",
                f"- 解答例：{fmt_answer(p, qq)}",
                f"- 解き方：{qq['howto']}",
                "",
            ]
        lines += ["</details>", ""] + choice_lines(p)
        lines += ["### 採点講評のポイント", "", p["comment"], ""]
        lines += [f"<sub>{source_line(ex, p['no'], '午後')}（解答例は IPA 公表の解答例より、採点講評は要約）</sub>",
                  "", f"[↑ 目次へ](#目次)", "", "---", ""]
    write(os.path.join(B_DIR, f"{ex['id']}.md"), "\n".join(lines))


# ---------------------------------------------------------------- 全体 README
def build_readme(a_exams, b_exams):
    from collections import Counter
    n_ex = len(a_exams)
    cat = Counter()
    kw = defaultdict(list)
    for ex in a_exams:
        for q in ex["questions"]:
            cat[q["category"]] += 1
            for k in q["keywords"]:
                kw[k.strip()].append((ex, q))
    lines = [
        "# 過去問解説（IPA 公表問題）",
        "",
        "> IPA が公表している応用情報技術者試験の過去問題を、出典を明記して教材化したものです。問題の著作権は IPA にあります。"
        "解説・解き方ガイドはオリジナルです（IPA「試験制度に関するよくある質問」の過去問題の使用に関する方針に基づく）。",
        "",
        "## 収録内容",
        "",
        f"- **科目A（旧午前）**：{n_ex}回分・{sum(len(e['questions']) for e in a_exams)}問。全問の書き起こしとオリジナル解説",
        f"- **科目B（旧午後）**：{len(b_exams)}回分・{sum(len(e['problems']) for e in b_exams)}問。分野別の解き方ガイドと、回別の解答例・採点講評まとめ（問題文は IPA の PDF を参照）",
        "",
        "## 使い方",
        "",
        "1. まず [インタラクティブ教材の四択クイズ](../06_インタラクティブ教材/quiz.html#past) の「IPA過去問」タブで、1回分を本番形式（80問・150分）で解く。",
        "2. 間違えた問題の解説を読み、関連する解説資料（01〜03）に戻って理解する。",
        "3. [分野別索引](科目A/分野別索引.md) で苦手な中分類の過去問をまとめて解く。",
        "4. 科目B は [分野別ガイド](科目B/README.md) で、選んだ分野の過去問を PDF で解いてから答え合わせをする。"
        "1回分を通して解いたら、下の回別一覧の「解答例・採点講評」で答え合わせをする。",
        "",
        "## 回別一覧（問題・解答・採点講評）",
        "",
        "この資料の解説と、IPA 公式の PDF（問題冊子・解答・採点講評）を回ごとにまとめています。",
        "",
    ]
    a_ids = {e["id"] for e in a_exams}
    b_ids = {e["id"] for e in b_exams}
    covered = [e for e in PDFS.values() if e["id"] in a_ids | b_ids]
    older = [e for e in PDFS.values() if e["id"] not in a_ids | b_ids]
    for e in covered:
        am = (f"[解説集](科目A/{e['id']}.md)・" if e["id"] in a_ids else "") + f"IPA {pdf_links(e['id'], 'am')}"
        pm = (f"[解答例・採点講評](科目B/{e['id']}.md)・" if e["id"] in b_ids else "") + f"IPA {pdf_links(e['id'], 'pm')}"
        lines += [f"### {e['label']}", "", f"- 科目A（午前）：{am}", f"- 科目B（午後）：{pm}", ""]
    if older:
        lines += [
            "<details><summary>それより前の回（IPA の PDF のみ）</summary>",
            "",
        ]
        for e in older:
            lines.append(f"- **{e['label']}**　午前：{pdf_links(e['id'], 'am')}　／　午後：{pdf_links(e['id'], 'pm')}")
        lines += ["", "</details>", ""]
    lines += [
        "",
        "## 中分類別の出題数（勉強の優先順位の目安）",
        "",
        f"{n_ex}回分の合計と、1回（80問）あたりの平均です。平均が多い分野ほど得点源になります。",
        "",
        "| 中分類 | 合計 | 1回あたり |",
        "|---|---|---|",
    ]
    for c in CATEGORY_ORDER:
        if cat[c]:
            lines.append(f"| [{c}](科目A/分野別索引.md#{c}) | {cat[c]} | {cat[c] / n_ex:.1f} |")
    rep = sorted(((k, v) for k, v in kw.items() if len({e['id'] for e, _ in v}) >= 3),
                 key=lambda kv: (-len({e['id'] for e, _ in kv[1]}), kv[0]))
    lines += [
        "",
        "## 繰り返し出題されているキーワード",
        "",
        "3回以上の試験で出題されたキーワードです。科目A は過去問の類題が多いので、ここに並ぶ用語は確実に説明できるようにしておきましょう。",
        "",
        "| キーワード | 出題回数 | 出題例 |",
        "|---|---|---|",
    ]
    for k, v in rep[:120]:
        n = len({e['id'] for e, _ in v})
        links = "、".join(f"[{e['label'].replace('年度', '')} 問{q['no']}](科目A/{e['id']}.md#q{q['no']:02d})" for e, q in v[:4])
        lines.append(f"| {k} | {n} | {links} |")
    write(os.path.join(BASE, "README.md"), "\n".join(lines))


def load_pdfs():
    if not os.path.exists(PDF_JSON):
        return {}
    with open(PDF_JSON, encoding="utf-8") as f:
        return {e["id"]: e for e in json.load(f)}


PDFS = load_pdfs()


def main():
    a_exams, b_exams = load_dir(A_DIR), load_dir(B_DIR)
    na = build_a(a_exams)
    build_b(b_exams)
    build_readme(a_exams, b_exams)
    print(f"科目A {na}問、科目B を生成しました")


if __name__ == "__main__":
    main()
