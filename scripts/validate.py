#!/usr/bin/env python3
"""校验一份公众号正文 HTML（平台限制 / leaf 包裹 / 半角标点 / 保险禁用词 / 免责必含句）。

用法：
  python3 scripts/validate.py body.html [--src 原文.md]
  --src：原文里本来就有的禁用词降级为 WARN（不改原文，只在报告列出）
退出码：有 ERROR 返回 1。
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
from checker import check  # noqa: E402
from source import source_paragraphs  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('html')
    ap.add_argument('--src')
    a = ap.parse_args()
    src = '\n'.join(source_paragraphs(a.src)) if a.src else ''
    err, warn, _ = check(open(a.html, encoding='utf-8').read(), src)
    for e in err:
        print('ERROR', e)
    for w in warn:
        print('WARN ', w)
    print('结果：%d ERROR，%d WARN' % (len(err), len(warn)))
    sys.exit(1 if err else 0)


if __name__ == '__main__':
    main()
