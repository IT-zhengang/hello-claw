#!/usr/bin/env python3
"""
网页 HTML 转 Markdown 转换脚本。
输入: chrome_get_web_content 返回的 JSON 文件路径
输出: 格式化后的 .md 文件
"""

import json
import sys
import os
import re
from datetime import datetime
import html2text
from bs4 import BeautifulSoup, NavigableString


def get_default_output_dir():
    """默认保存到执行命令时所在目录的 mds/ 子目录。"""
    return os.path.join(os.getcwd(), 'mds')

# ── 内容提取 ──────────────────────────────────────────────

CONTENT_SELECTORS = [
    ('div', {'class': 'rich_media_content'}),   # 微信公众号
    ('div', {'id': 'js_content'}),              # 微信公众号备选
    ('article', {}),                            # 通用
    ('main', {}),                               # HTML5
    ('div', {'class': 'article-content'}),
    ('div', {'class': 'post-content'}),
    ('div', {'class': 'entry-content'}),
    ('div', {'class': 'content'}),
]


def extract_main_content(html_str):
    soup = BeautifulSoup(html_str, 'html.parser')
    for tag, attrs in CONTENT_SELECTORS:
        el = soup.find(tag, attrs)
        if el:
            return el, soup
    return soup.find('body') or soup, soup


def extract_author(soup):
    """从 meta 标签中提取作者信息"""
    meta = soup.find('meta', attrs={'name': 'author'})
    if meta and meta.get('content'):
        return meta['content']
    # 微信公众号备选：profile_nickname
    el = soup.find('a', {'id': 'js_name'})
    if el:
        return el.get_text(strip=True)
    return ''


# ── 微信公众号 HTML 预处理 ────────────────────────────────

def is_wechat(html_str):
    """检测是否为微信公众号页面"""
    return 'rich_media_content' in html_str or 'js_content' in html_str


def preprocess_wechat_html(content_el):
    """预处理微信公众号的 HTML，修复常见问题"""
    tag_factory = content_el if callable(getattr(content_el, 'new_tag', None)) else BeautifulSoup('', 'html.parser')

    # 1. 图片：将 data-src 覆盖到 src（微信懒加载）
    for img in content_el.find_all('img'):
        data_src = img.get('data-src')
        if data_src:
            img['src'] = data_src

    # 2. 代码块：微信用嵌套 section + code 实现代码块
    #    将这种结构转为 <pre><code> 以便 html2text 正确识别
    for pre_section in content_el.find_all('section', attrs={'data-mpa-template': True}):
        codes = pre_section.find_all('code')
        if codes:
            lines = [c.get_text() for c in codes]
            new_pre = tag_factory.new_tag('pre')
            new_code = tag_factory.new_tag('code')
            new_code.string = '\n'.join(lines)
            new_pre.append(new_code)
            pre_section.replace_with(new_pre)

    # 3. 代码块备选：<pre> 下直接多个 <code> 行
    for pre in content_el.find_all('pre'):
        codes = pre.find_all('code')
        if len(codes) > 1:
            lines = [c.get_text() for c in codes]
            pre.clear()
            new_code = tag_factory.new_tag('code')
            new_code.string = '\n'.join(lines)
            pre.append(new_code)

    # 4. 移除空的 section/span 等装饰标签（减少空标题）
    for tag in content_el.find_all(['section', 'span', 'p']):
        text = tag.get_text(strip=True)
        if not text and not tag.find('img'):
            # 保留包含图片的空标签
            tag.decompose()

    return content_el


def clean_image_url(url):
    """清理微信图片 URL：移除 fragment、修复 HTML 实体"""
    if not url:
        return url
    # 移除 #imgIndex=N 等 fragment
    url = re.sub(r'#[^#]*$', '', url)
    # 修复 HTML 实体
    url = url.replace('&amp;', '&')
    # 移除可能导致问题的参数
    url = re.sub(r'[&?]tp=webp', '', url)
    url = re.sub(r'[&?]wxfrom=\d+', '', url)
    url = re.sub(r'[&?]wx_lazy=\d+', '', url)
    # 清理可能产生的 ?& 或 && 等
    url = re.sub(r'\?&', '?', url)
    url = re.sub(r'&&+', '&', url)
    url = url.rstrip('?&')
    return url


# ── Markdown 后处理 ───────────────────────────────────────

def fix_tables(text):
    """核心修复: 删除表格行之间的空行，保留表格前后的空行。"""
    lines = text.split('\n')
    result = []
    i = 0
    while i < len(lines):
        result.append(lines[i])
        if lines[i].strip().startswith('|') and lines[i].strip().endswith('|'):
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            if j < len(lines) and lines[j].strip().startswith('|'):
                i = j
                continue
        i += 1
    return '\n'.join(result)


def fix_code_blocks(text):
    """将 html2text 生成的 [code]...[/code] 转为 ```...```"""
    text = re.sub(r'\[code\]', '```', text)
    text = re.sub(r'\[/code\]', '```', text)
    return text


def fix_reference_links(text):
    """将脚注式引用 '1. url: url' 转为 Markdown 链接格式"""
    text = re.sub(
        r'(\d+)\. (https?://[^:\s]+): (https?://[^\s]+)',
        r'\1. [\2](\3)',
        text
    )
    return text


def clean_empty_images(text):
    """移除空的图片标签 ![]()"""
    return re.sub(r'!\[\]\(\s*\)', '', text)


def clean_image_urls_in_md(text):
    """清理 Markdown 中所有图片 URL"""
    def replace_img(match):
        alt = match.group(1)
        url = clean_image_url(match.group(2))
        if not alt or alt.strip() == '':
            alt = '图片'
        return f'![{alt}]({url})'
    return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_img, text)


def fix_empty_headings(text):
    """移除空的标题行（如单独的 # 或 ## ）"""
    return re.sub(r'^#{1,6}\s*$', '', text, flags=re.MULTILINE)


def fix_bold_markers(text):
    """修复断裂的加粗标记：** 后换行或 ** 前换行"""
    # 修复 **文字** 中间被换行打断的情况
    text = re.sub(r'\*\*\s*\n\s*\*\*', '', text)
    # 移除行尾孤立的 **
    text = re.sub(r'\*\*\s*$', '', text, flags=re.MULTILINE)
    # 移除行首孤立的 **
    text = re.sub(r'^\s*\*\*\s*$', '', text, flags=re.MULTILINE)
    return text


def fix_inline_list_as_codeblock(text):
    """
    修复 html2text 将多行代码内容转为缩进列表的问题。
    检测模式：连续的 `  * ` 开头行，内容像代码/流程图/树状图，转为代码块。
    """
    lines = text.split('\n')
    result = []
    i = 0
    while i < len(lines):
        # 检测连续的缩进列表行，内容含 ← 或 ↓ 或 ├── 等代码特征
        if re.match(r'^\s{2,}\*\s+', lines[i]):
            block = []
            j = i
            has_code_chars = False
            while j < len(lines) and re.match(r'^\s{2,}\*\s+', lines[j]):
                content = re.sub(r'^\s{2,}\*\s+', '', lines[j])
                block.append(content)
                if re.search(r'[←↓↑→├└│┌┐┘┤┬┴┼]', content):
                    has_code_chars = True
                j += 1
            if has_code_chars and len(block) >= 3:
                result.append('```')
                result.extend(block)
                result.append('```')
                i = j
                continue
        result.append(lines[i])
        i += 1
    return '\n'.join(result)


def add_section_separators(text):
    """在 H2 标题前添加 --- 分隔线（除了第一个 H2）"""
    lines = text.split('\n')
    result = []
    h2_count = 0
    for i, line in enumerate(lines):
        if re.match(r'^## ', line):
            h2_count += 1
            if h2_count > 1:
                # 避免重复添加 ---
                if result and result[-1].strip() != '---':
                    # 移除多余空行，加入分隔线
                    while result and result[-1].strip() == '':
                        result.pop()
                    result.append('')
                    result.append('---')
                    result.append('')
        result.append(line)
    return '\n'.join(result)


def normalize_spacing(text):
    """规范化空行和间距"""
    # 标题前后确保有空行
    text = re.sub(r'([^\n])\n(#{1,6} )', r'\1\n\n\2', text)
    text = re.sub(r'(#{1,6} [^\n]+)\n([^\n#\s])', r'\1\n\n\2', text)

    # 代码块前后确保有空行
    text = re.sub(r'([^\n])\n(```)', r'\1\n\n\2', text)
    text = re.sub(r'(```)\n([^\n`])', r'\1\n\n\2', text)

    # 表格块前后确保有空行
    text = re.sub(r'([^\n|])\n(\|)', r'\1\n\n\2', text)
    text = re.sub(r'(\|[^\n]+)\n([^\n|])', r'\1\n\n\2', text)

    # 压缩连续空行
    text = re.sub(r'\n{3,}', '\n\n', text)

    # 清理行尾空格
    text = re.sub(r' +\n', '\n', text)

    return text.strip()


def optimize_markdown(text):
    """全部后处理流水线（顺序重要）"""
    text = fix_code_blocks(text)
    text = fix_inline_list_as_codeblock(text)
    text = clean_empty_images(text)
    text = clean_image_urls_in_md(text)
    text = fix_empty_headings(text)
    text = fix_bold_markers(text)
    text = fix_reference_links(text)
    text = fix_tables(text)
    text = add_section_separators(text)
    text = normalize_spacing(text)
    return text


# ── 转换主函数 ────────────────────────────────────────────

def convert(html_str, title='', url='', author=''):
    content_el, soup = extract_main_content(html_str)

    # 自动提取作者
    if not author:
        author = extract_author(soup)

    # 微信公众号特殊预处理
    if is_wechat(html_str):
        content_el = preprocess_wechat_html(content_el)

    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.body_width = 0           # 不自动换行
    h.unicode_snob = True      # 保留 Unicode 字符
    h.images_to_alt = False
    h.single_line_break = False
    h.wrap_links = False
    h.wrap_list_items = False
    h.pad_tables = True
    h.protect_links = True     # 保护链接不被换行打断
    h.mark_code = True         # 标记 <code> 为反引号

    md = h.handle(str(content_el))
    md = optimize_markdown(md)

    # 构建文件头
    header_parts = [f'# {title}']
    if author or url:
        header_parts.append('')
        header_parts.append('> **作者**：' + (author or '未知'))
        if url:
            header_parts.append('>')
            header_parts.append(f'> **原文链接**：[{url}]({url})')
        header_parts.append('')
        header_parts.append('---')

    header = '\n'.join(header_parts)
    md = f'{header}\n\n{md}'
    return md


# ── 文件名生成 ────────────────────────────────────────────

def safe_filename(title, max_len=60):
    # 保留中文、字母、数字、空格、连字符
    name = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', title).strip()
    name = re.sub(r'[\s]+', '_', name)
    if len(name) > max_len:
        name = name[:max_len]
    return f'{name}.md'


# ── CLI 入口 ──────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: convert_webpage.py <input_json> [output_path]")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        data = json.load(f)

    raw = json.loads(data[0]['text'])
    html_str = raw['htmlContent']
    title = raw.get('title', 'untitled')
    url = raw.get('url', '')

    md = convert(html_str, title, url)

    if len(sys.argv) >= 3:
        out = sys.argv[2]
    else:
        default_output_dir = get_default_output_dir()
        os.makedirs(default_output_dir, exist_ok=True)
        out = os.path.join(default_output_dir, safe_filename(title))

    with open(out, 'w', encoding='utf-8') as f:
        f.write(md)

    print(f'Saved: {out}')
    print(f'Size:  {os.path.getsize(out)} bytes')


if __name__ == '__main__':
    main()
