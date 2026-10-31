#!/usr/bin/env python3
"""构建：标记稿 → body.html（干净正文）/ article.html（带复制按钮）/ preview.png（375px 2x 长图）/ check.txt（校验报告）

用法：
  python3 scripts/build.py <主题id|all> <标记稿.gzh.md> [--src 原文.md] [--out 输出目录] [--no-shot]

  主题id：miaolan nuanzhi shenlan wangge tijian heiban leitai xuangou；all = 8 套全出
  --src     原文 Markdown。提供时：原文已有的禁用词降级为 WARN，并做原文逐句覆盖比对
  --out     输出目录，默认 output/<标记稿名>/<主题id>/（主题为 all 时自动按主题分子目录）
  --no-shot 不截图（没有浏览器环境时用；同时跳过版面自检）
退出码：任一主题有 ERROR 返回 1。
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
from builder import build, THEMES  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description='喵叔说保 · 公众号排版构建')
    ap.add_argument('theme')
    ap.add_argument('draft')
    ap.add_argument('--src')
    ap.add_argument('--out')
    ap.add_argument('--no-shot', action='store_true')
    a = ap.parse_args()
    themes = THEMES if a.theme == 'all' else [a.theme]
    name = os.path.basename(a.draft).split('.')[0]
    bad = 0
    for t in themes:
        if a.out:
            out = os.path.join(a.out, t) if len(themes) > 1 else a.out
        else:
            out = os.path.join(ROOT, 'output', name, t)
        rep, n = build(t, a.draft, out, a.src, shot=not a.no_shot)
        bad += n
        print('\n'.join(rep))
        print('→ 输出：%s\n' % out)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
