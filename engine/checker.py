#!/usr/bin/env python3
"""喵叔说保 · 公众号 HTML 校验器（自写）。

三关：
  1 平台关：禁用标签/属性/样式（ERROR）
  2 包裹关：所有文字必须在 <span leaf=""> 内（ERROR）；中文后半角标点（ERROR）
  3 合规关：保险禁用词（ERROR）；需人工确认词（WARN）
原则：排版不改原文。原文里本来就有的禁用词只降级为 WARN 列在报告里，由作者决定是否改稿；
排版新加的文字（标签、表格、标题等）出现禁用词一律 ERROR。
命令行入口：scripts/validate.py。
"""
import re
import sys
from html.parser import HTMLParser

ALLOWED_TAGS = {'section', 'p', 'span', 'strong', 'em', 'br', 'img', 'table', 'tbody', 'thead', 'tr', 'td', 'th'}
ALLOWED_ATTRS = {'style', 'leaf', 'src', 'alt', 'colspan', 'rowspan', 'width'}
BAD_STYLE = [
    (r'position\s*:', 'position 不可用'),
    (r'float\s*:', 'float 不可用'),
    (r'display\s*:\s*(flex|grid|inline-flex)', 'flex/grid 不可用（本规范从严）'),
    (r'var\s*\(', 'CSS 变量不可用'),
    (r'@font-face|font-face|url\s*\(', '外部资源/字体不可用'),
    (r'@media|@keyframes|animation|transition', '媒体查询/动画不可用'),
    (r'(linear|radial|conic)-gradient', '渐变背景可能触发暗黑模式检测（本规范禁用）'),
]
BANNED = ['回本', '取钱', '利息', '本金', '保本', '稳赚', '零风险', '收益率', '收益', '回报率', '复利',
          '比存款', '停售', '窗口期', '最高', '第一', '唯一', '排行榜', '排名']
SUGGEST = {'复利': 'IRR', '回本': '现价超过已交保费', '收益': '利益 / 演示利益', '收益率': 'IRR / 演示利益',
           '回报率': 'IRR', '保本': '（删去或改写为合同约定的保证利益）', '利息': '（改写为合同约定的利益）'}
WARN_WORDS = ['保证续保', '首选', '最好', '最值得', '必买', '闭眼']
HALF = re.compile(r'[\u4e00-\u9fff][,;!?:]|[,;!?:][\u4e00-\u9fff]|[\u4e00-\u9fff]\.(?![0-9])|"|\'')


class V(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.leaf, self.err, self.warn, self.texts = [], 0, [], [], []

    def handle_starttag(self, tag, attrs):
        ln = self.getpos()[0]
        if tag not in ALLOWED_TAGS:
            self.err.append('L%d 禁用标签 <%s>' % (ln, tag))
        for k, v in attrs:
            if k not in ALLOWED_ATTRS:
                self.err.append('L%d 禁用属性 %s 于 <%s>' % (ln, k, tag))
            if k == 'style' and v:
                for pat, msg in BAD_STYLE:
                    if re.search(pat, v, re.I):
                        self.err.append('L%d %s：%s' % (ln, msg, v[:60]))
        is_leaf = tag == 'span' and any(k == 'leaf' for k, _ in attrs)
        if tag != 'br':
            self.stack.append(is_leaf)
            if is_leaf:
                self.leaf += 1

    def handle_endtag(self, tag):
        if tag == 'br' or not self.stack:
            return
        if self.stack.pop():
            self.leaf -= 1

    def handle_data(self, d):
        if not d.strip():
            return
        if self.leaf <= 0:
            self.err.append('L%d 文字未用 <span leaf> 包裹：%s' % (self.getpos()[0], d.strip()[:20]))
        self.texts.append(d)


def hint(w):
    return '　建议改为：' + SUGGEST[w] if w in SUGGEST else ''


def check(html, source_text=''):
    v = V()
    v.feed(html)
    text = ''.join(v.texts)
    # 记录每段文字的起止，判断原文禁用词时上下文只取同一文字段内（避免与相邻标签粘连误报）
    bounds, pos = [], 0
    for t in v.texts:
        bounds.append((pos, pos + len(t))); pos += len(t)

    def seg_ctx(a, b):
        for s0, s1 in bounds:
            if s0 <= a and b <= s1:
                return text[max(s0, a - 5):min(s1, b + 5)]
        return text[max(0, a - 5):b + 5]
    for m in HALF.finditer(text):
        ctx = text[max(0, m.start() - 8):m.end() + 8]
        v.err.append('半角标点：…%s…' % ctx)
    for w in BANNED:
        for m in re.finditer(w, text):
            ctx = text[max(0, m.start() - 10):m.end() + 10]
            if w == '收益' and text[m.start():m.start() + 3] == '收益率':
                continue
            if source_text and w in source_text and seg_ctx(m.start(), m.end()) in source_text:
                v.warn.append('原文禁用词「%s」（未改原文，请作者确认）：…%s…%s' % (w, ctx, hint(w)))
            else:
                v.err.append('禁用词「%s」：…%s…%s' % (w, ctx, hint(w)))
    for w in WARN_WORDS:
        for m in re.finditer(w, text):
            v.warn.append('需人工确认词「%s」：…%s…' % (w, text[max(0, m.start() - 10):m.end() + 10]))
    if '以保险合同条款及核保结果为准' not in text:
        v.err.append('免责缺少「以保险合同条款及核保结果为准」')
    return v.err, v.warn, text
