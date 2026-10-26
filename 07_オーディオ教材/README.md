# オーディオ教材 — 聞き流し講座

四国めたん先生（解説役）とずんだもん（生徒役）の掛け合いで、頻出テーマを1回約5分で学べる音声教材です。音声は [VOICEVOX](https://voicevox.hiroshiba.jp/) で合成しています。

## 聞き方

- **おすすめ**：[インタラクティブ教材の「聞き流し講座」](../06_インタラクティブ教材/audio.html) をブラウザで開く。字幕（文字起こし）が再生位置に合わせてハイライトされ、セリフをクリックするとそこから再生できます。倍速再生・続きから再生にも対応しています。
- スマホや音楽アプリで聞く：`audio/` フォルダの MP3 をコピーしてください。`audio/playlist.m3u` は全16回を順に再生するプレイリストです。
- 各回の最後に **ミニクイズ** があります。問題のあとの無音の間に、答えを考えてみてください。

## エピソード一覧

| 回 | タイトル（文字起こし） | 内容 | 長さ | 音声 |
|---|---|---|---|---|
| 01 | [第1回 試験の全体像とCBT](transcripts/ep01_exam-overview.md) | 応用情報技術者試験の科目Aと科目Bの形式、科目Bの選択のしかた、合格基準、CBT受験の注意点と勉強の進め方をつかみます。 | 5:24 | [▶ mp3](audio/ep01_exam-overview.mp3) |
| 02 | [第2回 基数変換と2の補数](transcripts/ep02_radix-complement.md) | 10進数と2進数・16進数の変換手順と、負の数を表す2の補数の作り方・表現範囲を、口頭でたどれる例で学びます。 | 6:15 | [▶ mp3](audio/ep02_radix-complement.mp3) |
| 03 | [第3回 稼働率とRAID](transcripts/ep03_availability-raid.md) | MTBF・MTTRから稼働率を求める方法、直列・並列システムの稼働率、RAIDの各レベルの特徴と実効容量を学びます。 | 5:02 | [▶ mp3](audio/ep03_availability-raid.mp3) |
| 04 | [第4回 CPUの性能とキャッシュ](transcripts/ep04_cpu-cache.md) | クロック周波数・CPI・MIPSの関係、キャッシュメモリの実効アクセス時間、パイプライン処理の所要サイクル数を、簡単な数値で計算できるようにします。 | 4:50 | [▶ mp3](audio/ep04_cpu-cache.mp3) |
| 05 | [第5回 OS：スケジューリングと仮想記憶・ページ置換](transcripts/ep05_os-virtual-memory.md) | タスクの3つの状態とスケジューリング方式、仮想記憶とページフォールト、FIFOとLRUによるページ置換の違いを学びます。 | 5:12 | [▶ mp3](audio/ep05_os-virtual-memory.mp3) |
| 06 | [第6回 データベース：正規化とSQL](transcripts/ep06_db-normalization-sql.md) | 関数従属と第1〜第3正規形の考え方、SQLの句の実行順、WHEREとHAVINGの違い、NULLの扱いと結合の種類を学びます。 | 4:58 | [▶ mp3](audio/ep06_db-normalization-sql.mp3) |
| 07 | [第7回 トランザクションと障害回復](transcripts/ep07_db-transaction.md) | ACID特性、ロストアップデートとロック（共有・専有、2相ロック、デッドロック）、ログを使ったロールバックとロールフォワードによる障害回復を学びます。 | 4:41 | [▶ mp3](audio/ep07_db-transaction.mp3) |
| 08 | [第8回 ネットワーク：TCP/IPとサブネット](transcripts/ep08_network-subnet.md) | TCP/IPモデルの4つの層、TCPとUDPの違い、IPv4アドレスとサブネットマスク、ホスト数・ネットワークアドレス・ブロードキャストアドレスの求め方を学びます。 | 5:14 | [▶ mp3](audio/ep08_network-subnet.mp3) |
| 09 | [第9回 暗号とデジタル署名・PKI](transcripts/ep09_crypto-pki.md) | 共通鍵暗号と公開鍵暗号、ハイブリッド暗号、ハッシュ関数、デジタル署名、PKIと証明書の失効確認を、「どの鍵で何をするか」を軸に整理します。 | 5:30 | [▶ mp3](audio/ep09_crypto-pki.mp3) |
| 10 | [第10回 攻撃手法と対策](transcripts/ep10_web-attacks.md) | SQLインジェクション、XSS、CSRF、セッション固定化、パスワードリスト攻撃、ランサムウェアについて、攻撃の仕組みと根本的な対策をセットで覚えます。 | 4:48 | [▶ mp3](audio/ep10_web-attacks.mp3) |
| 11 | [第11回 認証とネットワークセキュリティ](transcripts/ep11_auth-network-security.md) | 多要素認証、TLS、ファイアウォール・WAF・IDS・IPS、送信ドメイン認証（SPF・DKIM・DMARC）、ゼロトラストの役割の違いを整理します。 | 5:22 | [▶ mp3](audio/ep11_auth-network-security.mp3) |
| 12 | [第12回 開発プロセスとテスト技法](transcripts/ep12_dev-test.md) | ウォーターフォール・V字・プロトタイピング・アジャイルの特徴と、テスト工程、スタブとドライバ、ホワイトボックス・ブラックボックスの技法を学びます。 | 4:32 | [▶ mp3](audio/ep12_dev-test.mp3) |
| 13 | [第13回 プロジェクトマネジメント：クリティカルパスとEVM](transcripts/ep13_pm-evm-cpm.md) | アローダイアグラムのクリティカルパスと余裕日数、スケジュール短縮の2手法、EVMのPV・EV・ACと差異・効率指数の計算を、口頭でたどれる数値で練習します。 | 5:00 | [▶ mp3](audio/ep13_pm-evm-cpm.mp3) |
| 14 | [第14回 サービスマネジメントとシステム監査](transcripts/ep14_service-audit.md) | SLA・OLA・UCの違い、稼働率と許容停止時間、インシデント管理と問題管理、変更・構成・リリース管理、システム監査の独立性・監査証拠・フォローアップを整理します。 | 4:36 | [▶ mp3](audio/ep14_service-audit.mp3) |
| 15 | [第15回 経営戦略と会計](transcripts/ep15_strategy-accounting.md) | SWOT分析とPPMで事業を整理する考え方と、損益分岐点・安全余裕率の計算、ROE・ROA・流動比率・自己資本比率などの財務指標を学びます。 | 4:57 | [▶ mp3](audio/ep15_strategy-accounting.mp3) |
| 16 | [第16回 法務](transcripts/ep16_law.md) | 著作権と特許権の違い、職務著作と委託開発の権利、個人情報保護法の要点、請負・準委任・派遣と偽装請負、2026年1月施行の中小受託取引適正化法（旧：下請法）を整理します。 | 4:42 | [▶ mp3](audio/ep16_law.mp3) |

## 音声を作り直す・追加する

台本（`scripts/*.json`）を編集して、VOICEVOX エンジンを起動した状態で次を実行します。合成結果は `.cache/` にキャッシュされるので、変更した行だけが再合成されます。

```bash
# VOICEVOX エンジン（https://github.com/VOICEVOX/voicevox_engine/releases）を起動しておく
python3 07_オーディオ教材/tools/build_audio.py          # 全エピソード
python3 07_オーディオ教材/tools/build_audio.py ep03     # 第3回だけ
```

- `ffmpeg` が PATH にあれば MP3、なければ WAV で出力します（環境変数 `FFMPEG` でパス指定も可）。
- 台本の書き方は [README_DEV.md](README_DEV.md) を参照してください。誤読する語は `yomi` に読みを書きます。

## クレジット・利用条件

- 音声合成：**VOICEVOX:四国めたん**、**VOICEVOX:ずんだもん**
- VOICEVOX 本体および各キャラクターの利用規約に従ってください。音声を公開・配布する場合は、上記のクレジット表記が必要です。
  - [VOICEVOX 利用規約](https://voicevox.hiroshiba.jp/term/)
  - [ずんだもん・四国めたん 利用規約（東北ずん子・ずんだもんプロジェクト）](https://zunko.jp/con_ongen_kiyaku.html)
