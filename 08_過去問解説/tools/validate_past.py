#!/usr/bin/env python3
"""科目A過去問データ（科目A/data/*.json）の検査。使い方: python3 tools/validate_past.py [id ...]"""
import json, os, re, sys

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "科目A")
CATEGORIES = {
    "tech": ["基礎理論", "アルゴリズムとプログラミング", "コンピュータ構成要素", "システム構成要素", "ソフトウェア",
             "ハードウェア", "ユーザーインタフェース", "情報メディア", "データベース", "ネットワーク", "セキュリティ",
             "システム開発技術", "ソフトウェア開発管理技術"],
    "mgmt": ["プロジェクトマネジメント", "サービスマネジメント", "システム監査"],
    "strat": ["システム戦略", "システム企画", "経営戦略マネジメント", "技術戦略マネジメント", "ビジネスインダストリ", "企業活動", "法務"],
}
KEYS = {"no", "field", "category", "q", "choices", "answer", "figures", "calc", "keywords", "explanation", "modified"}


def check(sid, keys):
    errs = []
    path = os.path.join(BASE, "data", sid + ".json")
    try:
        data = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        return [f"JSONとして読めない: {e}"]
    if data.get("id") != sid:
        errs.append("id がファイル名と一致しない")
    if data.get("label") != keys[sid]["label"]:
        errs.append(f"label は {keys[sid]['label']!r} にする")
    qs = data.get("questions", [])
    nos = [q.get("no") for q in qs]
    missing = sorted(set(range(1, 81)) - set(nos))
    if missing:
        errs.append(f"未作成の問: {missing}")
    if len(nos) != len(set(nos)):
        errs.append("問番号が重複")
    for q in qs:
        n = q.get("no")
        p = f"問{n}: "
        if set(q) != KEYS:
            errs.append(p + f"キーが仕様と違う（不足 {sorted(KEYS - set(q))} / 余分 {sorted(set(q) - KEYS)}）")
            continue
        exp_ans, exp_field = keys[sid]["answers"][n - 1]
        if q["answer"] != exp_ans:
            errs.append(p + f"answer={q['answer']} だが IPA 解答例は {'アイウエ'[exp_ans]}")
        if q["field"] != exp_field:
            errs.append(p + f"field={q['field']} だが解答例は {exp_field}")
        if q["category"] not in CATEGORIES.get(q["field"], []):
            errs.append(p + f"category {q['category']!r} が {q['field']} の中分類にない")
        if not isinstance(q["choices"], list) or len(q["choices"]) != 4 or not all(isinstance(c, str) and c.strip() for c in q["choices"]):
            errs.append(p + "choices は空でない文字列4つ")
        if len(q["q"].strip()) < 8:
            errs.append(p + "問題文が短すぎる")
        if len(q["explanation"].strip()) < 60:
            errs.append(p + "解説が短すぎる（60字以上）")
        for f in q["figures"]:
            if not re.fullmatch(rf"img/{sid}_q{n:02d}[a-z]?\.png", f):
                errs.append(p + f"図のパス {f} は img/{sid}_q{n:02d}.png 形式に")
            elif not os.path.exists(os.path.join(BASE, f)):
                errs.append(p + f"図 {f} が存在しない")
        if not isinstance(q["calc"], bool):
            errs.append(p + "calc は true/false")
        if not isinstance(q["keywords"], list) or not q["keywords"]:
            errs.append(p + "keywords は1個以上")
    return errs


def main():
    keys = json.load(open(os.path.join(BASE, "answer_keys.json"), encoding="utf-8"))
    ids = sys.argv[1:] or sorted(f[:-5] for f in os.listdir(os.path.join(BASE, "data")) if f.endswith(".json"))
    bad = 0
    for sid in ids:
        errs = check(sid, keys)
        print(f"{sid}: {'OK' if not errs else str(len(errs)) + ' 件のエラー'}")
        for e in errs[:60]:
            print("  -", e)
        bad += bool(errs)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
