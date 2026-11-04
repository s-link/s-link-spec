# PDFの生成

```sh
python3 -m pip install -r tools/pdf-requirements.txt
python3 tools/build_pdf.py
```

Node.js 22以降とChromiumを使います。Chromiumを自動検出できない場合は、`--chrome /path/to/chromium` を指定します。

コミットを生成元にする場合は、Markdownを先にコミットしてください。PDFの表紙に、それぞれの生成元コミットを記載します。

公開タグを生成元にする場合は `python3 tools/build_pdf.py --source-tag v0.2` のように指定します。生成後、MarkdownとPDFを含むコミットに、そのタグを付けて公開します。

体裁はGitHubで公開した文書版0.1のPDFを基準にしています。本文にはIBM Plex Sans JPを使い、コード用の書体は同PDFに埋め込まれたMenloを使います。フォントは初回生成時に取得し、`~/.cache/s-link-pdf/fonts` に保存します。
