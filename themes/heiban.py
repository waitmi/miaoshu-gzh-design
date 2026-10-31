"""主题⑥　黑板荧光笔 · 知识笔记（heiban）
米白笔记纸 + 黑板绿 #26392F 板书块（粉笔白 / 粉笔黄）+ 荧光黄半截划线 + 红笔圈注。
静态化自视频 T06 黑板讲解（粉笔描公式、最后画圈）/ T01 荧光笔笔记（标题划重点、白卡逐条讲要点）。
适合：知识科普、名词解释、医保怎么选、带一个公式的推演。
注：小标题字体栈楷体优先（Mac/Windows 有楷体时显示手写感），手机端多回落为宋体/黑体，版式不依赖它。
"""
import re

from base import sp, sec, blank, leaf, SANS, SERIF
import miaolan

BOARD, CHALK, CHALKY, WOOD = '#26392F', '#F3F1E7', '#F5D76E', '#8B6B4A'
PAPER, INK, TXT, SUB, MUTE, LINE = '#FFFDF7', '#22272B', '#2F3437', '#5B6166', '#8E9397', '#E6E1D3'
RED, HL, NOTE = '#E04F3F', '#FFE873', '#FFF4B8'
KAI = "'Kaiti SC','STKaiti','KaiTi'," + SERIF


class T(miaolan.T):
    id = 'heiban'
    name = '黑板荧光笔 · 知识笔记'
    P = dict(bg=PAPER, text=TXT, title=INK, muted=MUTE, line=LINE, primary=RED,
             plight='#F6F2E6', hl=HL, ul=RED, gold=BOARD, goldlight=NOTE,
             red=RED, redlight='#FDEDEA')
    REMAP = {'#051A4C': INK, '#0288D1': BOARD, '#F2A900': BOARD, '#EEF7FD': '#F6F2E6',
             '#D6E9F5': LINE, '#F7FAFD': '#FFFFFF', '#E3EAF2': LINE, '#55606F': SUB,
             '#EEF2F6': '#EFEBDF', '#7FC6EE': '#9DB0A5', '#F1F4F8': '#F6F2E6', '#DDF0FB': '#DCE5DF',
             '#DCE6F0': LINE, '#F6F8FA': '#FFFFFF', '#F5F9FC': '#FBF8EF', '#FFF7E0': NOTE,
             '#8A94A3': MUTE, '#3A4556': TXT, '#FFD666': CHALKY, '#8CCDF0': RED}

    def mark_style(self, kind):
        return {
            # 红笔圈注
            'anchor': 'color:%s;font-weight:bold;border:2px solid %s;border-radius:14px;padding:0 5px;white-space:nowrap;' % (INK, RED),
            # 荧光笔半截划线
            'hl': 'box-shadow:inset 0 -9px 0 %s;padding:0 1px;' % HL,
            # 划重点：荧光黄下半截 + 加粗
            'ul': 'box-shadow:inset 0 -8px 0 %s;font-weight:bold;padding:0 1px;' % HL,
        }[kind]

    def _tok(self, kind, t, color=None, count=True):
        if kind == 'anchor' and color:
            # 黑板上的圈注：粉笔黄圈 + 粉笔白字
            return sp('color:%s;font-weight:bold;border:2px solid %s;border-radius:14px;padding:0 5px;' % (CHALK, CHALKY), t)
        if kind in ('hl', 'ul') and color:
            # 黑板上不用荧光底（会和粉笔白撞色），改粉笔黄字 + 虚线
            return sp('color:%s;font-weight:bold;border-bottom:1px dashed %s;' % (CHALKY, CHALKY), t)
        return super()._tok(kind, t, color, count)

    def chalk_tag(self, t, bg=CHALKY, fg=BOARD):
        return sp('display:inline-block;padding:0 8px;margin-right:6px;background:%s;color:%s;font-size:12px;font-weight:bold;letter-spacing:1px;' % (bg, fg), t)

    def board(self, inner, pad='18px 16px', m='0 16px 8px'):
        """黑板 + 木色粉笔槽。"""
        return (sec('margin:%s;background:%s;padding:%s;border:6px solid #3B4A40;border-bottom:none;' % (m, BOARD, pad), inner)
                + blank('margin:0 16px 24px;height:8px;background:%s;line-height:8px;font-size:0;' % WOOD))

    # 头图：整块黑板，粉笔标题 + 粉笔黄虚线
    def header(self):
        m = self.meta
        inner = ('<p style="margin:0 0 14px;font-size:12px;line-height:1.6;">%s%s</p>' % (
                    self.chalk_tag('喵叔说保'), sp('color:#B9C4BC;letter-spacing:2px;', '黑板课 · ' + m.get('date', '')))
                 + '<p style="margin:0 0 6px;font-size:13px;line-height:1.6;color:%s;letter-spacing:2px;font-family:%s;">%s</p>' % (CHALKY, KAI, leaf('今日板书：' + m.get('kicker', '').split(' · ')[-1]))
                 + '<p style="margin:0 0 14px;font-size:24px;line-height:1.5;color:%s;font-weight:bold;font-family:%s;">%s</p>' % (CHALK, KAI, self.head_title())
                 + blank('height:0;border-top:2px dashed %s;margin:0 0 12px;width:60%%;line-height:0;font-size:0;' % CHALKY)
                 + '<p style="margin:0;font-size:12px;line-height:1.6;color:#B9C4BC;">%s</p>' % leaf('防坑｜买对｜赔好　·　喵叔'))
        return sec('padding:18px 0 0;', self.board(inner, '22px 18px 20px', '0 12px 0')
                   .replace('margin:0 16px 24px;height:8px', 'margin:0 12px 28px;height:8px'))

    # 章节：红笔圈号 + 楷体标题 + 荧光半截
    def b_h2(self, b):
        self.chap += 1
        return sec('margin:36px 16px 16px;',
            '<table style="border-collapse:collapse;"><tbody><tr>'
            '<td style="width:34px;padding:0;vertical-align:middle;"><p style="margin:0;font-size:15px;line-height:26px;">%s</p></td>'
            '<td style="padding:0 0 0 8px;vertical-align:middle;"><p style="margin:0;font-size:20px;line-height:1.5;color:%s;font-weight:bold;font-family:%s;">%s</p></td>'
            '</tr></tbody></table>' % (
                sp('display:inline-block;width:24px;height:24px;line-height:24px;border:2px solid %s;border-radius:50%%;color:%s;text-align:center;font-weight:bold;letter-spacing:0;' % (RED, RED), str(self.chap)),
                INK, KAI, sp('box-shadow:inset 0 -10px 0 %s;padding:0 2px;' % HL, b['text'])))

    def b_case(self, b):
        title, label = (b['args'] + ['', ''])[:2]
        return sec('margin:0 16px 22px;padding:12px 14px 4px;background:#FFFFFF;border:1px solid %s;border-left:4px solid %s;' % (LINE, BOARD),
            '<p style="margin:0 0 10px;font-size:13px;line-height:1.6;">%s%s</p>' % (self.chalk_tag(label, BOARD, CHALK), sp('color:%s;font-weight:bold;font-family:%s;' % (INK, KAI), title))
            + ''.join(self.p(t, 'font-size:14px;margin-bottom:10px;') for t in b['paras']))

    def b_lead(self, b):
        return sec('margin:0 16px 24px;padding:4px 0 4px 14px;border-left:4px solid %s;' % HL,
            ''.join(self.p(t, 'margin:0;font-size:16px;color:%s;font-weight:bold;' % INK) for t in b['paras']))

    # 划重点：红笔「✎ 划重点」+ 白卡
    def b_key(self, b):
        return sec('margin:4px 16px 24px;padding:12px 14px;background:#FFFFFF;border:2px dashed %s;' % RED,
            '<p style="margin:0 0 6px;font-size:13px;line-height:1.5;color:%s;font-weight:bold;font-family:%s;">%s</p>' % (RED, KAI, leaf('✎ 划重点'))
            + ''.join(self.p(t, 'margin:0;color:%s;font-weight:bold;' % INK) for t in b['paras']))

    # 便签：名词解释
    def b_term(self, b):
        return sec('margin:0 16px 24px;padding:12px 14px 2px;background:%s;box-shadow:3px 3px 0 #E8DC9A;' % NOTE,
            '<p style="margin:0 0 8px;font-size:13px;line-height:1.6;">%s%s</p>' % (
                self.chalk_tag('名词', INK, NOTE), sp('color:%s;font-weight:bold;font-size:16px;font-family:%s;' % (INK, KAI), b['args'][0] if b['args'] else ''))
            + ''.join(self.p(t, 'font-size:14px;margin-bottom:10px;') for t in b['paras']))

    def b_example(self, b):
        return sec('margin:0 16px 20px;padding:12px 14px 2px;background:#FFFFFF;border:1px solid %s;' % LINE,
            '<p style="margin:0 0 8px;font-size:13px;line-height:1.6;">%s%s</p>' % (
                self.chalk_tag('举例', BOARD, CHALK), sp('color:%s;font-weight:bold;font-family:%s;' % (INK, KAI), b['args'][0] if b['args'] else ''))
            + ''.join(self.p(t, 'font-size:14px;margin-bottom:10px;') for t in b['paras']))

    # 易错：红笔虚框
    def b_warn(self, b):
        return sec('margin:0 16px 22px;padding:12px 14px 2px;background:#FFFFFF;border:1px dashed %s;' % RED,
            '<p style="margin:0 0 8px;font-size:14px;line-height:1.6;color:%s;font-weight:bold;font-family:%s;">%s</p>' % (
                RED, KAI, leaf('✗ 易错｜' + (b['args'][0] if b['args'] else '')))
            + ''.join(self.p(t, 'font-size:14px;margin-bottom:10px;') for t in b['paras']))

    # 条款卡：白卡抄原文，下方小黑板写「人话」
    def b_clause(self, b):
        name, ins, lead = (b['args'] + ['', '', ''])[:3]
        return sec('margin:0 16px 16px;background:#FFFFFF;border:1px solid %s;' % LINE,
            sec('padding:10px 14px 6px;',
                '<p style="margin:0;font-size:16px;line-height:1.5;color:%s;font-weight:bold;font-family:%s;">%s</p>' % (INK, KAI, sp('box-shadow:inset 0 -8px 0 %s;padding:0 2px;' % HL, name))
                + '<p style="margin:2px 0 8px;font-size:12px;line-height:1.6;color:%s;">%s</p>' % (MUTE, self.rich(ins + '。' + lead + '：'))
                + '<p style="margin:0 0 4px;font-size:14px;line-height:1.8;color:%s;text-align:justify;">%s</p>' % (SUB, self.rich(b['text'])))
            + sec('padding:10px 14px;background:%s;' % BOARD,
                '<p style="margin:0;font-size:14px;line-height:1.6;color:%s;font-weight:bold;">%s%s</p>' % (CHALK, self.chalk_tag('人话'), leaf(b['note']))))

    # 公式板：一行公式 + 代入，粉笔书写
    def b_formula(self, b):
        title = b['args'][0] if b['args'] else ''
        rows = b['rows']
        inner = '<p style="margin:0 0 12px;font-size:12px;line-height:1.6;">%s</p>' % self.chalk_tag(title)
        for i, r in enumerate(rows):
            k, v = (r + ['', ''])[:2]
            last = i == len(rows) - 1
            inner += ('<p style="margin:0 0 %s;font-size:12px;line-height:1.5;color:#B9C4BC;letter-spacing:1px;">%s</p>'
                      '<p style="margin:0 0 14px;font-size:%dpx;line-height:1.5;color:%s;font-weight:bold;font-family:%s;">%s</p>' % (
                          '2px', leaf(k), 22 if last else 17, CHALKY if last else CHALK, KAI,
                          sp('border:2px solid %s;border-radius:22px;padding:2px 10px;' % CHALKY, v) if last else leaf(v)))
        inner += ''.join('<p style="margin:0;font-size:12px;line-height:1.7;color:#B9C4BC;">%s</p>' % self.rich(t) for t in b['paras'])
        return self.board(inner)

    # 黑板推演：原文逐行写在黑板上，结果用粉笔圈出来
    def b_calc(self, b):
        inner = '<p style="margin:0 0 12px;font-size:12px;line-height:1.6;">%s</p>' % self.chalk_tag(b['args'][0])
        # 推演行：左侧粉笔黄短竖线（装饰不进文字流，免得和原文粘连影响校验）
        inner += ''.join('<p style="margin:0 0 10px;padding-left:10px;border-left:2px solid %s;font-size:14px;line-height:1.85;color:%s;text-align:justify;">%s</p>' % (
            CHALKY, CHALK, self.rich(t, color=CHALK)) for t in b['lines'])
        tds = ''
        for i, (label, num, note) in enumerate(b['cards']):
            hot = i == len(b['cards']) - 1
            tds += ('<td style="width:50%%;padding:12px 6px 4px;vertical-align:top;text-align:center;%s">'
                    '<p style="margin:0 0 6px;font-size:12px;line-height:1.5;color:#B9C4BC;">%s</p>'
                    '<p style="margin:0 0 6px;font-size:24px;line-height:1.3;font-weight:bold;">%s</p>'
                    '<p style="margin:0;font-size:11px;line-height:1.5;color:#B9C4BC;">%s</p></td>' % (
                        '' if i == 0 else 'border-left:1px dashed #6E8075;', '<br>'.join(leaf(x) for x in label.split(' · ')),
                        sp('display:inline-block;padding:2px 12px;border:2px solid %s;border-radius:24px;color:%s;' % (CHALKY if hot else '#9DB0A5', CHALKY if hot else CHALK), num),
                        leaf(note)))
        inner += (blank('height:0;border-top:1px dashed #6E8075;margin:6px 0 0;line-height:0;font-size:0;')
                  + '<p style="margin:10px 0 0;font-size:13px;line-height:1.5;color:%s;text-align:center;font-weight:bold;font-family:%s;">%s</p>' % (CHALKY, KAI, leaf(b['cards_title']))
                  + '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody><tr>%s</tr></tbody></table>' % tds)
        return self.board(inner)

    # 板书表：黑板绿表头 + 笔记纸行，差异格荧光黄
    def table(self, rows):
        head, body = rows[0], rows[1:]
        n = len(head)
        w0 = 34 if n > 2 else 64
        wi = (100 - w0) // max(1, n - 1)
        th = ''.join('<td style="padding:8px 4px;background:%s;color:%s;font-size:12px;line-height:1.4;font-weight:bold;text-align:%s;width:%d%%;">%s</td>'
                     % (BOARD, CHALK if i == 0 else CHALKY, 'left' if i == 0 else 'center', w0 if i == 0 else wi, leaf(c)) for i, c in enumerate(head))
        trs = []
        for row in body:
            tds = []
            for i, c in enumerate(row):
                hot = c.startswith('==')
                c = c.strip('=')
                inner = self.rich(c) if not hot else sp('box-shadow:inset 0 -8px 0 %s;font-weight:bold;color:%s;padding:0 2px;' % (HL, INK), c)
                tds.append('<td style="padding:9px 4px;border-bottom:1px dashed #D5CFBE;font-size:13px;line-height:1.45;text-align:%s;color:%s;%s">%s</td>'
                           % ('left' if i == 0 else 'center', INK if i == 0 else SUB, 'font-weight:bold;' if i == 0 else '', inner))
            trs.append('<tr>%s</tr>' % ''.join(tds))
        return ('<table style="width:100%%;border-collapse:collapse;table-layout:fixed;background:#FFFFFF;border:1px solid %s;"><tbody><tr>%s</tr>%s</tbody></table>'
                % (LINE, th, ''.join(trs)))

    def b_table(self, b):
        title, sub = (b['args'] + ['', ''])[:2]
        return sec('margin:0 16px 24px;',
            '<p style="margin:0 0 8px;font-size:16px;line-height:1.5;color:%s;font-weight:bold;font-family:%s;">%s</p>' % (INK, KAI, leaf('▍' + title))
            + self.table(b['rows'])
            + '<p style="margin:6px 0 0;font-size:12px;line-height:1.6;color:%s;">%s</p>' % (MUTE, self.rich(sub)))

    # 荧光笔条：粗黄条 + 墨色数值
    def b_bars(self, b):
        title, unit = (b['args'] + ['', ''])[:2]
        mx = max(v for _, v in b['items'])
        rows = []
        for name, v in b['items']:
            w = max(6, int(round(v / mx * 100)))
            nm, _, subt = name.partition(' · ')
            rows.append('<tr><td style="width:36%%;padding:6px 6px 6px 0;font-size:13px;line-height:1.35;color:%s;vertical-align:middle;">%s%s</td>'
                        '<td style="padding:6px 0;vertical-align:middle;">%s</td>'
                        '<td style="width:48px;padding:6px 0 6px 6px;vertical-align:middle;"><p style="margin:0;font-size:14px;line-height:1;color:%s;font-weight:bold;text-align:right;">%s</p></td></tr>' % (
                            INK, leaf(nm), ('<br>' + sp('color:%s;font-size:11px;' % MUTE, subt)) if subt else '',
                            blank('width:%d%%;height:14px;background:%s;line-height:14px;font-size:0;' % (w, HL if v != mx else '#F7C948')),
                            RED if v == mx else INK, leaf('%g' % v)))
        return sec('margin:0 16px 24px;padding:14px;background:#FFFFFF;border:1px solid %s;' % LINE,
            '<p style="margin:0 0 6px;font-size:16px;line-height:1.5;color:%s;font-weight:bold;font-family:%s;">%s</p>' % (INK, KAI, leaf(title))
            + '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody>%s</tbody></table>' % ''.join(rows)
            + '<p style="margin:6px 0 0;font-size:12px;line-height:1.6;color:%s;">%s</p>' % (MUTE, self.rich(unit)))

    def numlist(self, items, labels):
        circ = '①②③④⑤⑥'
        out = []
        for i, t in enumerate(items):
            out.append('<tr><td style="width:28px;vertical-align:top;padding:0 0 12px;"><p style="margin:0;font-size:20px;line-height:27px;color:%s;font-weight:bold;">%s</p></td>'
                       '<td style="vertical-align:top;padding:0 0 12px 4px;">%s</td></tr>' % (RED, leaf(circ[i]), self.p(t, 'margin:0;font-size:14px;')))
        return '<table style="width:100%%;border-collapse:collapse;"><tbody>%s</tbody></table>' % ''.join(out)

    def b_steps(self, b):
        return sec('margin:0 16px 22px;padding:14px 14px 2px;background:#FFFFFF;border:1px solid %s;' % LINE, self.numlist(b['items'], None))

    def b_quote(self, b):
        inner = ''.join('<p style="margin:0;font-size:17px;line-height:1.75;color:%s;font-weight:bold;text-align:center;font-family:%s;">%s</p>' % (CHALKY, KAI, self.rich(t, color=CHALK)) for t in b['paras'])
        return self.board(inner, '16px 16px', '8px 16px 0')

    def b_verdict(self, b):
        inner = ('<p style="margin:0 0 10px;font-size:12px;line-height:1.6;">%s</p>' % self.chalk_tag('结论')
                 + ''.join('<p style="margin:0;font-size:18px;line-height:1.7;color:%s;font-weight:bold;font-family:%s;">%s</p>' % (CHALK, KAI, self.title_html(t, color=CHALK)) for t in b['paras']))
        return self.board(inner)

    def b_end(self, b):
        it = b['items']
        return sec('margin:30px 16px 16px;padding:16px 14px 14px;background:#FFFFFF;border:1px solid %s;text-align:center;' % LINE,
            '<p style="margin:0 0 10px;font-size:14px;line-height:1.8;color:%s;">%s</p>' % (SUB, self.rich(it[0]))
            + '<p style="margin:0 0 12px;font-size:15px;line-height:1.8;color:%s;font-weight:bold;">%s</p>' % (INK, self.rich(it[1]))
            + '<p style="margin:0;font-size:13px;line-height:1.6;">%s</p>' % sp(
                'display:inline-block;padding:4px 14px;background:%s;color:%s;font-weight:bold;' % (BOARD, CHALK), it[2]))
