"""喵叔说保 · 公众号排版标记解析器（自写）。

输入：.gzh.md（Markdown 子集 + ::: 指令块），输出：meta 字典 + 块列表。
支持：
  @key value              元信息（title/kicker/date/source/type）
  ## 标题                 章节
  普通段落                空行分段
  ::: 类型 参数1 | 参数2   指令块，到单独一行 ::: 结束
行内：**锚点**  ==高亮==  ++关键词下划线++
"""
import re


def parse(text):
    meta, blocks = {}, []
    lines = text.replace('\r', '').split('\n')
    i, buf = 0, []

    def flush():
        if buf:
            blocks.append({'type': 'para', 'text': ''.join(s.strip() for s in buf)})
            buf.clear()

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if s.startswith('@') and not blocks and ' ' in s:
            k, v = s[1:].split(' ', 1)
            meta[k] = v.strip()
        elif s.startswith('## '):
            flush()
            blocks.append({'type': 'h2', 'text': s[3:].strip()})
        elif s.startswith(':::') and s != ':::':
            flush()
            head = s[3:].strip()
            kind, _, args = head.partition(' ')
            argv = [a.strip() for a in args.split('|')] if args.strip() else []
            body = []
            i += 1
            while i < len(lines) and lines[i].strip() != ':::':
                body.append(lines[i])
                i += 1
            blocks.append(_block(kind, argv, body))
        elif s == '':
            flush()
        else:
            buf.append(s)
        i += 1
    flush()
    return meta, blocks


def _paras(body):
    out, cur = [], []
    for ln in body:
        if ln.strip() == '':
            if cur:
                out.append(''.join(cur)); cur = []
        else:
            cur.append(ln.strip())
    if cur:
        out.append(''.join(cur))
    return out


def _block(kind, argv, body):
    b = {'type': kind, 'args': argv}
    lines = [l.strip() for l in body if l.strip()]
    if kind == 'clause':
        b['text'] = ' '.join(l for l in lines if not l.startswith('??'))
        b['note'] = next((l[2:].strip() for l in lines if l.startswith('??')), '')
    elif kind == 'table':
        b['rows'] = [[c.strip() for c in l.strip('|').split('|')] for l in lines if l.startswith('|')]
    elif kind == 'bars':
        items = []
        for l in lines:
            name, val = [x.strip() for x in l.rsplit('|', 1)]
            items.append((name, float(val)))
        b['items'] = items
    elif kind == 'calc':
        b['lines'] = [l for l in lines if not l.startswith('=') and not l.startswith('|')]
        b['cards_title'] = next((l[1:].strip() for l in lines if l.startswith('=')), '')
        b['cards'] = [[c.strip() for c in l.strip('|').split('|')] for l in lines if l.startswith('|')]
    elif kind == 'duo':
        b['items'] = [[x.strip() for x in l.split('|', 1)] for l in lines]
    elif kind in ('gates', 'steps', 'end'):
        b['items'] = lines
    elif kind == 'products':
        b.update(_products(lines))
    else:
        # 通用：以 | 开头的行进 rows，其余按空行分段进 paras（第二批主题的 grid/vs/report/roster 等用）
        b['paras'] = _paras([l for l in body if not l.strip().startswith('|')])
        b['rows'] = [[c.strip() for c in l.strip().strip('|').split('|')] for l in lines if l.startswith('|')]
    return b


def _point(t):
    """产品要点：`标签 | 正文` 或 `标签：正文`（标签 ≤6 字且不含标点时才拆）。返回 (标签, 正文, 分隔符)。"""
    if '|' in t:
        lab, txt = [x.strip() for x in t.split('|', 1)]
        return lab, txt, '：'
    k = t.find('：')
    if 0 < k <= 6 and not re.search(r'[，。、；？！（）]', t[:k]):
        return t[:k], t[k + 1:], '：'
    return '', t, ''


def _products(lines):
    """产品列表块（选购清单）：
      # 产品名 | 角标        一张产品卡（角标可省略，如「示例」）
      - 标签 | 正文 / - 标签：正文   卡内要点（标签可省略）
      其他行                 分类导语（排在产品卡前）
    paras 收齐全部正文（导语、产品名、要点），供未提供原文时比对和兜底降级用。"""
    intro, prods = [], []
    for l in lines:
        if l.startswith('# '):
            name, _, badge = l[2:].partition('|')
            prods.append({'name': name.strip(), 'badge': badge.strip(), 'points': []})
        elif l.startswith('- ') and prods:
            prods[-1]['points'].append(_point(l[2:].strip()))
        else:
            intro.append(l)
    paras = list(intro)
    for pd in prods:
        paras.append(pd['name'])
        paras += [lab + sep + txt for lab, txt, sep in pd['points']]
    return {'intro': intro, 'products': prods, 'paras': paras, 'rows': []}


INLINE = re.compile(r'(\*\*.+?\*\*|==.+?==|\+\+.+?\+\+)')


def inline_tokens(text):
    """把一段文字拆成 [(kind, str)]，kind ∈ plain/anchor/hl/ul。"""
    out = []
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith('**'):
            out.append(('anchor', part[2:-2]))
        elif part.startswith('=='):
            out.append(('hl', part[2:-2]))
        elif part.startswith('++'):
            out.append(('ul', part[2:-2]))
        else:
            out.append(('plain', part))
    return out


def strip_marks(text):
    return ''.join(t for _, t in inline_tokens(text))
