#!/usr/bin/env python3
"""Build the combined DRAFT PDF in the style of the GitHub v0.1 PDF.

Requires Node.js 22+, Chromium, and pdf-requirements.txt. Fonts are cached
outside the repository. Markdown sources must match their recorded commits.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import quote, unquote, urlsplit
from urllib.request import urlopen

import fitz
from markdown_it import MarkdownIt
from markdown_it.token import Token

ROOT = Path(__file__).resolve().parents[1]
DOCS = [Path('S-LINK2.0/S-LINK2.0-規格書.md'), Path('S-LINK2.0/S-LINK2.0-機能表.md')]
REFERENCE = '5e82a056166612e8f42d27940da62dbc424cc032'
PDF_PATH = Path('S-LINK2.0/S-LINK2.0-規格書・機能表.pdf')
# IBM/plex commit 71f558992315a12ca1f06a2215d57962a1992162, OFL fonts.
FONT_BLOBS = {'Regular': '226ec05eb0032434f82b5fa0a69d8c6ca72f439e', 'Bold': '7861e098f6a069c696edd806a406ad3a8ccb875d'}
REPOSITORY = 'https://github.com/s-link/s-link-spec'
WIDTHS = [7.5, 8.5, 7, 8, 5, 6, 6, 10.5, 4.5, 11, 7, 19]


def git(*args: str) -> bytes:
    return subprocess.check_output(['git', *args], cwd=ROOT)


def fonts(cache: Path) -> tuple[str, str]:
    cache.mkdir(parents=True, exist_ok=True)
    css = []
    for style, weight in [('Regular', 400), ('Bold', 700)]:
        path = cache / f'IBMPlexSansJP-{style}.ttf'
        if not path.exists():
            endpoint = f'repos/IBM/plex/git/blobs/{FONT_BLOBS[style]}'
            if shutil.which('gh'):
                payload = json.loads(subprocess.check_output(['gh', 'api', endpoint], timeout=30))
            else:
                with urlopen(f'https://api.github.com/{endpoint}', timeout=30) as response:
                    payload = json.load(response)
            path.write_bytes(base64.b64decode(payload['content']))
        raw = path.read_bytes()
        blob = hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
        if blob != FONT_BLOBS[style]:
            raise ValueError(f'Unexpected font contents: {path}')
        css.append(f"@font-face {{font-family:SlinkJP; font-weight:{weight}; src:url('{path.as_uri()}')}}")
    reference = fitz.open(stream=git('show', f'{REFERENCE}:{PDF_PATH}'), filetype='pdf')
    seen, families, counts = set(), [], {400: 0, 700: 0}
    for page in reference:
        for info in page.get_fonts():
            xref, _, _, name, *_ = info
            if xref in seen or 'Menlo' not in name:
                continue
            seen.add(xref)
            name, extension, _, raw = reference.extract_font(xref)
            weight = 700 if 'Bold' in name else 400
            family = f'ReferenceMono{counts[weight]}'
            counts[weight] += 1
            if family not in families:
                families.append(family)
            path = cache / f'menlo-{hashlib.sha256(raw).hexdigest()[:12]}.{extension}'
            path.write_bytes(raw)
            css.append(f"@font-face {{font-family:{family}; font-weight:{weight}; src:url('{path.as_uri()}')}}")
    reference.close()
    mono = ','.join(f"'{family}'" for family in families)
    return '\n'.join(css), mono


def slug(text: str) -> str:
    return re.sub(r'\s', '-', re.sub(r'[^\w\s-]', '', text.lower().strip()))


def markdown(text: str, function_table: bool = False) -> str:
    md = MarkdownIt('commonmark').enable('table')
    tokens = md.parse(text)
    additions = []
    used = {}
    for i, token in enumerate(tokens):
        if token.type == 'heading_open':
            label = tokens[i + 1].content.replace('`', '')
            key = slug(label)
            suffix = used.get(key, 0)
            used[key] = suffix + 1
            token.attrSet('id', key + (f'-{suffix}' if suffix else ''))
        if token.type == 'paragraph_open' and i + 1 < len(tokens):
            children = tokens[i + 1].children or []
            significant = [child for child in children if child.content or child.type in ('strong_open', 'strong_close')]
            if significant and significant[0].type == 'strong_open' and significant[-1].type == 'strong_close':
                token.attrSet('class', 'minor-title')
        if token.type == 'table_open' and function_table:
            count = 0
            for child in tokens[i + 1:]:
                if child.type == 'thead_close':
                    break
                count += child.type == 'th_open'
            if count == 12:
                token.attrSet('class', 'function-list')
                cols = Token('html_block', '', 0)
                cols.content = '<colgroup>' + ''.join(f'<col style="width:{width}%">' for width in WIDTHS) + '</colgroup>\n'
                additions.append((i + 1, cols))
    for i, token in reversed(additions):
        tokens.insert(i, token)
    rendered = md.renderer.render(tokens, md.options, {})

    def link(match: re.Match) -> str:
        target = html.unescape(match[1])
        parts = urlsplit(target)
        path = unquote(parts.path)
        for index, source in enumerate(DOCS):
            if not parts.scheme and path.endswith(source.name):
                target = '#' + (parts.fragment or ('specification' if index == 0 else 'function-table'))
        return f'href="{html.escape(target, quote=True)}"'

    rendered = re.sub(r'href="([^"]+)"', link, rendered)
    if function_table:
        def row(match: re.Match) -> str:
            index = 0

            def cell(cell_match: re.Match) -> str:
                nonlocal index
                index += 1
                content = cell_match[1]
                if index in (9, 10, 11):
                    content = re.sub(r'[−±-]?\d[\d,]*(?:\.\d+)?', r'<span class="nobr">\g<0></span>', content)
                return '<td>' + content + '</td>'

            return re.sub(r'<td>(.*?)</td>', cell, match[0], flags=re.S)

        rendered = re.sub(r'<tr>.*?</tr>', row, rendered, flags=re.S)
    return rendered


def chromium(explicit: str | None) -> str:
    if explicit or os.environ.get('SLINK_CHROMIUM'):
        return explicit or os.environ['SLINK_CHROMIUM']
    for command in ('chromium', 'chromium-browser', 'google-chrome'):
        if binary := shutil.which(command):
            return binary
    candidates = list((Path.home() / '.cache/ms-playwright').glob('chromium-*/chrome-linux64/chrome'))
    if candidates:
        return str(max(candidates, key=lambda path: int(path.parts[-3].split('-')[-1])))
    raise RuntimeError('Set SLINK_CHROMIUM to a Chromium executable')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chrome')
    parser.add_argument('--output', type=Path, default=ROOT / PDF_PATH)
    args = parser.parse_args()
    texts, commits = [], []
    for source in DOCS:
        text = (ROOT / source).read_text()
        commit = git('log', '-1', '--format=%H', '--', str(source)).decode().strip()
        if git('show', f'{commit}:{source}').decode() != text:
            raise RuntimeError(f'Commit the Markdown source before rendering: {source}')
        texts.append(text)
        commits.append(commit)
    revision = re.search(r'\| 文書の版 \| ([\d.]+)', texts[0])[1]
    date = re.search(r'\| 発行日 \| (\d{4}-\d{2}-\d{2})', texts[0])[1]
    if any(f'| 文書の版 | {revision}（DRAFT） |' not in text or f'| 発行日 | {date} |' not in text for text in texts):
        raise RuntimeError('Document revisions or publication dates differ')
    font_css, mono = fonts(Path.home() / '.cache/s-link-pdf/fonts')
    css = (ROOT / 'tools/pdf.css').read_text()
    sources = ''.join(f'<tr><td><code>{html.escape(str(source))}</code></td><td>文書の版 {revision}</td><td><a href="{REPOSITORY}/blob/{commit}/{quote(str(source))}"><code>{commit[:12]}</code></a></td></tr>' for source, commit in zip(DOCS, commits))
    cover = f'<section class="cover"><h1>S-LINK 2.0 規格書・機能表</h1><p class="edition">文書の版 {revision}（DRAFT） ／ 発行日 {date}</p><h2>生成元</h2><table><thead><tr><th>ファイル</th><th>版</th><th>コミット</th></tr></thead><tbody>{sources}</tbody></table><p class="repository">リポジトリ: <a href="{REPOSITORY}">{REPOSITORY}</a></p></section>'
    contents = cover + f'<section class="specification" id="specification">{markdown(texts[0])}</section><section class="functions" id="function-table">{markdown(texts[1], True)}</section>'
    document = f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>S-LINK 2.0 規格書・機能表 — DRAFT</title><style>{font_css}\n:root{{--mono:{mono}}}\n{css}</style></head><body>{contents}</body></html>'
    with tempfile.TemporaryDirectory(prefix='slink-pdf-') as work:
        work = Path(work)
        source_html, raw_pdf = work / 'document.html', work / 'raw.pdf'
        source_html.write_text(document)
        subprocess.run(['node', str(ROOT / 'tools/print_pdf.mjs'), chromium(args.chrome), str(source_html), str(raw_pdf)], check=True, timeout=90)
        pdf = fitz.open(raw_pdf)
        labels = ['S-LINK 2.0 規格書・機能表', '生成元']
        for text in texts:
            tokens = MarkdownIt('commonmark').parse(text)
            labels.extend(tokens[i + 1].content.replace('`', '') for i, token in enumerate(tokens) if token.type == 'heading_open')
        outline = pdf.get_toc(simple=False)
        if len(outline) != len(labels):
            raise RuntimeError('PDF bookmarks do not match the source headings')
        for entry, label in zip(outline, labels):
            entry[1] = label
        pdf.set_toc(outline)
        font = fitz.Font('hebo')
        for index, page in enumerate(pdf):
            width, height = page.rect.width, page.rect.height
            center = fitz.Point(width / 2, height / 2)
            size = min(width, height) * .78 / font.text_length('DRAFT', fontsize=1)
            text_width = font.text_length('DRAFT', fontsize=size)
            point = fitz.Point(center.x - text_width / 2, center.y + (font.ascender + font.descender) * size / 2)
            page.insert_text(point, 'DRAFT', fontsize=size, fontname='hebo', color=(.8, .1, .1), fill_opacity=.10, morph=(center, fitz.Matrix(35)), overlay=True)
            page.insert_text((45, 21), 'S-LINK 2.0', fontsize=7.5, color=(.25, .25, .25))
            footer = f'{date} / DRAFT / Rev {revision} / Source {commits[0][:12]}'
            page.insert_text((45, height - 19), footer, fontsize=7.5, color=(.25, .25, .25))
            folio = f'{index + 1} / {len(pdf)}'
            page.insert_text((width - 45 - fitz.get_text_length(folio, fontsize=7.5), height - 19), folio, fontsize=7.5, color=(.25, .25, .25))
        metadata = pdf.metadata
        metadata.update(title='S-LINK 2.0 規格書・機能表 — DRAFT', author='株式会社ティーファブワークス', subject=f'文書の版 {revision} / 規格書 {commits[0]} / 機能表 {commits[1]}')
        pdf.set_metadata(metadata)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        pdf.save(args.output, garbage=4, deflate=True)
        print(f'{args.output}: {len(pdf)} pages, source {commits[0][:12]} / {commits[1][:12]}')


if __name__ == '__main__':
    main()
