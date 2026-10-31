"""主题⑦　测评擂台 · 产品横评（leitai）
白底 + 擂台黑 #15181E + 红方 #E5483B / 蓝方 #2563C9；红蓝对阵表、胜方✓、分项条、单品打分卡、回合制章节。
静态化自视频 T04 对比擂台（左右分屏、维度逐行亮起、更宽松一项打勾）/ T03 测评打分卡（维度进度条 + 一句总评）。
适合：多款产品横评、两款同口径 PK、单品逐项拆解。不写星级、不打主观分，条上数字全部来自原文。
"""
import re

from base import sp, sec, blank, leaf, SANS
import miaolan

STAGE, RED, BLUE = '#15181E', '#E5483B', '#2563C9'
TXT, SUB, MUTE, LINE, PALE = '#2C2F36', '#5E636B', '#959AA2', '#E4E6EA', '#F4F5F7'
RT, BT = '#FDEEEC', '#EAF0FB'
NUM = "'DIN Alternate','Helvetica Neue',Helvetica,Arial," + SANS


class T(miaolan.T):
    id = 'leitai'
    name = '测评擂台 · 产品横评'
    P = dict(bg='#FFFFFF', text=TXT, title=STAGE, muted=MUTE, line=LINE, primary=RED,
             plight=PALE, hl='#FFE7E3', ul=RED, gold=RED, goldlight=RT,
             red=RED, redlight=RT)
    REMAP = {'#051A4C': STAGE, '#0288D1': BLUE, '#F2A900': RED, '#EEF7FD': PALE,
             '#D6E9F5': LINE, '#F7FAFD': '#FFFFFF', '#E3EAF2': LINE, '#55606F': SUB,
             '#EEF2F6': '#ECEEF1', '#7FC6EE': '#9FB6E3', '#F1F4F8': PALE, '#DDF0FB': '#DCE6F8',
             '#DCE6F0': LINE, '#F6F8FA': PALE, '#F5F9FC': '#FAFAFB', '#FFF7E0': RT,
             '#8A94A3': MUTE, '#3A4556': TXT, '#FFD666': '#FFB4AA', '#8CCDF0': RED}

    def post_inherit(self, h):
        return re.sub(r'border-radius:\d+px(?: \d+px)*;', 'border-radius:4px;', h)

    def mark_style(self, kind):
        return {
            'anchor': 'color:%s;font-weight:bold;' % RED,
            'hl': 'background:#FFE7E3;padding:0 2px;',
            'ul': 'border-bottom:2px solid %s;font-weight:600;padding-bottom:1px;' % RED,
        }[kind]

    def split(self, h=3, m='0'):
        """红蓝对半线：擂台的标志。"""
        return ('<table style="width:100%%;border-collapse:collapse;table-layout:fixed;margin:%s;"><tbody><tr>'
                '<td style="width:50%%;padding:0;height:%dpx;line-height:%dpx;font-size:0;background:%s;">%s</td>'
                '<td style="width:50%%;padding:0;height:%dpx;line-height:%dpx;font-size:0;background:%s;">%s</td>'
                '</tr></tbody></table>' % (m, h, h, RED, leaf(''), h, h, BLUE, leaf('')))

    def tagx(self, text, bg, fg, size=12):
        return sp('display:inline-block;padding:0 7px;margin-right:6px;border-radius:3px;background:%s;'
                  'color:%s;font-size:%dpx;font-weight:bold;letter-spacing:1px;' % (bg, fg, size), text)

    # 头图：擂台黑 + 红蓝线 + 同口径说明
    def header(self):
        m = self.meta
        basis = m.get('basis', '')
        return sec('margin:0 0 26px;background:%s;' % STAGE,
            self.split(4)
            + sec('padding:22px 18px 20px;',
                '<p style="margin:0 0 14px;font-size:12px;line-height:1.6;">%s%s</p>' % (
                    self.tagx('喵叔说保', RED, '#FFFFFF'), sp('color:#9AA1AC;letter-spacing:2px;', m.get('kicker', '')))
                + '<p style="margin:0 0 14px;font-size:23px;line-height:1.45;color:#FFFFFF;font-weight:bold;">%s</p>' % self.head_title()
                + ('<p style="margin:0 0 12px;font-size:12px;line-height:1.6;">%s%s</p>' % (
                    sp('display:inline-block;padding:0 6px;margin-right:6px;border:1px solid #4A515C;color:#C9CED6;', '同口径'), sp('color:#C9CED6;', basis)) if basis else '')
                + '<p style="margin:0;font-size:12px;line-height:1.6;color:#7D8591;">%s</p>' % leaf(m.get('date', '') + ' · 喵叔　防坑｜买对｜赔好')))

    # 回合章节
    def b_h2(self, b):
        self.chap += 1
        c = RED if self.chap % 2 else BLUE
        return sec('margin:36px 16px 16px;',
            '<p style="margin:0 0 6px;font-size:12px;line-height:1.5;">%s%s</p>' % (
                sp('display:inline-block;padding:1px 8px;background:%s;color:#FFFFFF;font-weight:bold;letter-spacing:1px;' % STAGE, 'ROUND %d' % self.chap),
                sp('display:inline-block;width:10px;height:10px;margin-left:6px;background:%s;' % c, ''))
            + '<p style="margin:0 0 10px;font-size:19px;line-height:1.5;color:%s;font-weight:bold;">%s</p>' % (STAGE, leaf(b['text']))
            + self.split(2))

    # 选手卡：编号 + 名字 + 承保方
    def b_roster(self, b):
        title, sub = (b['args'] + ['', ''])[:2]
        trs = ''
        for i, r in enumerate(b['rows']):
            name, co = (r + ['', ''])[:2]
            trs += ('<tr><td style="width:34px;padding:8px 0;border-bottom:1px solid %s;vertical-align:middle;"><p style="margin:0;font-size:12px;line-height:24px;">%s</p></td>'
                    '<td style="padding:8px 6px;border-bottom:1px solid %s;vertical-align:middle;"><p style="margin:0;font-size:15px;line-height:1.4;color:%s;font-weight:bold;">%s</p></td>'
                    '<td style="width:96px;padding:8px 0;border-bottom:1px solid %s;vertical-align:middle;text-align:right;"><p style="margin:0;font-size:12px;line-height:1.4;">%s</p></td></tr>' % (
                        LINE, sp('display:inline-block;width:24px;height:24px;line-height:24px;border-radius:50%%;background:%s;color:#FFFFFF;text-align:center;font-weight:bold;font-family:%s;letter-spacing:0;' % (STAGE, NUM), str(i + 1)),
                        LINE, STAGE, leaf(name), LINE,
                        sp('display:inline-block;padding:1px 7px;background:%s;color:%s;' % (PALE, SUB), co)))
        return sec('margin:0 16px 24px;padding:12px 14px 6px;border:1px solid %s;border-top:3px solid %s;' % (LINE, STAGE),
            '<p style="margin:0 0 4px;font-size:15px;line-height:1.5;color:%s;font-weight:bold;">%s</p>' % (STAGE, leaf(title))
            + '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody>%s</tbody></table>' % trs
            + ('<p style="margin:6px 0 4px;font-size:11px;line-height:1.6;color:%s;">%s</p>' % (MUTE, self.rich(sub)) if sub else ''))

    # 红蓝对阵表：左红方、中维度、右蓝方，更宽松的一方加粗打勾
    def b_vs(self, b):
        a, bb, basis = (b['args'] + ['', '', ''])[:3]
        head = ('<tr><td style="width:38%%;padding:10px 8px;background:%s;text-align:center;"><p style="margin:0;font-size:14px;line-height:1.35;color:#FFFFFF;font-weight:bold;">%s</p></td>'
                '<td style="width:24%%;padding:0;background:%s;text-align:center;vertical-align:middle;"><p style="margin:0;font-size:15px;line-height:1;color:#FFFFFF;font-weight:bold;font-family:%s;font-style:italic;">%s</p></td>'
                '<td style="width:38%%;padding:10px 8px;background:%s;text-align:center;"><p style="margin:0;font-size:14px;line-height:1.35;color:#FFFFFF;font-weight:bold;">%s</p></td></tr>' % (
                    RED, leaf(a), STAGE, NUM, leaf('VS'), BLUE, leaf(bb)))
        trs = ''
        for r in b['rows']:
            dim, va, vb, win = (r + ['', '', '', '-'])[:4]

            def cell(v, side):
                w = win == side
                col = RED if side == 'a' else BLUE
                mark = sp('color:%s;font-weight:bold;margin-%s:4px;' % (col, 'left' if side == 'a' else 'right'), '✓') if w else ''
                body = '<span style="color:%s;font-weight:%s;">%s</span>' % (STAGE if w else SUB, 'bold' if w else 'normal', self.rich(v))
                inner = (body + mark) if side == 'a' else (mark + body)
                return ('<td style="padding:10px 8px;border-bottom:1px solid %s;background:%s;text-align:%s;vertical-align:middle;">'
                        '<p style="margin:0;font-size:13px;line-height:1.45;">%s</p></td>' % (
                            LINE, (RT if side == 'a' else BT) if w else '#FFFFFF', 'right' if side == 'a' else 'left', inner))
            trs += ('<tr>%s<td style="padding:10px 2px;border-bottom:1px solid %s;background:%s;text-align:center;vertical-align:middle;">'
                    '<p style="margin:0;font-size:11px;line-height:1.35;color:%s;font-weight:bold;">%s</p></td>%s</tr>' % (
                        cell(va, 'a'), LINE, PALE, SUB, leaf(dim), cell(vb, 'b')))
        return sec('margin:0 16px 26px;border:1px solid %s;' % LINE,
            '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody>%s%s</tbody></table>' % (head, trs)
            + ('<p style="margin:0;padding:8px 10px;font-size:11px;line-height:1.6;color:%s;">%s</p>' % (MUTE, self.rich('✓＝更宽松的一方。' + basis)) if basis or True else ''))

    # 单品打分卡：不打分，只逐项列出原文写到的「多给的东西」
    def b_card(self, b):
        name, co = (b['args'] + ['', ''])[:2]
        side = RED if (getattr(self, 'card_n', 0) % 2 == 0) else BLUE
        self.card_n = getattr(self, 'card_n', 0) + 1
        trs = ''.join('<tr><td style="width:24px;padding:9px 0;border-bottom:1px solid %s;vertical-align:top;"><p style="margin:0;font-size:14px;line-height:1.45;color:%s;font-weight:bold;">%s</p></td>'
                      '<td style="padding:9px 6px 9px 0;border-bottom:1px solid %s;vertical-align:top;"><p style="margin:0;font-size:13px;line-height:1.45;color:%s;font-weight:bold;">%s</p></td>'
                      '<td style="width:46%%;padding:9px 0;border-bottom:1px solid %s;vertical-align:top;"><p style="margin:0;font-size:13px;line-height:1.45;color:%s;">%s</p></td></tr>' % (
                          LINE, side, leaf('＋'), LINE, STAGE, self.rich(r[0]), LINE, SUB, self.rich(r[1] if len(r) > 1 else ''))
                      for r in b['rows'])
        return sec('margin:0 16px 24px;border:1px solid %s;' % LINE,
            sec('padding:10px 14px;background:%s;' % side,
                '<p style="margin:0;font-size:16px;line-height:1.4;color:#FFFFFF;font-weight:bold;">%s%s</p>' % (
                    leaf(name), sp('font-size:11px;font-weight:normal;margin-left:8px;color:#FFFFFF;', co)))
            + sec('padding:2px 14px 6px;', '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody>%s</tbody></table>' % trs)
            + ''.join(sec('padding:0 14px 4px;', self.p(t, 'font-size:14px;margin:6px 0 10px;')) for t in b['paras']))

    def table(self, rows):
        head, body = rows[0], rows[1:]
        n = len(head)
        w0 = 32
        wi = (100 - w0) // (n - 1)
        th = ''.join('<td style="padding:8px 3px;background:%s;color:#FFFFFF;font-size:12px;line-height:1.4;font-weight:bold;text-align:%s;width:%d%%;">%s</td>'
                     % (STAGE, 'left' if i == 0 else 'center', w0 if i == 0 else wi, leaf(c)) for i, c in enumerate(head))
        trs = []
        for r, row in enumerate(body):
            tds = []
            for i, c in enumerate(row):
                hot = c.startswith('==')
                c = c.strip('=')
                # 差异项：红字加粗；只有标记稿里写了 ✓ 的格子才表示「更宽松」
                inner = self.rich(c) if not hot else sp('color:%s;font-weight:bold;' % RED, c)
                tds.append('<td style="padding:9px 3px;border-bottom:1px solid %s;font-size:13px;line-height:1.4;text-align:%s;color:%s;%s%s">%s</td>'
                           % (LINE, 'left' if i == 0 else 'center', STAGE if i == 0 else SUB, 'font-weight:bold;' if i == 0 else '',
                              'background:%s;' % RT if hot else ('background:#FAFAFB;' if r % 2 else ''), inner))
            trs.append('<tr>%s</tr>' % ''.join(tds))
        return '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody><tr>%s</tr>%s</tbody></table>' % (th, ''.join(trs))

    def b_table(self, b):
        title, sub = (b['args'] + ['', ''])[:2]
        return sec('margin:0 16px 26px;',
            '<p style="margin:0 0 8px;font-size:15px;line-height:1.5;color:%s;font-weight:bold;">%s</p>' % (STAGE, leaf(title))
            + self.table(b['rows'])
            + '<p style="margin:6px 0 0;font-size:11px;line-height:1.6;color:%s;">%s</p>' % (MUTE, self.rich(sub)))

    # 分项条：细条 + 右侧数值；名字以 == 开头的为本回合焦点（红），否则最大值为焦点
    def b_bars(self, b):
        title, unit = (b['args'] + ['', ''])[:2]
        items = b['items']
        mx = max(v for _, v in items)
        flagged = any(n.startswith('==') for n, _ in items)
        rows = []
        for name, v in items:
            hot = name.startswith('==') if flagged else v == mx
            name = name.strip('=')
            w = max(4, int(round(v / mx * 100)))
            nm, _, subt = name.partition(' · ')
            rows.append('<tr><td style="width:38%%;padding:7px 6px 7px 0;font-size:13px;line-height:1.35;color:%s;vertical-align:middle;%s">%s%s</td>'
                        '<td style="padding:7px 0;vertical-align:middle;">%s</td>'
                        '<td style="width:50px;padding:7px 0 7px 6px;vertical-align:middle;"><p style="margin:0;font-size:15px;line-height:1;color:%s;font-weight:bold;font-family:%s;text-align:right;">%s</p></td></tr>' % (
                            STAGE, 'font-weight:bold;' if hot else '', leaf(nm), ('<br>' + sp('color:%s;font-size:11px;font-weight:normal;' % MUTE, subt)) if subt else '',
                            sec('background:%s;height:12px;line-height:12px;font-size:0;border-radius:6px;' % PALE,
                                blank('width:%d%%;height:12px;background:%s;line-height:12px;font-size:0;border-radius:6px;' % (w, RED if hot else '#9AA1AC'))),
                            RED if hot else STAGE, NUM, leaf('%g' % v)))
        return sec('margin:0 16px 26px;padding:14px;border:1px solid %s;border-top:3px solid %s;' % (LINE, STAGE),
            '<p style="margin:0 0 6px;font-size:15px;line-height:1.5;color:%s;font-weight:bold;">%s</p>' % (STAGE, leaf(title))
            + '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody>%s</tbody></table>' % ''.join(rows)
            + '<p style="margin:8px 0 0;font-size:11px;line-height:1.6;color:%s;">%s</p>' % (MUTE, self.rich(unit)))

    def b_clause(self, b):
        name, ins, lead = (b['args'] + ['', '', ''])[:3]
        return sec('margin:0 16px 16px;border:1px solid %s;border-left:4px solid %s;' % (LINE, STAGE),
            sec('padding:9px 14px 4px;',
                '<p style="margin:0;font-size:15px;line-height:1.5;color:%s;font-weight:bold;">%s</p>' % (STAGE, leaf(name))
                + '<p style="margin:0 0 6px;font-size:12px;line-height:1.6;color:%s;">%s</p>' % (MUTE, self.rich(ins + '。' + lead + '：'))
                + '<p style="margin:0 0 8px;font-size:14px;line-height:1.8;color:%s;text-align:justify;">%s</p>' % (SUB, self.rich(b['text'])))
            + sec('padding:9px 14px;background:%s;' % PALE,
                '<p style="margin:0;font-size:14px;line-height:1.6;color:%s;font-weight:bold;">%s%s</p>' % (STAGE, self.tagx('人话', RED, '#FFFFFF'), leaf(b['note']))))

    def b_key(self, b):
        return sec('margin:4px 16px 24px;border:1px solid %s;' % LINE,
            self.split(3)
            + sec('padding:12px 14px;', ''.join(self.p(t, 'margin:0;color:%s;font-weight:bold;' % STAGE) for t in b['paras'])))

    def b_warn(self, b):
        return sec('margin:0 16px 22px;padding:12px 14px 2px;background:%s;border-left:4px solid %s;' % (RT, RED),
            '<p style="margin:0 0 8px;font-size:13px;line-height:1.6;">%s%s</p>' % (
                self.tagx('犯规提醒', RED, '#FFFFFF'), sp('color:%s;font-weight:bold;' % STAGE, b['args'][0] if b['args'] else ''))
            + ''.join(self.p(t, 'font-size:14px;margin-bottom:10px;') for t in b['paras']))

    def b_quote(self, b):
        return sec('margin:8px 16px 26px;text-align:center;',
            ''.join('<p style="margin:0 0 12px;font-size:17px;line-height:1.75;color:%s;font-weight:bold;">%s</p>' % (STAGE, self.rich(t)) for t in b['paras'])
            + '<table style="width:80px;margin:0 auto;border-collapse:collapse;table-layout:fixed;"><tbody><tr>'
              '<td style="padding:0;height:4px;line-height:4px;font-size:0;background:%s;">%s</td><td style="padding:0;height:4px;line-height:4px;font-size:0;background:%s;">%s</td>'
              '</tr></tbody></table>' % (RED, leaf(''), BLUE, leaf('')))

    def b_verdict(self, b):
        return sec('margin:0 16px 22px;background:%s;' % STAGE,
            self.split(4)
            + sec('padding:16px;',
                '<p style="margin:0 0 8px;font-size:12px;line-height:1.6;">%s</p>' % self.tagx('擂台结论', RED, '#FFFFFF')
                + ''.join('<p style="margin:0;font-size:18px;line-height:1.6;color:#FFFFFF;font-weight:bold;">%s</p>' % self.title_html(t, color='#FFB4AA') for t in b['paras'])))

    def b_end(self, b):
        it = b['items']
        return sec('margin:30px 16px 16px;border:1px solid %s;text-align:center;' % LINE,
            self.split(3)
            + sec('padding:16px 14px 14px;',
                '<p style="margin:0 0 10px;font-size:14px;line-height:1.8;color:%s;">%s</p>' % (SUB, self.rich(it[0]))
                + '<p style="margin:0 0 12px;font-size:15px;line-height:1.8;color:%s;font-weight:bold;">%s</p>' % (STAGE, self.rich(it[1]))
                + '<p style="margin:0;font-size:13px;line-height:1.6;">%s</p>' % sp(
                    'display:inline-block;padding:4px 14px;background:%s;color:#FFFFFF;font-weight:bold;' % STAGE, it[2])))
