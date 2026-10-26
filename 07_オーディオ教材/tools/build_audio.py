#!/usr/bin/env python3
"""台本 JSON（scripts/*.json）から VOICEVOX で音声を生成する。

生成物:
  audio/<name>.mp3                     … 音声（ffmpeg があれば MP3、無ければ WAV）
  transcripts/<name>.md                … 文字起こし
  ../06_インタラクティブ教材/data/audio_index.js … プレーヤー用の一覧と字幕タイミング

使い方:
  1. VOICEVOX エンジンを起動する（既定: http://127.0.0.1:50021）
  2. python3 tools/build_audio.py            # 全エピソード
     python3 tools/build_audio.py ep03       # 指定したものだけ

環境変数:
  VOICEVOX_URL  エンジンのURL
  FFMPEG        ffmpeg のパス（既定: PATH 上の ffmpeg）
"""
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
import wave

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(BASE, "scripts")
AUDIO = os.path.join(BASE, "audio")
TRANSCRIPTS = os.path.join(BASE, "transcripts")
CACHE = os.path.join(BASE, ".cache")
INDEX_JS = os.path.join(os.path.dirname(BASE), "06_インタラクティブ教材", "data", "audio_index.js")

ENGINE = os.environ.get("VOICEVOX_URL", "http://127.0.0.1:50021")
FFMPEG = os.environ.get("FFMPEG") or shutil.which("ffmpeg")

RATE = 24000
GAP_SAME = 0.25   # 同じ話者が続くときの間（秒）
GAP_SWITCH = 0.45  # 話者が交代するときの間（秒）

SPEAKERS = {
    "metan": {"id": 2, "name": "四国めたん", "speed": 1.08},
    "zundamon": {"id": 3, "name": "ずんだもん", "speed": 1.08},
}


def post(path, params, body=None):
    url = ENGINE + path + "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode("utf-8") if body is not None else b""
    req = urllib.request.Request(url, data=data, method="POST", headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as res:
        return res.read()


def synthesize(text, speaker):
    """1発話を合成して 16bit PCM（RATE Hz, mono）の bytes を返す。結果はキャッシュする。"""
    sp = SPEAKERS[speaker]
    key = hashlib.sha1(f"{sp['id']}|{sp['speed']}|{RATE}|{text}".encode("utf-8")).hexdigest()
    path = os.path.join(CACHE, key + ".pcm")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()
    query = json.loads(post("/audio_query", {"text": text, "speaker": sp["id"]}))
    query["speedScale"] = sp["speed"]
    query["outputSamplingRate"] = RATE
    query["outputStereo"] = False
    query["prePhonemeLength"] = 0.05
    query["postPhonemeLength"] = 0.05
    wav = post("/synthesis", {"speaker": sp["id"]}, query)
    with wave.open(io.BytesIO(wav)) as w:
        assert w.getframerate() == RATE and w.getnchannels() == 1 and w.getsampwidth() == 2
        pcm = w.readframes(w.getnframes())
    os.makedirs(CACHE, exist_ok=True)
    with open(path, "wb") as f:
        f.write(pcm)
    return pcm


def silence(sec):
    return b"\x00\x00" * int(RATE * sec)


def build(script_path):
    with open(script_path, encoding="utf-8") as f:
        ep = json.load(f)
    name = os.path.splitext(os.path.basename(script_path))[0]
    chunks, cues = [], []
    t = 0.0
    prev = None
    for i, line in enumerate(ep["lines"]):
        if "pause" in line:
            chunks.append(silence(line["pause"]))
            t += line["pause"]
            continue
        speaker = line["speaker"]
        if prev is not None:
            gap = GAP_SAME if prev == speaker else GAP_SWITCH
            chunks.append(silence(gap))
            t += gap
        pcm = synthesize(line.get("yomi") or line["text"], speaker)
        dur = len(pcm) / 2 / RATE
        cues.append({"s": speaker, "t": line["text"], "start": round(t, 2), "end": round(t + dur, 2)})
        chunks.append(pcm)
        t += dur
        prev = speaker
        print(f"\r  {name}: {i + 1}/{len(ep['lines'])}", end="", flush=True)
    chunks.append(silence(0.8))
    t += 0.8
    print()

    os.makedirs(AUDIO, exist_ok=True)
    wav_path = os.path.join(AUDIO, name + ".wav")
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(chunks))
    audio_file = name + ".wav"
    if FFMPEG:
        mp3_path = os.path.join(AUDIO, name + ".mp3")
        subprocess.run(
            [FFMPEG, "-y", "-loglevel", "error", "-i", wav_path, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(RATE), "-ac", "1", "-b:a", "48k",
             "-metadata", f"title={ep['title']}", "-metadata", "artist=VOICEVOX:四国めたん, VOICEVOX:ずんだもん",
             "-metadata", "album=APLearn 応用情報技術者試験 聞き流し講座", mp3_path],
            check=True,
        )
        os.remove(wav_path)
        audio_file = name + ".mp3"

    write_transcript(name, ep, round(t, 1))
    return {
        "id": ep["id"],
        "file": audio_file,
        "title": ep["title"],
        "summary": ep.get("summary", ""),
        "related": ep.get("related", []),
        "duration": round(t, 1),
        "cues": cues,
    }


def write_transcript(name, ep, duration):
    os.makedirs(TRANSCRIPTS, exist_ok=True)
    m, s = divmod(int(duration), 60)
    out = [f"# {ep['title']}", "", f"> {ep.get('summary', '')}", "",
           f"- 音声: [../audio/{name}.mp3](../audio/{name}.mp3)（約{m}分{s:02d}秒）",
           "- 音声合成: VOICEVOX:四国めたん、VOICEVOX:ずんだもん", ""]
    for line in ep["lines"]:
        if "pause" in line:
            out.append(f"*（{line['pause']:g}秒 考えてみよう）*")
        else:
            out.append(f"**{SPEAKERS[line['speaker']]['name']}**：{line['text']}")
        out.append("")
    with open(os.path.join(TRANSCRIPTS, name + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out))


def main():
    targets = sys.argv[1:]
    files = sorted(fn for fn in os.listdir(SCRIPTS) if fn.endswith(".json"))
    if targets:
        files = [fn for fn in files if any(fn.startswith(t) for t in targets)]

    # 既存の一覧を読み、今回生成したものだけ差し替える
    index = {}
    if os.path.exists(INDEX_JS):
        with open(INDEX_JS, encoding="utf-8") as f:
            src = f.read()
        try:
            for ep in json.loads(src[src.index("["): src.rindex("]") + 1]):
                index[ep["id"]] = ep
        except ValueError:
            pass

    for fn in files:
        ep = build(os.path.join(SCRIPTS, fn))
        index[ep["id"]] = ep
        print(f"  -> {ep['file']} ({ep['duration']}秒)")

    os.makedirs(os.path.dirname(INDEX_JS), exist_ok=True)
    with open(INDEX_JS, "w", encoding="utf-8") as f:
        f.write("// 自動生成: 07_オーディオ教材/tools/build_audio.py\n")
        f.write("window.APL_DATA_AUDIO = ")
        json.dump([index[k] for k in sorted(index)], f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")


if __name__ == "__main__":
    main()
