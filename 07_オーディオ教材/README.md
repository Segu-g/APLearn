# オーディオ教材 — 聞き流し講座

VOICEVOX キャラクターの掛け合いで学べる音声教材です。音声は [VOICEVOX](https://voicevox.hiroshiba.jp/) で合成しています。

- **解説講座** 全40回（約223分）：四国めたん先生（解説役）とずんだもん（生徒役）。頻出テーマを1回約5分で。各回の最後にミニクイズつき
- **科目B攻略編** 全11回（約97分）：冥鳴ひまり（解説役）と春日部つむぎ（生徒役）。科目B の11分野を1回1分野ずつ、出題傾向・解き方・過去問1題のケーススタディで
- **用語聞き流し** 全14本（約49分）：略語 → 少し間 → 正式名称と意味、の順に読み上げ。略語を聞いたら意味を思い浮かべてください（奇数回はめたん・ずんだもん、偶数回はひまり・つむぎ）

## 聞き方

- **おすすめ**：[インタラクティブ教材の「聞き流し講座」](../06_インタラクティブ教材/audio.html) をブラウザで開く。字幕（文字起こし）が再生位置に合わせてハイライトされ、セリフをクリックするとそこから再生できます。倍速再生・続きから再生にも対応しています。
- スマホや音楽アプリで聞く：`audio/` フォルダの MP3 をコピーしてください。`audio/playlist.m3u`（解説講座）、`audio/playlist_kamoku_b.m3u`（科目B攻略編）、`audio/playlist_glossary.m3u`（用語聞き流し）はプレイリストです。

## 解説講座

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
| 16 | [第16回 法務](transcripts/ep16_law.md) | 著作権と特許権の違い、職務著作と委託開発の権利、個人情報保護法の要点、請負・準委任・派遣と偽装請負、2026年1月施行の中小受託取引適正化法（旧：下請法）を整理します。 | 4:49 | [▶ mp3](audio/ep16_law.mp3) |
| 17 | [第17回 アルゴリズムと擬似言語の読み方](transcripts/ep17_algorithm-pseudocode.md) | 科目B問3（プログラミング）に向けて、IPA擬似言語の約束ごと、トレース表の作り方、配列の要素番号と境界条件、再帰の追い方を学びます。 | 5:30 | [▶ mp3](audio/ep17_algorithm-pseudocode.mp3) |
| 18 | [第18回 データ構造と計算量](transcripts/ep18_data-structure.md) | スタックとキュー、連結リスト、2分探索木、ヒープ、ハッシュ表の特徴と使いどころ、O記法による計算量の見積り方を学びます。 | 6:00 | [▶ mp3](audio/ep18_data-structure.mp3) |
| 19 | [第19回 論理演算・確率・待ち行列](transcripts/ep19_logic-probability-queue.md) | AND・OR・XORとビットマスク、シフト演算、ド・モルガンの法則、場合の数と確率、M/M/1待ち行列の利用率・待ち時間・応答時間の計算を学びます。 | 6:29 | [▶ mp3](audio/ep19_logic-probability-queue.mp3) |
| 20 | [第20回 排他制御・デッドロック・セマフォ](transcripts/ep20_os-exclusive-control.md) | 共有資源の同時更新で起こる問題とクリティカルセクション、セマフォのP操作・V操作と初期値の意味、デッドロックの4条件と予防・回避・検出の方法を学びます。 | 4:56 | [▶ mp3](audio/ep20_os-exclusive-control.mp3) |
| 21 | [第21回 システム構成：クラウド・仮想化・コンテナ・性能評価](transcripts/ep21_cloud-virtualization.md) | IaaS・PaaS・SaaSの管理範囲、スケールアップとスケールアウト、ハイパーバイザ型とコンテナ型の違い、レスポンスタイムとスループット、ボトルネックの計算を学びます。 | 5:42 | [▶ mp3](audio/ep21_cloud-virtualization.mp3) |
| 22 | [第22回 ネットワーク：DNS・DHCP・NAT・メール・IPv6・ルーティング](transcripts/ep22_network-protocols.md) | DHCPとリレーエージェント、DNSの役割と主なレコード、NATとNAPT、メールの送受信プロトコル、IPv6の特徴と省略表記、ロンゲストマッチとルーティングプロトコルを学びます。 | 5:54 | [▶ mp3](audio/ep22_network-protocols.mp3) |
| 23 | [第23回 ISMS・リスクマネジメント・CSIRTとインシデント対応](transcripts/ep23_isms-incident.md) | 脅威・脆弱性・リスクの関係、ISMSの規格とPDCA、リスクアセスメントと4つのリスク対応、年間予想損失額、CSIRTとSOCの違い、インシデント対応の流れと初動を学びます。 | 5:45 | [▶ mp3](audio/ep23_isms-incident.mp3) |
| 24 | [第24回 オブジェクト指向とUML](transcripts/ep24_uml-oop.md) | カプセル化・継承・多態性、オーバーライドとオーバーロード、汎化・集約・コンポジションと多重度、UMLの主な図の使い分けとユースケースの包含・拡張を学びます。 | 5:06 | [▶ mp3](audio/ep24_uml-oop.mp3) |
| 25 | [第25回 アジャイル・スクラム・DevOps と見積り（FP法）](transcripts/ep25_agile-devops.md) | スクラムの役割・イベント・作成物、ベロシティによるリリース時期の見積り、XPのプラクティス、DevOpsとCI/CD、ファンクションポイント法による規模見積りの計算を学びます。 | 5:37 | [▶ mp3](audio/ep25_agile-devops.mp3) |
| 26 | [第26回 ハードウェア・組込みシステム（論理回路、センサ、RTOS）](transcripts/ep26_hardware-embedded.md) | NANDゲートと半加算器・全加算器、組合せ回路と順序回路、センサからアクチュエータまでの流れとA/D変換・PWMの計算、RTOSの優先度スケジューリングと優先度逆転、ウォッチドッグタイマ、フェールセーフを学びます。 | 5:26 | [▶ mp3](audio/ep26_hardware-embedded.mp3) |
| 27 | [第27回 ユーザーインタフェース・情報メディア・AIの基礎](transcripts/ep27_ui-media-ai.md) | 画面部品の使い分けとユーザビリティ・アクセシビリティ、画像のデータ量と可逆・非可逆圧縮、VRとAR、機械学習の3つの学び方、過学習、適合率と再現率、生成AIの注意点を学びます。 | 5:28 | [▶ mp3](audio/ep27_ui-media-ai.mp3) |
| 28 | [第28回 科目Bの記述式で点を取る書き方](transcripts/ep28_kamoku-b-writing.md) | 設問の聞き方に合わせた文末の型（〜ため、〜するため、〜おそれがある）、指定字数の7〜9割を目安にした書き方、本文の語句を使うコツ、問1情報セキュリティの答え方の型とCBTでの注意点を学びます。 | 5:39 | [▶ mp3](audio/ep28_kamoku-b-writing.mp3) |
| 29 | [第29回 プロジェクトマネジメント：PMBOK・WBS・リスク対応・調達と契約](transcripts/ep29_pm-scope-risk.md) | PMBOK第6版と第7版の違い、スコープとWBS（ワークパッケージ・100%ルール）、期待金額価値とリスク対応戦略（脅威と好機）、定額契約と実費償還契約のリスク分担を整理します。 | 6:14 | [▶ mp3](audio/ep29_pm-scope-risk.mp3) |
| 30 | [第30回 サービスマネジメント：SLA・可用性・キャパシティ・バックアップ](transcripts/ep30_itil-sla-availability.md) | ITIL 4とJIS Q 20000の違い、SLAの条件の読み方、可用性を高める方法、キャパシティ管理の増設時期の計算、RPO・RTOと代替拠点、差分・増分バックアップの復元手順を整理します。 | 6:54 | [▶ mp3](audio/ep30_itil-sla-availability.mp3) |
| 31 | [第31回 内部統制・ITガバナンス・監査証拠と監査手続](transcripts/ep31_internal-control-governance.md) | COSOとJ-SOXの目的と構成要素、IT全般統制とIT業務処理統制の見分け方、ITガバナンスのEDMモデル、十分かつ適切な監査証拠、具体的な監査手続の書き方、整備状況と運用状況の違い、CAATの技法を整理します。 | 6:15 | [▶ mp3](audio/ep31_internal-control-governance.mp3) |
| 32 | [第32回 システム戦略とシステム企画：EA・BPR・DX・RFI/RFP・要件定義](transcripts/ep32_system-strategy-planning.md) | 情報システム戦略と全体最適、EAの4つの体系、BPR・BPM・BPOとRPAの違い、DXの3段階、システム化構想から要件定義までの流れ、機能要件と非機能要件、RFI・RFP・RFQの順序と提案の評価を整理します。 | 5:52 | [▶ mp3](audio/ep32_system-strategy-planning.mp3) |
| 33 | [第33回 マーケティング（4P/4C・STP・PLC・価格戦略）とバランススコアカード](transcripts/ep33_marketing.md) | STPから4Pへのマーケティングの流れ、4Pと4Cの対応、プロダクトライフサイクルの各時期の戦略、スキミングとペネトレーションなどの価格戦略、バランススコアカードの4つの視点とKGI・CSF・KPIの関係を整理します。 | 5:39 | [▶ mp3](audio/ep33_marketing.mp3) |
| 34 | [第34回 技術戦略とビジネスインダストリ（MOT、イノベーション、IoT、フィンテック、e-ビジネス）](transcripts/ep34_tech-strategy-industry.md) | MOTと技術ロードマップ、魔の川・死の谷・ダーウィンの海、イノベーションのジレンマやキャズムなどのイノベーション用語、IoT・CPS・デジタルツイン、フィンテックと電子商取引の用語を整理します。 | 5:34 | [▶ mp3](audio/ep34_tech-strategy-industry.mp3) |
| 35 | [第35回 OR・IE：線形計画法・在庫管理（EOQ）・意思決定・需要予測](transcripts/ep35_or-ie.md) | 線形計画法で利益が最大になる組合せを頂点から探す手順、定量発注方式と定期発注方式、発注点と経済的発注量（EOQ）の計算、マクシマックス・マクシミン・期待値原理の違い、移動平均法と指数平滑法を、口頭でたどれる数値で練習します。 | 6:21 | [▶ mp3](audio/ep35_or-ie.mp3) |
| 36 | [第36回 品質管理：QC七つ道具・新QC七つ道具・管理図](transcripts/ep36_quality-control.md) | 数値データを扱うQC七つ道具と、言語データを扱う新QC七つ道具の用途の違い、管理図で異常と判断する条件（管理限界の外・連・傾向・周期）、特性要因図と連関図法などの見分け方を、図を見なくても分かる言い方で整理します。 | 5:39 | [▶ mp3](audio/ep36_quality-control.mp3) |
| 37 | [第37回 会計：財務諸表・減価償却・在庫評価・キャッシュフロー](transcripts/ep37_accounting-advanced.md) | 損益計算書の5つの利益と費用の区分、貸借対照表の構造、定額法と定率法の減価償却、先入先出法・移動平均法・総平均法による在庫評価、キャッシュフロー計算書の3区分と間接法の調整を、口頭でたどれる数値で学びます。 | 6:37 | [▶ mp3](audio/ep37_accounting-advanced.mp3) |
| 38 | [第38回 知的財産権の深掘り（著作権・特許・職務著作・ライセンス・不正競争防止法）](transcripts/ep38_ip-law.md) | 産業財産権の存続期間、著作者人格権と不行使特約、プログラムの複製物の所有者ができること、職務著作と職務発明の違い、専用実施権と通常実施権、ソフトウェアのライセンス形態とOSS、営業秘密の3要件と限定提供データを整理します。 | 6:21 | [▶ mp3](audio/ep38_ip-law.mp3) |
| 39 | [第39回 労働・取引関連法と標準化（派遣・請負・準委任、取適法、フリーランス法、JIS/ISO）](transcripts/ep39_labor-contract-standard.md) | 契約不適合責任と準委任の2つの型、労働者派遣法の主なルール、36協定と裁量労働制、中小受託取引適正化法（取適法）の対象と委託事業者の義務、フリーランス法との違い、デジュレ・デファクト・フォーラム標準と主な標準化団体・規格を整理します。 | 6:26 | [▶ mp3](audio/ep39_labor-contract-standard.mp3) |
| 40 | [第40回 直前総まとめ：ひっかけやすい対の用語と当日の注意（CBT）](transcripts/ep40_final-review.md) | 最終回。ロールバックとロールフォワード、RPOとRTO、IDSとIPS、フェールセーフ・フェールソフト・フールプルーフ、スタブとドライバ、検証と妥当性確認など、対になる用語を一気に確認し、計算ミスの防ぎ方とCBT受験当日の注意点で締めくくります。 | 6:04 | [▶ mp3](audio/ep40_final-review.mp3) |

## 科目B攻略編

| 回 | タイトル（文字起こし） | 内容 | 長さ | 音声 |
|---|---|---|---|---|
| 01 | [科目B攻略1 情報セキュリティ](transcripts/b01_security.md) | 科目B攻略編の第1回。必須の問1情報セキュリティについて、8回分の出題傾向、設問を先に読む解き方、令和6年度秋期のパスワード管理の問題を使ったケーススタディ、記述の型とひっかけを学びます。 | 9:35 | [▶ mp3](audio/b01_security.mp3) |
| 02 | [科目B攻略2 経営戦略](transcripts/b02_strategy.md) | 科目B問2経営戦略の特徴と選び方、8回分の出題傾向、SWOTを内外・プラスマイナスの2軸で読む解き方を学び、令和4年度秋期問2で強み・機会の記述と変動費率の計算を練習します。 | 7:57 | [▶ mp3](audio/b02_strategy.mp3) |
| 03 | [科目B攻略3 プログラミング](transcripts/b03_programming.md) | 科目B問3プログラミング（アルゴリズム）の特徴と選び方、8回分の出題傾向、本文の手順とプログラムを対応づける解き方、メモ用紙でのトレース表の練習法を、令和6年度春期のダイクストラ法の問題を例に学びます。 | 8:54 | [▶ mp3](audio/b03_programming.mp3) |
| 04 | [科目B攻略4 システムアーキテクチャ](transcripts/b04_architecture.md) | 科目B問4システムアーキテクチャの出題傾向と解き方を学びます。令和7年度春期のBEMSのクラウド移行を例に、SLAの稼働率から障害時間の上限と減額を口頭で計算し、スケールアウトとスケールアップ、境界値のひっかけも確認します。 | 9:37 | [▶ mp3](audio/b04_architecture.mp3) |
| 05 | [科目B攻略5 ネットワーク](transcripts/b05_network.md) | 科目B問5ネットワークの選び方、出題傾向、パケットの通り道を追う解き方を学びます。ケーススタディは令和4年度春期の「ネットワークの構成変更」で、IPsecトンネルの送信元やプロキシ経由の宛先を確認します。 | 8:33 | [▶ mp3](audio/b05_network.mp3) |
| 06 | [科目B攻略6 データベース](transcripts/b06_database.md) | 科目B問6データベースの特徴と出題傾向、E-R図の多重度を本文から決める手順、内部結合と外部結合の使い分けを、令和5年度春期の問6で学びます。 | 9:45 | [▶ mp3](audio/b06_database.mp3) |
| 07 | [科目B攻略7 組込みシステム開発](transcripts/b07_embedded.md) | 状態遷移・タスク間通知・タイマとセンサの計算という問7の3本柱と、読む順番を学びます。令和6年度春期のコーヒーマシンの問題をケーススタディに、チャタリング対策やタスク優先度の答え方を確認します。 | 7:51 | [▶ mp3](audio/b07_embedded.mp3) |
| 08 | [科目B攻略8 情報システム開発](transcripts/b08_sysdev.md) | 問8 情報システム開発の特徴と向き不向き、8回分の出題傾向（オブジェクト指向・クラス図、ブランチ運用とテスト、設計レビュー）、令和6年度秋期のオブジェクト指向設計のケーススタディ、オーバーライドと集約・コンポジションなどの頻出用語と境界値分析を学びます。 | 8:35 | [▶ mp3](audio/b08_sysdev.mp3) |
| 09 | [科目B攻略9 プロジェクトマネジメント](transcripts/b09_pm.md) | 科目B問9プロジェクトマネジメントの出題傾向と読み方、PMの行動を「誰に・何を・なぜ」で答える型を、令和5年度春期の移行プロジェクトの過去問で学びます。契約形態やリスク対応戦略のひっかけも整理します。 | 8:40 | [▶ mp3](audio/b09_pm.mp3) |
| 10 | [科目B攻略10 サービスマネジメント](transcripts/b10_service.md) | 科目B問10サービスマネジメントの特徴と8回分の出題傾向、表の手順と本文を突き合わせる解き方を学び、令和5年度春期の可用性管理の問題で稼働率から許容停止時間を求める計算を口頭でたどります。 | 8:55 | [▶ mp3](audio/b10_service.mp3) |
| 11 | [科目B攻略11 システム監査](transcripts/b11_audit.md) | 科目B問11システム監査の特徴と選び方、8回分の出題傾向、指示と本文を結び付ける解き方を学びます。令和7年度秋期の過去問で監査手続・監査証拠（記録とインタビュー、照合する資料）の考え方を確認し、全11分野の選び方を振り返ります。 | 8:38 | [▶ mp3](audio/b11_audit.mp3) |

## 用語聞き流し

| No | タイトル（文字起こし） | 内容 | 長さ | 音声 |
|---|---|---|---|---|
| 01 | [用語聞き流し1 基礎理論・AI](transcripts/g01_glossary.md) | 基礎理論・AIの頻出略語12語を、略語 → 間 → 正式名称と意味の順に読み上げます。 | 2:24 | [▶ mp3](audio/g01_glossary.mp3) |
| 02 | [用語聞き流し2 コンピュータ構成要素・ハードウェア](transcripts/g02_glossary.md) | コンピュータ構成要素・ハードウェアの頻出略語20語を、略語 → 間 → 正式名称と意味の順に読み上げます。 | 3:07 | [▶ mp3](audio/g02_glossary.mp3) |
| 03 | [用語聞き流し3 システム構成要素・ソフトウェア](transcripts/g03_glossary.md) | システム構成要素・ソフトウェアの頻出略語21語を、略語 → 間 → 正式名称と意味の順に読み上げます。 | 3:40 | [▶ mp3](audio/g03_glossary.mp3) |
| 04 | [用語聞き流し4 データベース](transcripts/g04_glossary.md) | データベースの頻出略語18語を、略語 → 間 → 正式名称と意味の順に読み上げます。 | 3:04 | [▶ mp3](audio/g04_glossary.mp3) |
| 05 | [用語聞き流し5 ネットワーク](transcripts/g05_glossary.md) | ネットワークの頻出略語36語を、略語 → 間 → 正式名称と意味の順に読み上げます。 | 5:58 | [▶ mp3](audio/g05_glossary.mp3) |
| 06 | [用語聞き流し6 情報セキュリティ](transcripts/g06_glossary.md) | 情報セキュリティの頻出略語41語を、略語 → 間 → 正式名称と意味の順に読み上げます。 | 6:38 | [▶ mp3](audio/g06_glossary.mp3) |
| 07 | [用語聞き流し7 システム開発技術](transcripts/g07_glossary.md) | システム開発技術の頻出略語17語を、略語 → 間 → 正式名称と意味の順に読み上げます。 | 2:58 | [▶ mp3](audio/g07_glossary.mp3) |
| 08 | [用語聞き流し8 プロジェクトマネジメント](transcripts/g08_glossary.md) | プロジェクトマネジメントの頻出略語19語を、略語 → 間 → 正式名称と意味の順に読み上げます。 | 2:57 | [▶ mp3](audio/g08_glossary.mp3) |
| 09 | [用語聞き流し9 サービスマネジメント](transcripts/g09_glossary.md) | サービスマネジメントの頻出略語18語を、略語 → 間 → 正式名称と意味の順に読み上げます。 | 3:05 | [▶ mp3](audio/g09_glossary.mp3) |
| 10 | [用語聞き流し10 システム監査・内部統制](transcripts/g10_glossary.md) | システム監査・内部統制の頻出略語7語を、略語 → 間 → 正式名称と意味の順に読み上げます。 | 1:29 | [▶ mp3](audio/g10_glossary.mp3) |
| 11 | [用語聞き流し11 システム戦略・調達](transcripts/g11_glossary.md) | システム戦略・調達の頻出略語20語を、略語 → 間 → 正式名称と意味の順に読み上げます。 | 3:17 | [▶ mp3](audio/g11_glossary.mp3) |
| 12 | [用語聞き流し12 経営戦略・マーケティング](transcripts/g12_glossary.md) | 経営戦略・マーケティングの頻出略語27語を、略語 → 間 → 正式名称と意味の順に読み上げます。 | 4:18 | [▶ mp3](audio/g12_glossary.mp3) |
| 13 | [用語聞き流し13 企業活動・会計](transcripts/g13_glossary.md) | 企業活動・会計の頻出略語21語を、略語 → 間 → 正式名称と意味の順に読み上げます。 | 3:26 | [▶ mp3](audio/g13_glossary.mp3) |
| 14 | [用語聞き流し14 法務・標準化](transcripts/g14_glossary.md) | 法務・標準化の頻出略語14語を、略語 → 間 → 正式名称と意味の順に読み上げます。 | 2:26 | [▶ mp3](audio/g14_glossary.mp3) |

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
