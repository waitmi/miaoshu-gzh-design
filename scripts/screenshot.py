#!/usr/bin/env python3
"""把正文 HTML 截成手机长图，并输出 375px 版面自检（孤字、行首标点、越界、容器溢出）。

用法：
  python3 scripts/screenshot.py body.html preview.png [--width 375] [--scale 2]
环境变量：GZH_CHROMIUM 指定浏览器路径；GZH_FONT_DIR 指定截图用中文字体目录（默认 fonts/）。
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
from shot import screenshot  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('html')
    ap.add_argument('png')
    ap.add_argument('--width', type=int, default=375)
    ap.add_argument('--scale', type=float, default=2)
    a = ap.parse_args()
    body = open(a.html, encoding='utf-8').read()
    if 'id="gzh-body"' in body:  # 传入的是 article.html：只截正文
        body = body.split('id="gzh-body">', 1)[1].rsplit('</section>\n</section>', 1)[0]
    res = screenshot(body, a.png, a.width, a.scale)
    print('版面自检（%dpx）：%d 项，页面高 %dpx' % (a.width, len(res['issues']), res['height']))
    for i in res['issues']:
        print('  ' + i)
    print('→', a.png)


if __name__ == '__main__':
    main()
