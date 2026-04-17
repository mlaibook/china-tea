#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZH_DIR = ROOT / '_zh_teaware'
EN_DIR = ROOT / '_en_teaware'
ZH_SECTION_DIR = ROOT / '_zh_section_index'
EN_SECTION_DIR = ROOT / '_en_section_index'
LEGACY_OUTPUT_DIRS = [ROOT / 'zh' / 'teaware', ROOT / 'en' / 'teaware']

KEY_FIELDS = [
    'lang_switch_url',
    'layout',
    'lang',
    'title',
    'description',
    'permalink',
    'collection_key',
    'section',
]


def parse_front_matter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding='utf-8')
    normalized = text.lstrip('\ufeff\n\r\t ')
    if not normalized.startswith('---'):
        raise ValueError(f'{path}: missing front matter start')
    if normalized.startswith('---\r\n'):
        rest = normalized[5:]
    elif normalized.startswith('---\n'):
        rest = normalized[4:]
    else:
        raise ValueError(f'{path}: malformed front matter opening')

    m = re.search(r'\n---\r?\n', rest)
    if not m:
        raise ValueError(f'{path}: missing front matter end')
    block = rest[:m.start()].splitlines()
    data: dict[str, str] = {}
    for line in block:
        if not line.strip() or line.lstrip().startswith('#') or ':' not in line:
            continue
        key, value = line.split(':', 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def expect(cond: bool, msg: str, errors: list[str]) -> None:
    if not cond:
        errors.append(msg)


def main() -> int:
    errors: list[str] = []

    expect(ZH_DIR.is_dir(), 'missing _zh_teaware directory', errors)
    expect(EN_DIR.is_dir(), 'missing _en_teaware directory', errors)
    expect(ZH_SECTION_DIR.is_dir(), 'missing _zh_section_index directory', errors)
    expect(EN_SECTION_DIR.is_dir(), 'missing _en_section_index directory', errors)
    if errors:
        for e in errors:
            print(f'ERROR: {e}')
        return 1

    zh_files = sorted(p for p in ZH_DIR.glob('*.html') if p.is_file())
    en_files = sorted(p for p in EN_DIR.glob('*.html') if p.is_file())
    zh_names = {p.stem for p in zh_files}
    en_names = {p.stem for p in en_files}

    for missing in sorted(zh_names - en_names):
        errors.append(f'missing English counterpart for {missing}')
    for extra in sorted(en_names - zh_names):
        errors.append(f'English article has no Chinese source: {extra}')

    for slug in sorted(zh_names & en_names):
        zh_path = ZH_DIR / f'{slug}.html'
        en_path = EN_DIR / f'{slug}.html'
        zh = parse_front_matter(zh_path)
        en = parse_front_matter(en_path)

        for field in KEY_FIELDS:
            expect(field in zh and zh[field] != '', f'{zh_path.name}: missing {field}', errors)
            expect(field in en and en[field] != '', f'{en_path.name}: missing {field}', errors)

        expect(zh.get('lang') == 'zh-CN', f'{zh_path.name}: lang should be zh-CN', errors)
        expect(en.get('lang') == 'en', f'{en_path.name}: lang should be en', errors)
        expect(zh.get('layout') == 'article', f'{zh_path.name}: layout should be article', errors)
        expect(en.get('layout') == 'article', f'{en_path.name}: layout should be article', errors)

        expect(zh.get('section') == 'teaware', f'{zh_path.name}: section should be teaware', errors)
        expect(en.get('section') == 'teaware', f'{en_path.name}: section should be teaware', errors)
        expect(zh.get('collection_key') == slug, f'{zh_path.name}: collection_key should be {slug}', errors)
        expect(en.get('collection_key') == slug, f'{en_path.name}: collection_key should be {slug}', errors)

        expect(zh.get('permalink') == f'/zh/teaware/{slug}.html', f'{zh_path.name}: bad permalink', errors)
        expect(en.get('permalink') == f'/en/teaware/{slug}.html', f'{en_path.name}: bad permalink', errors)
        expect(zh.get('lang_switch_url') == f'../../en/teaware/{slug}.html', f'{zh_path.name}: bad lang_switch_url', errors)
        expect(en.get('lang_switch_url') == f'../../zh/teaware/{slug}.html', f'{en_path.name}: bad lang_switch_url', errors)

        expect(zh.get('title', '').strip() != en.get('title', '').strip(), f'{slug}: zh/en titles are identical; translation likely missing', errors)
        expect(zh.get('description', '').strip() != en.get('description', '').strip(), f'{slug}: zh/en descriptions are identical; translation likely missing', errors)

    for output_dir in LEGACY_OUTPUT_DIRS:
        if output_dir.exists():
            for direct_file in output_dir.glob('*.html'):
                if direct_file.name == 'index.html':
                    continue
                slug = direct_file.stem
                if slug in zh_names or slug in en_names:
                    pass

    if errors:
        print('Teaware collections check FAILED')
        for e in errors:
            print(f'- {e}')
        return 1

    print('Teaware collections check PASSED')
    print(f'- zh articles: {len(zh_files)}')
    print(f'- en articles: {len(en_files)}')
    print('- checked bilingual pairing, lang switch, permalink, section, collection_key, and source-only collection locations')
    return 0


if __name__ == '__main__':
    sys.exit(main())
