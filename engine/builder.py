"""构建核心（自写）：标记稿 → body.html / article.html / preview.png / check.txt。
命令行入口见 scripts/build.py。
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
for p in (HERE, os.path.join(ROOT, 'themes')):
    if p not in sys.path:
        sys.path.insert(0, p)

from parse import parse, strip_marks  # noqa: E402
from checker import check  # noqa: E402
from source import source_paragraphs, coverage  # noqa: E402
from page import preview_page  # noqa: E402

THEMES = ['miaolan', 'nuanzhi', 'shenlan', 'wangge', 'tijian', 'heiban', 'leitai']


def draft_text(blocks):
    """未提供原文时的替代：标记稿里的正文文字（段落、标题、块内段落/条目），不含指令参数和 | 表格行。"""
    out = []
    for b in blocks:
        for k in ('text', 'note'):
            if b.get(k):
                out.append(b[k])
        for k in ('paras', 'items', 'lines'):
            for x in b.get(k, []):
                out.append(x if isinstance(x, str) else '')
    return [strip_marks(x) for x in out if x]


def build(theme_id, draft, out_dir, src=None, shot=True):
    """返回 (报告行列表, ERROR 数)。"""
    if theme_id not in THEMES:
        raise SystemExit('未知主题 %s，可选：%s' % (theme_id, ' / '.join(THEMES)))
    meta, blocks = parse(open(draft, encoding='utf-8').read())
    if 'title' not in meta:
        raise SystemExit('标记稿缺少 @title')
    th = importlib.import_module(theme_id).T(meta)
    body = th.render(blocks)
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, 'body.html'), 'w', encoding='utf-8').write(body)
    open(os.path.join(out_dir, 'article.html'), 'w', encoding='utf-8').write(preview_page(meta['title'], th.name, body))

    rep = ['主题：%s（%s）' % (th.name, theme_id), '文章：%s' % meta['title'],
           '标记稿：%s' % os.path.basename(draft), '原文：%s' % (os.path.basename(src) if src else '未提供（以标记稿正文段落作原文，跳过覆盖比对）')]
    paras = source_paragraphs(src) if src else draft_text(blocks)
    err, warn, text = check(body, '\n'.join(paras))
    for u in sorted(set(getattr(th, 'unknown', []))):
        warn.append('本主题没有组件「%s」，已降级为普通段落/表格' % u)
    rep.append('— 校验：%d ERROR，%d WARN' % (len(err), len(warn)))
    rep += ['  ERROR ' + e for e in err] + ['  WARN  ' + w for w in warn]
    rep.append('— 锚点（主色加粗）次数：%d（规范 ≤5）' % th.anchor_count)
    if th.anchor_count > 5:
        rep.append('  WARN  锚点超过 5 处，建议减少 ** 标记')
    if src:
        miss = coverage(paras, text)
        rep.append('— 原文覆盖：%d 段，缺失/改动 %d 段' % (len(paras), len(miss)))
        rep += ['  缺失 ' + m[:40] for m in miss]
    if shot:
        from shot import screenshot
        res = screenshot(body, os.path.join(out_dir, 'preview.png'))
        rep.append('— 版面自检（375px）：%d 项，页面高 %dpx' % (len(res['issues']), res['height']))
        rep += ['  ' + i for i in res['issues']]
    open(os.path.join(out_dir, 'check.txt'), 'w', encoding='utf-8').write('\n'.join(rep) + '\n')
    return rep, len(err)
