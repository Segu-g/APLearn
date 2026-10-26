#!/usr/bin/env python3
"""07_オーディオ教材/README.md とプレイリスト（audio/*.m3u）を、生成済みの一覧データから作り直す。

使い方: python3 tools/make_readme.py   （build_audio.py の実行後に）
"""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_JS = os.path.join(os.path.dirname(BASE), "06_インタラクティブ教材", "data", "audio_index.js")


def fmt(sec):
    m, s = divmod(int(sec), 60)
    return f"{m}:{s:02d}"


def main():
    with open(INDEX_JS, encoding="utf-8") as f:
        src = f.read()
    eps = json.loads(src[src.index("["): src.rindex("]") + 1])
    lectures = [e for e in eps if e["id"].startswith("ep")]
    kamoku_b = [e for e in eps if e["id"].startswith("b")]
    glossary = [e for e in eps if e["id"].startswith("g")]

    def rows(items):
        out = []
        for e in items:
            name = os.path.splitext(e["file"])[0]
            out.append(f"| {e['id'].lstrip('epbg')} | [{e['title']}](transcripts/{name}.md) | {e['summary']} | {fmt(e['duration'])} | [▶ mp3](audio/{e['file']}) |")
        return "\n".join(out)

    def playlist(items, path):
        lines = ["#EXTM3U"]
        for e in items:
            lines += [f"#EXTINF:{int(e['duration'])},{e['title']}", e["file"]]
        with open(os.path.join(BASE, "audio", path), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    playlist(lectures, "playlist.m3u")
    playlist(kamoku_b, "playlist_kamoku_b.m3u")
    playlist(glossary, "playlist_glossary.m3u")
    total_l = sum(e["duration"] for e in lectures) / 60
    total_b = sum(e["duration"] for e in kamoku_b) / 60
    total_g = sum(e["duration"] for e in glossary) / 60

    body = f"""# オーディオ教材 — 聞き流し講座

VOICEVOX キャラクターの掛け合いで学べる音声教材です。音声は [VOICEVOX](https://voicevox.hiroshiba.jp/) で合成しています。

- **解説講座** 全{len(lectures)}回（約{total_l:.0f}分）：四国めたん先生（解説役）とずんだもん（生徒役）。頻出テーマを1回約5分で。各回の最後にミニクイズつき
- **科目B攻略編** 全{len(kamoku_b)}回（約{total_b:.0f}分）：冥鳴ひまり（解説役）と春日部つむぎ（生徒役）。科目B の11分野を1回1分野ずつ、出題傾向・解き方・過去問1題のケーススタディで
- **用語聞き流し** 全{len(glossary)}本（約{total_g:.0f}分）：略語 → 少し間 → 正式名称と意味、の順に読み上げ。略語を聞いたら意味を思い浮かべてください（奇数回はめたん・ずんだもん、偶数回はひまり・つむぎ）

## 聞き方

- **おすすめ**：[インタラクティブ教材の「聞き流し講座」](../06_インタラクティブ教材/audio.html) をブラウザで開く。字幕（文字起こし）が再生位置に合わせてハイライトされ、セリフをクリックするとそこから再生できます。倍速再生・続きから再生にも対応しています。
- スマホや音楽アプリで聞く：`audio/` フォルダの MP3 をコピーしてください。`audio/playlist.m3u`（解説講座）、`audio/playlist_kamoku_b.m3u`（科目B攻略編）、`audio/playlist_glossary.m3u`（用語聞き流し）はプレイリストです。

## 解説講座

| 回 | タイトル（文字起こし） | 内容 | 長さ | 音声 |
|---|---|---|---|---|
{rows(lectures)}

## 科目B攻略編

| 回 | タイトル（文字起こし） | 内容 | 長さ | 音声 |
|---|---|---|---|---|
{rows(kamoku_b)}

## 用語聞き流し

| No | タイトル（文字起こし） | 内容 | 長さ | 音声 |
|---|---|---|---|---|
{rows(glossary)}

## 音声を作り直す・追加する

台本（`scripts/*.json`）を編集して、VOICEVOX エンジンを起動した状態で次を実行します。合成結果は `.cache/` にキャッシュされるので、変更した行だけが再合成されます。

```bash
# VOICEVOX エンジン（https://github.com/VOICEVOX/voicevox_engine/releases）を起動しておく
python3 07_オーディオ教材/tools/build_audio.py              # 全エピソード
python3 07_オーディオ教材/tools/build_audio.py ep03         # 第3回だけ
python3 07_オーディオ教材/tools/make_glossary_scripts.py    # 略語集から用語聞き流しの台本を作り直す
python3 07_オーディオ教材/tools/make_readme.py              # この README とプレイリストを更新
```

- `ffmpeg` が PATH にあれば MP3、なければ WAV で出力します（環境変数 `FFMPEG` でパス指定も可）。
- 台本の書き方は [README_DEV.md](README_DEV.md) を参照してください。誤読する語は `yomi` に読みを書きます。

## クレジット・利用条件

- 音声合成：**VOICEVOX:四国めたん**、**VOICEVOX:ずんだもん**、**VOICEVOX:春日部つむぎ**、**VOICEVOX:冥鳴ひまり**
- VOICEVOX 本体および各キャラクターの利用規約に従ってください。音声を公開・配布する場合は、上記のクレジット表記が必要です。
  - [VOICEVOX 利用規約](https://voicevox.hiroshiba.jp/term/)
  - [ずんだもん・四国めたん 利用規約（東北ずん子・ずんだもんプロジェクト）](https://zunko.jp/con_ongen_kiyaku.html)
  - [春日部つむぎ 利用規約](https://tsumugi-official.studio.site/rule)
  - [冥鳴ひまり 利用規約](https://meimeihimari.wixsite.com/himari/terms-of-use)
"""
    with open(os.path.join(BASE, "README.md"), "w", encoding="utf-8") as f:
        f.write(body)
    print(f"README: 講座{len(lectures)}回 / 科目B{len(kamoku_b)}回 / 用語{len(glossary)}本")


if __name__ == "__main__":
    main()
