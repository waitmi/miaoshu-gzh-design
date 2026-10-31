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
    else:
        # 通用：以 | 开头的行进 rows，其余按空行分段进 paras（第二批主题的 grid/vs/report/roster 等用）
        b['paras'] = _paras([l for l in body if not l.strip().startswith('|')])
        b['rows'] = [[c.strip() for c in l.strip().strip('|').split('|')] for l in lines if l.startswith('|')]
    return b


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
