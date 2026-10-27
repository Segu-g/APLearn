# インタラクティブ教材 開発ルール

ブラウザで `index.html` を開くだけで動く、オフライン対応の教材です。

## 制約

- **外部ライブラリ・CDN・Webフォントは使わない**（素の HTML / CSS / JavaScript のみ）。
- **`file://` で開いて動くこと**。`fetch()` や ES Modules（`type="module"`）は使わない。データは `data/*.js` に `window.APL_DATA_xxx = [...]` の形で置き、`<script src>` で読み込む。`data/terms.js`（用語ドリル）は `09_用語集/tools/build_terms.py` が生成する。
- 図・グラフは **インライン SVG** を JavaScript で描く（Canvas でもよい）。色は CSS 変数（`var(--accent)` など）を使い、ライト／ダーク両方で読めるようにする。
- スマホ幅（360px）でも横スクロールなしで使えるレイアウトにする。
- 保存が必要な状態（成績・苦手問題など）は `APL.store.get/set`（localStorage を try/catch で包んだもの）を使う。保存できなくても動くこと。

## ページの雛形

```html
<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ページ名</title>
  <link rel="stylesheet" href="../assets/style.css">
</head>
<body data-root="../" data-title="ページ名">
  <main>
    <h1>ページ名</h1>
    <p class="lead">このページで何ができるか（1〜2文）</p>
    ...
  </main>
  <script src="../assets/common.js"></script>
  <script>/* ページ固有の処理 */</script>
</body>
</html>
```

- `data-root` は `index.html` があるフォルダまでの相対パス（`sim/` 配下なら `../`）。
- `common.js` がヘッダ（トップへのリンク・テーマ切替）を自動で挿入する。
- `assets/style.css` のクラス（`.card` `.row` `.field` `.result` `.steps` `.box-ok` `.box-ng` `.box-note` `.tag` `button.primary` など）を使い、ページ固有のスタイルは `<style>` に最小限で書く。

## 学習コンテンツとしての要件

- 計算系ツールは **答えだけでなく途中式（`.steps`）** を表示する。試験で手計算するときの手順と同じ順に書く。
- 「例題を読み込む」ボタンを置き、初見でもすぐ動かせるようにする。
- 関連する Markdown 資料へのリンク（例：`../../01_テクノロジ系/07_ネットワーク.md`）をページ末尾に置く。
