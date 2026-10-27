"""用語が科目A過去問（08_過去問解説/科目A/data/*.json）の問題文・選択肢・キーワードに何問出たかを数える。"""
import glob
import json
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAST = os.path.join(ROOT, "08_過去問解説", "科目A", "data")


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"\s+", "", s).lower()


def variants(term):
    """「PKI（公開鍵基盤）」「単精度・倍精度」のような表記から、照合に使う語の候補を作る。"""
    t = unicodedata.normalize("NFKC", term)
    out = {t}
    inner = re.findall(r"[（(]([^）)]*)[）)]", t)
    base = re.sub(r"[（(][^）)]*[）)]", "", t).strip()
    out.add(base)
    for s in inner:
        out.update(x for x in re.split(r"[、,，]", s))
    for s in list(out):
        parts = re.split(r"[・／/、，,]|及び|と(?=[^\s])(?<=[ぁ-んァ-ヶー一-龥]と)", s)
        if len(parts) > 1:
            out.update(parts)
    res = set()
    for v in out:
        v = norm(v).strip("・.。:：")
        if len(v) >= 2 and not re.fullmatch(r"[\d\W_]+", v):
            res.add(v)
    return res


def load_questions():
    qs = []
    for path in sorted(glob.glob(os.path.join(PAST, "*.json"))):
        data = json.load(open(path, encoding="utf-8"))
        for q in data["questions"]:
            qs.append({
                "sid": data["id"], "label": data["label"], "no": q["no"], "category": q["category"],
                "kw": [norm(k) for k in q.get("keywords", [])],
                "choices": norm(" ".join(q["choices"])),
                "full": norm(q["q"] + " " + " ".join(q["choices"])),
            })
    return qs


def _in(v, text):
    if re.fullmatch(r"[a-z0-9.+#\-]+", v):
        return re.search(r"(?<![a-z0-9])" + re.escape(v) + r"(?![a-z0-9])", text) is not None
    return v in text


_DF = {}


def _generic(v, questions):
    """問題文全体で多く出る一般語（「サービス」「プロセス」など）は照合に使わない。"""
    if v not in _DF:
        _DF[v] = sum(1 for q in questions if _in(v, q["full"]))
    return _DF[v] > 40


def count(term, category, questions):
    """その用語が「問われた」問の一覧を返す。

    問のキーワード（出題テーマ）か選択肢に用語が現れたものを数える。問題文の地の文だけに出る語は数えない。
    """
    vs = [v for v in variants(term) if not _generic(v, questions)]
    hits = []
    for q in questions:
        for v in vs:
            short = len(v) <= 2 and not re.fullmatch(r"[a-z0-9.+#\-]+", v)
            if short and q["category"] != category:
                continue
            if any(_in(v, k) for k in q["kw"]) or _in(v, q["choices"]):
                hits.append(q)
                break
    return hits
