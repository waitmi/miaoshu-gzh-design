"""公众号组件基类（自写）。

所有组件只输出 section / p / span / table / tr / td / br，样式全部内联，
文字一律 <span leaf=""> 包裹。不用 div/class/id/position/float/flex/grid/CSS 变量。
各主题继承 Theme，换色板并覆写有辨识度的组件。
"""
import html

from parse import inline_tokens

SANS = "-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif"
SERIF = "'Songti SC','STSong','Noto Serif SC','Source Han Serif SC','SimSun',serif"
PUNCT = '，。、；：？！）」』”’》〉…—'


def esc(s):
    return html.escape(s, quote=False)


def leaf(s):
    return '<span leaf="">%s</span>' % esc(s)


def sp(style, s):
    return '<span style="%s">%s</span>' % (style, leaf(s))


def sec(style, inner):
    return '<section style="%s">%s</section>' % (style, inner)


def blank(style):
    """装饰性空块：内放 leaf 占位，避免公众号剥样式。"""
    return '<section style="%s"><span leaf=""><br></span></section>' % style


class Theme:
    id = 'base'
    name = '基类'
    P = {}
    body_size = 15
    line_height = 1.85

    def __init__(self, meta):
        self.meta = meta
        self.chap = 0
        self.anchor_count = 0

    # ---------- 行内 ----------
    def mark_style(self, kind):
        P = self.P
        return {
            'anchor': 'color:%s;font-weight:bold;' % P['primary'],
            'hl': 'background:%s;padding:0 2px;' % P['hl'],
            'ul': 'border-bottom:2px solid %s;font-weight:600;padding-bottom:1px;' % P['ul'],
        }[kind]

    def rich(self, text, guard=True, color=None):
        toks = inline_tokens(text)
        self.anchor_count += sum(1 for k, _ in toks if k == 'anchor')
        tail = []
        full = ''.join(x for _, x in toks)
        if guard and len(full) >= 6:
            trail = len(full) - len(full.rstrip(PUNCT + '」'))
            need = 2 + trail
            while need > 0 and toks:
                kind, t = toks[-1]
                if len(t) <= need or (kind == 'anchor' and len(t) <= 8):
                    # 锚点不拆开（拆开会出现两个圈/两段标记）
                    tail.insert(0, toks.pop()); need -= len(t)
                else:
                    toks[-1] = (kind, t[:-need]); tail.insert(0, (kind, t[-need:])); need = 0
        head = ''.join(self._tok(k, t, color) for k, t in toks)
        if tail:
            head += '<span style="white-space:nowrap;">%s</span>' % ''.join(self._tok(k, t, color, count=False) for k, t in tail)
        return head

    def _tok(self, kind, t, color=None, count=True):
        if kind == 'plain':
            return leaf(t)
        st = self.mark_style(kind)
        if color and kind == 'anchor':
            st = st.replace(self.P['primary'], color)
        return sp(st, t)

    def title_html(self, title, color=None):
        """标题/判断句在第一个逗号处断行，避免孤字和难看的折行。"""
        if '，' in title:
            a, b = title.split('，', 1)
            if '**' not in a and '++' not in a and '==' not in a:
                return leaf(a + '，') + '<br>' + self.rich(b, color=color)
        return self.rich(title, color=color)

    def head_title(self, color=None):
        """头图大标题：@tbr 给了「/」断行位置就按它断（原文字不变），否则按第一个逗号断。"""
        t = self.meta.get('tbr')
        if t and t.replace('/', '') == self.meta['title']:
            return '<br>'.join(leaf(x) for x in t.split('/'))
        return self.title_html(self.meta['title'], color=color)

    def p(self, text, style='', guard=True, color=None):
        base = ('margin:0 0 18px;font-size:%dpx;line-height:%s;letter-spacing:0.5px;color:%s;'
                'text-align:justify;' % (self.body_size, self.line_height, self.P['text']))
        return '<p style="%s%s">%s</p>' % (base, style, self.rich(text, guard, color))

    def tag(self, text, bg, fg, extra=''):
        return sp('display:inline-block;padding:2px 9px;border-radius:3px;background:%s;color:%s;'
                  'font-size:12px;line-height:1.6;font-weight:bold;letter-spacing:1px;%s' % (bg, fg, extra), text)

    # ---------- 骨架 ----------
    def expand_unknown(self, blocks):
        """本主题没有的组件：降级为普通段落 + 通用表格，并记入 self.unknown（build 报 WARN）。"""
        out = []
        for b in blocks:
            if hasattr(self, 'b_' + b['type']):
                out.append(b)
                continue
            self.unknown.append(b['type'])
            for t in b.get('paras', []):
                out.append({'type': 'para', 'text': t})
            rows = b.get('rows') or []
            if rows and max(len(r) for r in rows) < 2:
                # 单列行（如⑤ chips 标签）：表格至少要两列，降级为一行一段
                out += [{'type': 'para', 'text': r[0]} for r in rows if r and r[0]]
            elif rows:
                out.append({'type': 'table', 'args': b.get('args', []), 'rows': rows})
        return out

    def render(self, blocks):
        self.unknown = []
        blocks = self.expand_unknown(blocks)
        parts = [self.header()]
        for b in blocks:
            name = 'b_' + b['type']
            h = getattr(self, name)(b)
            remap = getattr(self, 'REMAP', None)
            if remap and name not in type(self).__dict__:
                # 继承自其他主题的组件：按本主题色板换色
                for a, c in remap.items():
                    h = h.replace(a, '@@%s@@' % c)
                h = h.replace('@@', '')
                post = getattr(self, 'post_inherit', None)
                if post:
                    h = post(h)
            parts.append(h)
        parts.append(self.footer())
        P = self.P
        return ('<section style="max-width:677px;margin:0 auto;background:%s;font-family:%s;color:%s;'
                'font-size:%dpx;line-height:%s;letter-spacing:0.5px;word-wrap:break-word;'
                'overflow-x:hidden;padding:0 0 8px;">%s</section>'
                % (P['bg'], self.font, P['text'], self.body_size, self.line_height, ''.join(parts)))

    font = SANS

    def wrap(self, inner, pad='0 16px'):
        return sec('padding:%s;' % pad, inner)

    def footer(self):
        return ''

    # ---------- 默认块 ----------
    def b_para(self, b):
        return self.wrap(self.p(b['text']))

    def paras(self, b, style='', color=None, last_margin=True):
        ps = b.get('paras', [])
        out = []
        for i, t in enumerate(ps):
            st = style + ('margin-bottom:0;' if (i == len(ps) - 1 and not last_margin) else '')
            out.append(self.p(t, st, color=color))
        return ''.join(out)
