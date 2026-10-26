#!/usr/bin/env python3
"""略語集（06_インタラクティブ教材/data/glossary.js）から「用語聞き流し」の台本を生成する。

  出力: scripts/gNN_glossary-<分野>.json（分野ごとに1本）
  使い方: python3 tools/make_glossary_scripts.py   → そのあと build_audio.py で音声化
"""
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLOSSARY_JS = os.path.join(os.path.dirname(BASE), "06_インタラクティブ教材", "data", "glossary.js")
SCRIPTS = os.path.join(BASE, "scripts")

# 慣用の読み方がある略語（VOICEVOX が1文字ずつ読む・誤読するもの）
YOMI = {
    "GAN": "ギャン", "RAG": "ラグ", "IoT": "アイオーティー", "FLOPS": "フロップス", "UTF-8": "ユーティーエフエイト",
    "IaaS": "イアース", "PaaS": "パース", "SaaS": "サース", "KVS": "ケーブイエス", "BASE": "ベース",
    "CRUD": "クラッド", "ACID": "アシッド", "SoC": "エスオーシー", "SPOF": "スポフ", "RASIS": "レイシス",
    "PoE": "ピーオーイー", "CSIRT": "シーサート", "SOC": "ソック", "SAML": "サムル", "WAF": "ワフ",
    "SIEM": "シーム", "DoS": "ドス", "DDoS": "ディードス", "DKIM": "ディーキム", "DMARC": "ディーマーク",
    "S/MIME": "エスマイム", "SHA-256": "シャー、ニーゴーロク", "MAC": "マック", "HMAC": "エイチマック",
    "REST": "レスト", "JSON": "ジェイソン", "PMBOK": "ピンボック", "COCOMO": "ココモ", "ITIL": "アイティル",
    "COSO": "コソ", "COBIT": "コビット", "CAAT": "キャット", "SoR": "エスオーアール", "SoE": "エスオーイー",
    "PoC": "ピーオーシー", "SWOT": "スウォット", "SDGs": "エスディージーズ", "AIDMA": "アイドマ",
    "AISAS": "アイサス", "OODA": "ウーダ", "CISO": "シーソ", "NISC": "ニスク", "2PC": "ツーフェーズコミット",
    "FIFO": "ファイフォ", "NAPT": "ナプト", "IMAP": "アイマップ", "CIDR": "サイダー", "VLAN": "ブイラン",
    "IPv6": "アイピーブイシックス", "POP3": "ポップスリー", "WPA3": "ダブリューピーエースリー",
    "4P": "フォーピー", "4C": "フォーシー", "O2O": "オーツーオー", "B2B / B2C": "ビートゥービー、ビートゥーシー",
    "PL / P/L": "ピーエル", "BS / B/S": "ビーエス", "CF / C/F": "シーエフ", "M&A": "エムアンドエー",
    "DevOps": "デブオプス", "E-R図": "イーアールず", "SLA（契約）": "エスエルエー", "CC（評価基準）": "シーシー",
    "PPP / PFI": "ピーピーピー、ピーエフアイ", "TQC / TQM": "ティーキューシー、ティーキューエム",
    "CSMA/CD": "シーエスエムエー、シーディー", "CSMA/CA": "シーエスエムエー、シーエー",
}


def load_glossary():
    with open(GLOSSARY_JS, encoding="utf-8") as f:
        src = f.read()
    return json.loads(src[src.index("["): src.rindex("]") + 1])


def speakable(text):
    """記号を読み上げ向けに整える（表示用テキストはそのまま残す）"""
    t = text.replace("／", "、").replace("/", "、").replace("→", "、").replace("（", "、").replace("）", "、")
    return re.sub(r"、+", "、", t).strip("、")


def main():
    terms = load_glossary()
    cats = []
    for t in terms:
        if t["category"] not in cats:
            cats.append(t["category"])
    for i, cat in enumerate(cats, 1):
        items = [t for t in terms if t["category"] == cat]
        lines = [
            {"speaker": "zundamon", "text": f"用語の聞き流し、{cat}編なのだ。"},
            {"speaker": "metan", "text": "略語を読み上げたら、少し間をあけるわね。意味を思い浮かべてから答えを聞いてね。"},
        ]
        for t in items:
            line = {"speaker": "metan", "text": f"{t['abbr']}。"}
            if t["abbr"] in YOMI:
                line["yomi"] = YOMI[t["abbr"]] + "。"
            lines.append(line)
            lines.append({"pause": 1.5})
            if re.search(r"[A-Za-z]", t["full"]):
                lines.append({"speaker": "zundamon", "text": f"{t['full']}。"})
            m = {"speaker": "zundamon", "text": t["meaning"]}
            if speakable(t["meaning"]) != t["meaning"]:
                m["yomi"] = speakable(t["meaning"])
            lines.append(m)
        lines.append({"speaker": "metan", "text": f"{cat}編は、ここまでよ。聞き取れなかった用語は、略語カードで復習してね。"})
        script = {
            "id": f"g{i:02d}",
            "title": f"用語聞き流し{i} {cat}",
            "summary": f"{cat}の頻出略語{len(items)}語を、略語 → 間 → 正式名称と意味の順に読み上げます。",
            "related": ["../05_まとめ・横断資料/02_頻出略語・用語集.md"],
            "lines": lines,
        }
        with open(os.path.join(SCRIPTS, f"g{i:02d}_glossary.json"), "w", encoding="utf-8") as f:
            json.dump(script, f, ensure_ascii=False, indent=1)
        print(f"g{i:02d} {cat}: {len(items)}語")


if __name__ == "__main__":
    main()
