#!/usr/bin/env python3
"""标记稿合成：用原文段落编号拼标记稿，正文一字不改。

用法：
  python3 scripts/compose.py --dump 原文.md           列出原文段落编号
  python3 scripts/compose.py 文章.spec                写出同名 文章.gzh.md

spec 语法（详见 templates/标记语法.md）：
  @src 原文路径                    必填，相对 spec 所在目录或绝对路径
  @title/@tbr/@kicker/@date/@type  元信息（title 缺省取原文 # 标题）
  @mark <**|==|++> <原文子串>       行内标记，作用于子串在正文里第一次出现处
  <<n>> 或 <<a-b>>                 引用原文第 n 段 / 第 a～b 段
其余行原样保留（## 标题、::: 指令块、| 表格行等排版新加内容）。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
from source import source_paragraphs  # noqa: E402


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    if sys.argv[1] == '--dump':
        for i, p in enumerate(source_paragraphs(sys.argv[2])):
            print('%d\t%s' % (i, p))
        return
    spec = sys.argv[1]
    meta, marks, out = {}, [], []
    for ln in open(spec, encoding='utf-8').read().split('\n'):
        if ln.startswith('@mark '):
            _, k, sub = ln.split(' ', 2)
            marks.append((k, sub.strip()))
        elif ln.startswith('@') and not out:
            k, v = ln[1:].split(' ', 1)
            meta[k] = v.strip()
        else:
            out.append(ln)
    srcf = meta['src'] if os.path.isabs(meta['src']) else os.path.join(os.path.dirname(os.path.abspath(spec)), meta['src'])
    paras = source_paragraphs(srcf)
    if 'title' not in meta:
        meta['title'] = next(l[2:].strip() for l in open(srcf, encoding='utf-8') if l.startswith('# '))
    used, body = set(), []
    for ln in out:
        m = re.fullmatch(r'\s*<<(\d+)(?:-(\d+))?>>\s*', ln)
        if m:
            a = int(m.group(1)); b = int(m.group(2) or a)
            for i in range(a, b + 1):
                if i in used:
                    print('WARN 段落重复引用', i)
                used.add(i)
                body += [paras[i], '']
        else:
            body.append(ln)
    blines = '\n'.join(body).split('\n')
    for k, sub in marks:
        for j, l in enumerate(blines):
            if l.startswith((':::', '|', '##', '@')):
                continue
            if sub in l:
                blines[j] = l.replace(sub, k + sub + k, 1)
                break
        else:
            print('WARN 标记未命中', k, sub)
    miss = [i for i in range(len(paras)) if i not in used]
    if miss:
        print('WARN 未引用原文段落', miss)
    order = ['title', 'tbr', 'kicker', 'date', 'type']
    keys = [k for k in order if k in meta] + [k for k in meta if k not in order and k != 'src']
    head = ['@%s %s' % (k, meta[k]) for k in keys]
    dst = re.sub(r'\.spec$', '', spec) + '.gzh.md'
    open(dst, 'w', encoding='utf-8').write('\n'.join(head) + '\n\n' + re.sub(r'\n{3,}', '\n\n', '\n'.join(blines)).strip() + '\n')
    print('写出', dst, '原文段落', len(paras), '已引用', len(used))


if __name__ == '__main__':
    main()
