# 公開サイト（GitHub Pages）の生成

`main` に push すると、GitHub Actions（`.github/workflows/pages.yml`）が `tools/site/build_site.py` でサイトを生成し、GitHub Pages に公開します。

```bash
python3 tools/site/build_site.py --check   # _site/ に生成し、サイト内リンク切れを検査
cd _site && python3 -m http.server 8000    # http://localhost:8000/ で確認
```

必要なもの：`markdown-it-py`（3.x）と `linkify-it-py`。

| 元のファイル | サイトでの扱い |
|---|---|
| `X.md` | `X.html` に変換（共通ヘッダー・パンくず・スタイル `site.css` つき）。`README.md` は `index.html` も作る |
| Markdown 内の `X.md` / `X.md#見出し` へのリンク | `X.html` / `X.html#見出し` に書き換え。見出しのアンカーは GitHub と同じ規則 |
| ` ```mermaid ` のコードブロック | ブラウザで Mermaid（CDN）が図に描画 |
| インタラクティブ教材の HTML | そのままコピー。JS で組み立てる `.md` リンクは `mdlinks.js` がクリック時に `.html` に読み替える |
| その他（MP3・画像・JS など） | そのままコピー |
| README も index.html も無いフォルダ | ファイル一覧ページを自動生成 |
| （全体） | サイト内検索 `search.html`。見出しごとの検索インデックスを `_site_assets/search/{terms,past,core}.json` に出力（用語集は1語ずつ）。開発者向け文書と内容が重複するページ（最重要用語まとめ・分野別索引・科目B 回別ページ）は対象外。画面の処理は `search.js` |

git 管理下のファイルだけを対象にします（`.` で始まるファイル・フォルダは除外）。`_site/` は `.gitignore` 済み。
