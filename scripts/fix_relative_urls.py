from pathlib import Path
import re

root = Path('/home/richard/.openclaw/workspace/china-tea')
text_exts = {'.html', '.md', '.yml', '.yaml', '.py', '.css', '.js'}

skip_dirs = {'.git', '_site', 'node_modules'}


def rel_prefix(path: Path) -> str:
    rel = path.relative_to(root)
    depth = len(rel.parts) - 1
    return '' if depth == 0 else '../' * depth


def replace_path(value: str, prefix: str) -> str:
    if value.startswith('/china-tea/'):
        return prefix + value[len('/china-tea/'):]
    return value


for p in root.rglob('*'):
    if not p.is_file():
        continue
    if any(part in skip_dirs for part in p.parts):
        continue
    if p.suffix.lower() not in text_exts and p.name not in {'index.html'}:
        continue
    txt = p.read_text(encoding='utf-8')
    prefix = rel_prefix(p)
    new = txt
    new = re.sub(r'(href|src)="/china-tea/([^"]+)"', lambda m: f'{m.group(1)}="{prefix}{m.group(2)}"', new)
    new = re.sub(r'(href|src)=\'/china-tea/([^\']+)\'', lambda m: f"{m.group(1)}='{prefix}{m.group(2)}'", new)
    new = re.sub(r'(lang_switch_url:\s*)"/china-tea/([^"]+)"', lambda m: f'{m.group(1)}"{prefix}{m.group(2)}"', new)
    new = re.sub(r'(image:\s*)/china-tea/([^\s]+)', lambda m: f'{m.group(1)}{prefix}{m.group(2)}', new)
    if p.name == 'head.html' and p.parent.name == '_includes':
        new = new.replace('href="../assets/css/style.css"', 'href="{{ page.asset_prefix | default: \'../\' }}assets/css/style.css"')
    if p.name == 'index.html' and p.parent == root:
        new = new.replace('url=/china-tea/en/index.html', 'url=en/index.html')
        new = new.replace('href="en/index.html"', 'href="en/index.html"')
        new = new.replace('href="zh/index.html"', 'href="zh/index.html"')
    if new != txt:
        p.write_text(new, encoding='utf-8')
        print('updated', p.relative_to(root))
