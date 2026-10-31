"""主题④　IP蓝瑞士网格 · 清单指南（wangge）
米白底 + 墨黑粗细线 + 喵叔 IP 蓝 #0288D1；直角、编号网格、大号数字、方块标记。
静态化自视频 T68 IP蓝瑞士网格个人宣传片 / T64 瑞士网格（数字卡 + 进度条）。
适合：清单、选购指南、「先看什么后看什么」的排序型文章。
"""
import re

from base import sp, sec, blank, leaf, SANS
import miaolan

INK, BLUE, PAPER = '#111111', '#0288D1', '#F7F5F0'
TXT, SUB, MUTE, HAIR = '#2B2B2B', '#5C5C5C', '#8F8F8F', '#D6D2C8'
NUM = "'DIN Alternate','Helvetica Neue',Helvetica,Arial," + SANS


class T(miaolan.T):
    id = 'wangge'
    name = 'IP蓝瑞士网格 · 清单指南'
    P = dict(bg=PAPER, text=TXT, title=INK, muted=MUTE, line=HAIR, primary=BLUE,
             plight='#ECEAE3', hl='#D7ECF7', ul=BLUE, gold=INK, goldlight='#ECEAE3',
             red=INK, redlight='#ECEAE3')
    REMAP = {'#051A4C': INK, '#0288D1': BLUE, '#F2A900': INK, '#EEF7FD': '#ECEAE3',
             '#D6E9F5': HAIR, '#F7FAFD': '#FFFFFF', '#E3EAF2': HAIR, '#55606F': SUB,
             '#EEF2F6': '#E6E3DA', '#7FC6EE': '#9A9A9A', '#F1F4F8': '#ECEAE3', '#DDF0FB': '#D7ECF7',
             '#DCE6F0': HAIR, '#F6F8FA': '#FFFFFF', '#F5F9FC': '#FBFAF7', '#FFF7E0': '#ECEAE3',
             '#8A94A3': MUTE, '#3A4556': TXT, '#FFD666': '#7FD0F5', '#8CCDF0': BLUE}

    def post_inherit(self, h):
        return re.sub(r'border-radius:\d+px(?: \d+px)*;', 'border-radius:0;', h)

    def mark_style(self, kind):
        return {
            'anchor': 'color:%s;font-weight:bold;' % BLUE,
            'hl': 'background:#D7ECF7;padding:0 2px;',
            'ul': 'border-bottom:2px solid %s;font-weight:600;padding-bottom:1px;' % INK,
        }[kind]

    def rule(self, w=2, color=INK, m='0'):
        return blank('height:0;border-top:%dpx solid %s;margin:%s;line-height:0;font-size:0;' % (w, color, m))

    def label(self, t, color=MUTE):
        return '<p style="margin:0 0 6px;font-size:11px;line-height:1.5;color:%s;letter-spacing:2px;font-weight:bold;">%s</p>' % (color, leaf(t))

    # 刊头：粗线 + 三格元信息 + 大标题 + 蓝方块
    def header(self):
        m = self.meta
        cells = [('栏目', '喵叔说保'), ('类型', m.get('kicker', '').split(' · ')[0]), ('日期', m.get('date', ''))]
        tds = ''.join('<td style="width:33%%;padding:8px 6px 8px %s;vertical-align:top;border-left:%s;">'
                      '<p style="margin:0;font-size:10px;line-height:1.5;color:%s;letter-spacing:2px;">%s</p>'
                      '<p style="margin:0;font-size:13px;line-height:1.5;color:%s;font-weight:bold;">%s</p></td>' % (
                          '0' if i == 0 else '8px', 'none' if i == 0 else '1px solid %s' % HAIR, MUTE, leaf(k), INK, leaf(v))
                      for i, (k, v) in enumerate(cells))
        return sec('padding:22px 16px 0;margin:0 0 26px;',
            self.rule(6, INK, '0 0 0')
            + '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody><tr>%s</tr></tbody></table>' % tds
            + self.rule(1, INK, '0 0 22px')
            + '<p style="margin:0 0 4px;font-size:12px;line-height:1.5;color:%s;letter-spacing:2px;font-weight:bold;">%s</p>' % (BLUE, leaf('■ ' + m.get('kicker', '')))
            + '<p style="margin:0 0 18px;font-size:25px;line-height:1.42;color:%s;font-weight:bold;letter-spacing:0;">%s</p>' % (INK, self.head_title())
            + '<table style="width:100%%;border-collapse:collapse;"><tbody><tr>'
              '<td style="width:44px;padding:0;">%s</td><td style="padding:0 0 0 10px;"><p style="margin:0;font-size:11px;line-height:1.5;color:%s;letter-spacing:1px;">%s</p></td>'
              '</tr></tbody></table>' % (blank('width:44px;height:8px;background:%s;line-height:8px;font-size:0;' % BLUE), MUTE, leaf('防坑｜买对｜赔好　·　喵叔'))
            + self.rule(1, HAIR, '18px 0 0'))

    # 章节：左侧大号编号 + 右侧标题，下压细线
    def b_h2(self, b):
        self.chap += 1
        return sec('margin:36px 16px 16px;',
            self.rule(2, INK, '0 0 10px')
            + '<table style="width:100%%;border-collapse:collapse;"><tbody><tr>'
              '<td style="width:62px;padding:0;vertical-align:top;"><p style="margin:0;font-size:40px;line-height:1;color:%s;font-weight:bold;font-family:%s;letter-spacing:-1px;">%s</p></td>'
              '<td style="padding:2px 0 0 4px;vertical-align:top;"><p style="margin:0;font-size:19px;line-height:1.45;color:%s;font-weight:bold;">%s</p></td>'
              '</tr></tbody></table>' % (BLUE, NUM, leaf('%02d' % self.chap), INK, leaf(b['text'])))

    def b_case(self, b):
        title, label = (b['args'] + ['', ''])[:2]
        return sec('margin:0 16px 24px;background:#FFFFFF;border-top:2px solid %s;padding:12px 14px 4px;' % INK,
            self.label(label + '　/　' + title, BLUE)
            + ''.join(self.p(t, 'font-size:14px;margin-bottom:10px;') for t in b['paras']))

    def b_lead(self, b):
        return sec('margin:0 16px 24px;padding:0 0 0 14px;border-left:6px solid %s;' % BLUE,
            ''.join(self.p(t, 'margin:0;font-size:17px;line-height:1.7;color:%s;font-weight:bold;' % INK) for t in b['paras']))

    def b_key(self, b):
        return sec('margin:4px 16px 24px;padding:12px 0;border-top:2px solid %s;border-bottom:1px solid %s;' % (INK, INK),
            ''.join(self.p(t, 'margin:0;color:%s;font-weight:bold;' % INK) for t in b['paras']))

    # 条款卡：编号式表头 + 原文白底 + 蓝方块「人话」
    def b_clause(self, b):
        name, ins, lead = (b['args'] + ['', '', ''])[:3]
        self.clause_n = getattr(self, 'clause_n', 0) + 1
        return sec('margin:0 16px 16px;border-top:2px solid %s;' % INK,
            '<table style="width:100%%;border-collapse:collapse;"><tbody><tr>'
            '<td style="padding:8px 0 6px;vertical-align:bottom;"><p style="margin:0;font-size:16px;line-height:1.4;color:%s;font-weight:bold;">%s</p></td>'
            '<td style="width:40px;padding:8px 0 6px;vertical-align:bottom;text-align:right;"><p style="margin:0;font-size:20px;line-height:1;color:%s;font-weight:bold;font-family:%s;">%s</p></td>'
            '</tr></tbody></table>' % (INK, leaf(name), HAIR, NUM, leaf('%02d' % self.clause_n))
            + '<p style="margin:0 0 8px;font-size:12px;line-height:1.6;color:%s;">%s</p>' % (MUTE, self.rich(ins + '。' + lead + '：'))
            + sec('background:#FFFFFF;padding:10px 12px;',
                '<p style="margin:0;font-size:14px;line-height:1.8;color:%s;text-align:justify;">%s</p>' % (SUB, self.rich(b['text'])))
            + '<table style="width:100%%;border-collapse:collapse;border-bottom:1px solid %s;"><tbody><tr>'
              '<td style="width:52px;padding:9px 0;vertical-align:top;"><p style="margin:0;font-size:12px;line-height:1.7;color:%s;font-weight:bold;letter-spacing:1px;">%s</p></td>'
              '<td style="padding:9px 0;vertical-align:top;"><p style="margin:0;font-size:14px;line-height:1.6;color:%s;font-weight:bold;">%s</p></td>'
              '</tr></tbody></table>' % (INK, BLUE, leaf('■ 人话'), INK, leaf(b['note'])))

    # 数字网格：2 列格子，大号数字 + 单位 + 说明
    def b_grid(self, b):
        title, sub = (b['args'] + ['', ''])[:2]
        rows = b['rows']
        trs = []
        for r in range(0, len(rows), 2):
            tds = []
            for c in range(2):
                if r + c < len(rows):
                    num, unit, note = (rows[r + c] + ['', '', ''])[:3]
                    hot = num.startswith('==')
                    num = num.strip('=')
                    tds.append('<td style="width:50%%;padding:12px 10px 12px %s;vertical-align:top;border-bottom:1px solid %s;%s">'
                               '<p style="margin:0;font-size:30px;line-height:1.15;font-weight:bold;font-family:%s;color:%s;letter-spacing:-0.5px;">%s%s</p>'
                               '<p style="margin:4px 0 0;font-size:12px;line-height:1.5;color:%s;">%s</p></td>' % (
                                   '0' if c == 0 else '12px', HAIR, '' if c == 0 else 'border-left:1px solid %s;' % HAIR,
                                   NUM, BLUE if hot else INK, leaf(num), sp('font-size:13px;color:%s;font-weight:normal;margin-left:2px;letter-spacing:0;' % SUB, unit),
                                   SUB, leaf(note)))
                else:
                    tds.append('<td style="width:50%%;padding:0;border-bottom:1px solid %s;border-left:1px solid %s;">%s</td>' % (HAIR, HAIR, leaf('')))
            trs.append('<tr>%s</tr>' % ''.join(tds))
        return sec('margin:0 16px 24px;',
            self.rule(2, INK, '0 0 8px') + self.label(title, INK)
            + '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody>%s</tbody></table>' % ''.join(trs)
            + '<p style="margin:8px 0 0;font-size:11px;line-height:1.6;color:%s;">%s</p>' % (MUTE, self.rich(sub)))

    # 粗细线表格：上下粗线、行间细线、无底色；差异项蓝字 + 蓝方块
    def table(self, rows):
        head, body = rows[0], rows[1:]
        n = len(head)
        w0 = 34
        wi = (100 - w0) // (n - 1)
        th = ''.join('<td style="padding:8px 3px;border-bottom:1px solid %s;color:%s;font-size:11px;line-height:1.4;font-weight:bold;letter-spacing:1px;text-align:%s;width:%d%%;">%s</td>'
                     % (INK, MUTE, 'left' if i == 0 else 'center', w0 if i == 0 else wi, leaf(c)) for i, c in enumerate(head))
        trs = []
        for r, row in enumerate(body):
            last = r == len(body) - 1
            tds = []
            for i, c in enumerate(row):
                hot = c.startswith('==')
                c = c.strip('=')
                inner = leaf(c) if not hot else sp('color:%s;font-weight:bold;' % BLUE, '■ ' + c)
                tds.append('<td style="padding:9px 3px;border-bottom:%s;font-size:13px;line-height:1.4;text-align:%s;color:%s;%s">%s</td>'
                           % ('2px solid %s' % INK if last else '1px solid %s' % HAIR, 'left' if i == 0 else 'center',
                              INK if i == 0 else SUB, 'font-weight:bold;' if i == 0 else '', inner))
            trs.append('<tr>%s</tr>' % ''.join(tds))
        return ('<table style="width:100%%;border-collapse:collapse;table-layout:fixed;border-top:2px solid %s;"><tbody><tr>%s</tr>%s</tbody></table>'
                % (INK, th, ''.join(trs)))

    def b_table(self, b):
        title, sub = (b['args'] + ['', ''])[:2]
        return sec('margin:0 16px 26px;',
            self.label('TABLE　/　' + title, INK)
            + self.table(b['rows'])
            + '<p style="margin:8px 0 0;font-size:11px;line-height:1.6;color:%s;">%s</p>' % (MUTE, self.rich(sub)))

    # 进度条：方头细条，数值写在条外右侧
    def b_bars(self, b):
        title, unit = (b['args'] + ['', ''])[:2]
        mx = max(v for _, v in b['items'])
        rows = []
        for name, v in b['items']:
            w = max(4, int(round(v / mx * 100)))
            hot = v == mx
            nm, _, subt = name.partition(' · ')
            rows.append('<tr><td colspan="2" style="padding:10px 0 4px;"><p style="margin:0;font-size:13px;line-height:1.4;color:%s;font-weight:bold;">%s%s</p></td></tr>'
                        '<tr><td style="padding:0;vertical-align:middle;">%s</td>'
                        '<td style="width:58px;padding:0 0 0 8px;vertical-align:middle;"><p style="margin:0;font-size:15px;line-height:1;color:%s;font-weight:bold;font-family:%s;text-align:right;">%s</p></td></tr>' % (
                            INK, leaf(nm), sp('color:%s;font-weight:normal;font-size:11px;margin-left:6px;' % MUTE, subt) if subt else '',
                            sec('background:#E6E3DA;height:10px;line-height:10px;font-size:0;',
                                blank('width:%d%%;height:10px;background:%s;line-height:10px;font-size:0;' % (w, BLUE if hot else INK))),
                            BLUE if hot else INK, NUM, leaf(('%g' % v))))
        return sec('margin:0 16px 26px;',
            self.rule(2, INK, '0 0 8px') + self.label(title, INK)
            + '<table style="width:100%%;border-collapse:collapse;"><tbody>%s</tbody></table>' % ''.join(rows)
            + '<p style="margin:10px 0 0;font-size:11px;line-height:1.6;color:%s;">%s</p>' % (MUTE, self.rich(unit)))

    def b_warn(self, b):
        return sec('margin:0 16px 22px;padding:12px 14px 2px;background:#FFFFFF;border:1px solid %s;border-left:6px solid %s;' % (INK, INK),
            self.label('注意　/　' + (b['args'][0] if b['args'] else ''), INK)
            + ''.join(self.p(t, 'font-size:14px;margin-bottom:10px;') for t in b['paras']))

    def numlist(self, items, labels):
        out = []
        for i, t in enumerate(items):
            out.append('<tr><td style="width:46px;vertical-align:top;padding:12px 0;border-top:1px solid %s;">'
                       '<p style="margin:0;font-size:26px;line-height:1;color:%s;font-weight:bold;font-family:%s;">%s</p></td>'
                       '<td style="vertical-align:top;padding:12px 0 12px 6px;border-top:1px solid %s;">%s</td></tr>' % (
                           INK if i == 0 else HAIR, BLUE, NUM, leaf('%02d' % (i + 1)), INK if i == 0 else HAIR,
                           self.p(t, 'margin:0;font-size:14px;')))
        return '<table style="width:100%%;border-collapse:collapse;"><tbody>%s</tbody></table>' % ''.join(out)

    def b_steps(self, b):
        return sec('margin:0 16px 22px;padding:0 14px;background:#FFFFFF;', self.numlist(b['items'], None))

    # 顺序清单：一行一项，编号 + 关键词 + 位次标签，用于「先看什么后看什么」
    def b_seq(self, b):
        title, sub = (b['args'] + ['', ''])[:2]
        trs = []
        for i, row in enumerate(b['rows']):
            num, txt, tagt = (row + ['', '', ''])[:3]
            hot = i == 0
            trs.append('<tr><td style="width:54px;padding:10px 0;border-bottom:1px solid %s;vertical-align:middle;%s">'
                       '<p style="margin:0;font-size:28px;line-height:1;font-weight:bold;font-family:%s;color:%s;text-align:center;">%s</p></td>'
                       '<td style="padding:10px 10px;border-bottom:1px solid %s;vertical-align:middle;"><p style="margin:0;font-size:15px;line-height:1.45;color:%s;font-weight:bold;">%s</p></td>'
                       '<td style="width:56px;padding:10px 0;border-bottom:1px solid %s;vertical-align:middle;text-align:right;"><p style="margin:0;font-size:11px;line-height:1.4;color:%s;letter-spacing:1px;">%s</p></td></tr>' % (
                           HAIR, 'background:%s;' % BLUE if hot else '', NUM, '#FFFFFF' if hot else INK, leaf(num),
                           HAIR, INK, leaf(txt), HAIR, BLUE if hot else MUTE, leaf(tagt)))
        return sec('margin:0 16px 24px;',
            self.rule(6, INK, '0 0 8px') + self.label(title, INK)
            + '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody>%s</tbody></table>' % ''.join(trs)
            + ('<p style="margin:8px 0 0;font-size:11px;line-height:1.6;color:%s;">%s</p>' % (MUTE, self.rich(sub)) if sub else ''))

    def b_quote(self, b):
        return sec('margin:10px 16px 28px;padding:14px 0;border-top:6px solid %s;border-bottom:1px solid %s;' % (INK, INK),
            ''.join('<p style="margin:0;font-size:19px;line-height:1.6;color:%s;font-weight:bold;">%s</p>' % (INK, self.rich(t)) for t in b['paras']))

    def b_verdict(self, b):
        return sec('margin:0 16px 22px;padding:16px;background:%s;' % INK,
            '<table style="width:100%%;border-collapse:collapse;margin:0 0 10px;"><tbody><tr><td style="width:18px;padding:0;">%s</td>'
            '<td style="padding:0 0 0 8px;"><p style="margin:0;font-size:11px;line-height:1.4;color:#BDBDBD;letter-spacing:2px;font-weight:bold;">%s</p></td></tr></tbody></table>' % (
                blank('width:12px;height:12px;background:%s;line-height:12px;font-size:0;' % BLUE), leaf('判断线'))
            + ''.join('<p style="margin:0;font-size:19px;line-height:1.55;color:#FFFFFF;font-weight:bold;">%s</p>' % self.title_html(t, color='#7FD0F5')
                      for t in b['paras']))

    def datacards(self, title, cards):
        tds = []
        for i, (label, num, note) in enumerate(cards):
            hot = i == len(cards) - 1
            tds.append('<td style="width:50%%;padding:10px %s 10px %s;vertical-align:top;%s">'
                       '<p style="margin:0;font-size:11px;line-height:1.5;color:%s;">%s</p>'
                       '<p style="margin:4px 0;font-size:34px;line-height:1.1;font-weight:bold;font-family:%s;color:%s;">%s</p>'
                       '<p style="margin:0;font-size:11px;line-height:1.5;color:%s;">%s</p></td>' % (
                           '8px' if i == 0 else '0', '0' if i == 0 else '12px', '' if i == 0 else 'border-left:1px solid %s;' % HAIR,
                           MUTE, leaf(label), NUM, BLUE if hot else INK, leaf(num), SUB, leaf(note)))
        return (self.label(title, INK)
                + '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;border-top:2px solid %s;border-bottom:1px solid %s;"><tbody><tr>%s</tr></tbody></table>' % (INK, INK, ''.join(tds)))

    def b_calc(self, b):
        return sec('margin:0 16px 24px;padding:14px;background:#FFFFFF;border-top:6px solid %s;' % BLUE,
            self.label('CALC　/　' + b['args'][0], BLUE)
            + ''.join(self.p(t, 'font-size:14px;margin-bottom:8px;') for t in b['lines'])
            + sec('margin-top:12px;', self.datacards(b['cards_title'], b['cards'])))

    def b_end(self, b):
        it = b['items']
        return sec('margin:34px 16px 16px;',
            self.rule(6, INK, '0 0 14px')
            + '<p style="margin:0 0 10px;font-size:14px;line-height:1.8;color:%s;">%s</p>' % (SUB, self.rich(it[0]))
            + '<p style="margin:0 0 14px;font-size:15px;line-height:1.8;color:%s;font-weight:bold;">%s</p>' % (INK, self.rich(it[1]))
            + '<p style="margin:0 0 14px;font-size:13px;line-height:1.6;">%s</p>' % sp(
                'display:inline-block;padding:5px 14px;background:%s;color:#FFFFFF;font-weight:bold;' % BLUE, it[2])
            + self.rule(1, INK, '0'))

    def b_disclaimer(self, b):
        return sec('margin:0 16px 10px;padding:10px 0 0;',
            ''.join('<p style="margin:0;font-size:11px;line-height:1.7;color:%s;text-align:justify;">%s</p>' % (MUTE, self.rich(t))
                    for t in b['paras']))
