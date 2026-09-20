"""Convert cached SEC HTML into paragraph text with stable locators (P0001, P0002, ...).

Usage: python extract_text.py R01-irobot-carlyle
Writes <case>/extracted/<document id>.json: [{"locator": "P0001", "text": "..."}]. Text is whitespace-normalized only;
nothing is summarized, merged across blocks or edited, so quotations can be checked against the cached filing.
"""
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).parent
BLOCK = {'p', 'div', 'tr', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'table', 'br', 'title'}


class Blocks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks, self.current, self.skip = [], [], 0

    def flush(self):
        text = re.sub(r'\s+', ' ', ''.join(self.current).replace('\xa0', ' ')).strip()
        if text:
            self.blocks.append(text)
        self.current = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style') or tag.startswith('ix:header'):
            self.skip += 1
        if tag in BLOCK:
            self.flush()
        if tag == 'td':
            self.current.append(' | ')

    def handle_endtag(self, tag):
        if tag in ('script', 'style') or tag.startswith('ix:header'):
            self.skip = max(0, self.skip - 1)
        if tag in BLOCK:
            self.flush()

    def handle_data(self, data):
        if not self.skip:
            self.current.append(data)


def main(case):
    folder = HERE / case
    out = folder / 'extracted'
    out.mkdir(exist_ok=True)
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    for doc in manifest['documents']:
        parser = Blocks()
        parser.feed((folder / doc['cached_file']).read_bytes().decode('utf-8', errors='replace'))
        parser.flush()
        rows = [{'locator': f'P{i:04d}', 'text': text} for i, text in enumerate(parser.blocks, 1)]
        (out / (doc['id'] + '.json')).write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
        print(doc['id'], len(rows), sum(len(r['text']) for r in rows), flush=True)


if __name__ == '__main__':
    main(sys.argv[1])
