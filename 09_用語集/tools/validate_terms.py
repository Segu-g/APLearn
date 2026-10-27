#!/usr/bin/env python3
"""用語集データ（09_用語集/data/*.json）の検査。使い方: python3 09_用語集/tools/validate_terms.py [NN ...]"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "09_用語集", "data")
PAST = os.path.join(ROOT, "08_過去問解説", "科目A", "data")
TERM_KEYS = {"term", "en", "desc", "point", "imp", "past", "sub", "src"}
PAST_RE = re.compile(r"^(\d{4}[a-z]\d\d[a-z])-(\d\d)$")


def past_ids():
    ids = set()
    for p in glob.glob(os.path.join(PAST, "*.json")):
        d = json.load(open(p, encoding="utf-8"))
        ids.update(f"{d['id']}-{int(q['no']):02d}" for q in d["questions"])
    return ids


def check(path, valid_past):
    errs, warns = [], []
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        return [f"JSONとして読めない: {e}"], []
    for k in ("no", "category", "field", "pairs", "terms"):
        if k not in d:
            errs.append(f"キー {k} が無い")
    terms = d.get("terms", [])
    seen = set()
    imps = {1: 0, 2: 0, 3: 0}
    for i, t in enumerate(terms):
        p = f"[{i}] {t.get('term', '?')}: "
        extra = set(t) - TERM_KEYS
        if extra:
            errs.append(p + f"余分なキー {sorted(extra)}")
        for k in ("term", "desc", "imp", "sub"):
            if not t.get(k):
                errs.append(p + f"{k} が空")
        if t.get("term") in seen:
            errs.append(p + "用語が重複")
        seen.add(t.get("term"))
        if t.get("imp") not in (1, 2, 3):
            errs.append(p + "imp は 1〜3")
        else:
            imps[t["imp"]] += 1
        if t.get("imp") == 3 and not t.get("point"):
            errs.append(p + "★★★ には point が必要")
        if len(t.get("desc", "")) > 110:
            warns.append(p + f"desc が長い（{len(t['desc'])}字）")
        if len(t.get("point", "")) > 170:
            warns.append(p + f"point が長い（{len(t['point'])}字）")
        past = t.get("past", [])
        if not isinstance(past, list) or len(past) > 4:
            errs.append(p + "past は最大4件のリスト")
        else:
            for x in past:
                if not PAST_RE.match(x) or x not in valid_past:
                    errs.append(p + f"past {x!r} が存在しない問")
        src = t.get("src", "")
        if src:
            f = src.split("#")[0]
            if not os.path.exists(os.path.join(ROOT, f)):
                errs.append(p + f"src のファイルが無い: {f}")
    for j, pr in enumerate(d.get("pairs", [])):
        if set(pr) != {"a", "b", "diff"} or not all(pr.values()):
            errs.append(f"pairs[{j}] は a, b, diff が必要")
    n = len(terms) or 1
    info = f"{len(terms)}語 ★★★{imps[3]}({imps[3]*100//n}%) ★★{imps[2]}({imps[2]*100//n}%) ★{imps[1]} pairs{len(d.get('pairs', []))} past付き{sum(1 for t in terms if t.get('past'))}"
    return errs, warns, info


def main():
    want = sys.argv[1:]
    valid_past = past_ids()
    bad = 0
    for path in sorted(glob.glob(os.path.join(DATA, "*.json"))):
        name = os.path.basename(path)
        if want and not any(name.startswith(w) for w in want):
            continue
        res = check(path, valid_past)
        errs, warns = res[0], res[1]
        info = res[2] if len(res) > 2 else ""
        print(("NG " if errs else "OK ") + name, info)
        for e in errs[:30]:
            print("   ✗", e)
        for w in warns[:15]:
            print("   △", w)
        bad += bool(errs)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
