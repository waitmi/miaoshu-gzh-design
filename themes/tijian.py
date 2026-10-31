"""主题⑤　保单体检报告单 · 诊断排查（tijian）
米白化验单底 + 检验蓝 #1F5FA8 结构线；绿✓正常 / 灰!注意 / 红✕限制；检验项目表、判读、诊断意见。
静态化自视频 T72 保单体检报告单一镜到底 / T12 体检报告（报告单表格逐行展开，异常项标红加批注）。
适合：保单诊断、条款避坑排查、「这张保单保了什么没保什么」。
"""
import re

from base import sp, sec, blank, leaf, SANS
import miaolan

BLUE, INK, PAPER = '#1F5FA8', '#1E2329', '#FBFAF6'
OK, BAD = '#23955B', '#D23F3F'
TXT, SUB, MUTE, LINE, PALE = '#333A44', '#5A626D', '#8D949E', '#DCDFE3', '#EEF3F9'
MONO = "'SF Mono',Menlo,Consolas,'Roboto Mono'," + SANS
FLAG = {'ok': ('✓', OK, '#E8F5EE'), 'warn': ('！', '#6B7280', '#F1F2F4'), 'bad': ('✕', BAD, '#FDECEC')}


class T(miaolan.T):
    id = 'tijian'
    name = '保单体检报告单 · 诊断排查'
    P = dict(bg=PAPER, text=TXT, title=INK, muted=MUTE, line=LINE, primary=BLUE,
             plight=PALE, hl='#E3ECF7', ul='#8FB0D8', gold=BLUE, goldlight=PALE,
             red=BAD, redlight='#FDECEC')
    REMAP = {'#051A4C': INK, '#0288D1': BLUE, '#F2A900': BLUE, '#EEF7FD': PALE,
             '#D6E9F5': LINE, '#F7FAFD': '#FFFFFF', '#E3EAF2': LINE, '#55606F': SUB,
             '#EEF2F6': '#ECEEF1', '#7FC6EE': '#9DB5D6', '#F1F4F8': '#F1F3F5', '#DDF0FB': '#DCE7F5',
             '#DCE6F0': LINE, '#F6F8FA': '#FFFFFF', '#F5F9FC': '#F8F9FA', '#FFF7E0': PALE,
             '#8A94A3': MUTE, '#3A4556': TXT, '#FFD666': '#FFFFFF', '#8CCDF0': '#8FB0D8'}

    def post_inherit(self, h):
        return re.sub(r'border-radius:\d+px(?: \d+px)*;', 'border-radius:2px;', h)

    def mark_style(self, kind):
        return {
            'anchor': 'color:%s;font-weight:bold;' % BLUE,
            'hl': 'background:#E3ECF7;padding:0 2px;',
            'ul': 'border-bottom:2px solid #8FB0D8;font-weight:600;padding-bottom:1px;',
        }[kind]

    def flag(self, k, size=20):
        ch, c, bg = FLAG.get(k, FLAG['warn'])
        return sp('display:inline-block;width:%dpx;height:%dpx;line-height:%dpx;border-radius:50%%;background:%s;color:#FFFFFF;'
                  'text-align:center;font-size:%dpx;font-weight:bold;letter-spacing:0;' % (size, size, size, c, size - 8), ch)

    def lab(self, t, color=BLUE):
        return sp('display:inline-block;padding:0 6px;margin-right:6px;background:%s;color:#FFFFFF;font-size:12px;font-weight:bold;letter-spacing:1px;' % color, t)

    def dash(self, m='0'):
        return blank('height:0;border-top:1px dashed #C5CAD1;margin:%s;line-height:0;font-size:0;' % m)

    # 报告单抬头：机构行 + 大标题 + 蓝粗线 + 信息栏 + 图例
    def header(self):
        m = self.meta
        info = [('送检项目', m.get('sample') or m.get('kicker', '').split(' · ')[-1]), ('检验类型', m.get('kicker', '').split(' · ')[0]),
                ('报告日期', m.get('date', '')), ('检验', '喵叔')]
        cells = ''
        for r in range(2):
            tds = ''
            for c in range(2):
                k, v = info[r * 2 + c]
                tds += ('<td style="width:%s;padding:6px 0;vertical-align:top;border-bottom:1px solid %s;">'
                        '<p style="margin:0;font-size:12px;line-height:1.5;color:%s;">%s%s</p></td>' % (
                            '62%' if c == 0 else '38%', LINE, INK, sp('color:%s;margin-right:6px;' % MUTE, k + '：'), leaf(v)))
            cells += '<tr>%s</tr>' % tds
        legend = ''.join('%s%s' % (self.flag(k, 16), sp('font-size:11px;color:%s;margin:0 12px 0 4px;' % SUB, t))
                         for k, t in (('ok', '正常'), ('warn', '注意'), ('bad', '限制')))
        return sec('padding:22px 16px 0;margin:0 0 24px;',
            '<table style="width:100%%;border-collapse:collapse;"><tbody><tr>'
            '<td style="padding:0;"><p style="margin:0;font-size:12px;line-height:1.5;color:%s;font-weight:bold;letter-spacing:2px;">%s</p></td>'
            '<td style="padding:0;text-align:right;"><p style="margin:0;font-size:11px;line-height:1.5;color:%s;font-family:%s;">%s</p></td>'
            '</tr></tbody></table>' % (BLUE, leaf('喵叔说保 · 保单体检'), MUTE, MONO, leaf('No.' + m.get('date', '').replace('.', '')))
            + '<p style="margin:10px 0 10px;font-size:24px;line-height:1.3;color:%s;font-weight:bold;letter-spacing:6px;text-align:center;">%s</p>' % (INK, leaf('保单体检报告单'))
            + blank('height:0;border-top:3px solid %s;margin:0 0 2px;line-height:0;font-size:0;' % BLUE)
            + blank('height:0;border-top:1px solid %s;margin:0 0 4px;line-height:0;font-size:0;' % BLUE)
            + '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody>%s</tbody></table>' % cells
            + sec('margin:16px 0 0;padding:14px;background:#FFFFFF;border:1px solid %s;' % LINE,
                '<p style="margin:0 0 6px;font-size:11px;line-height:1.5;color:%s;letter-spacing:2px;">%s</p>' % (MUTE, leaf('本期结论题'))
                + '<p style="margin:0;font-size:20px;line-height:1.5;color:%s;font-weight:bold;">%s</p>' % (INK, self.head_title()))
            + '<p style="margin:10px 0 0;font-size:11px;line-height:20px;">%s</p>' % legend)

    def b_h2(self, b):
        self.chap += 1
        return sec('margin:34px 16px 16px;',
            '<table style="width:100%%;border-collapse:collapse;border-bottom:1px solid %s;"><tbody><tr>'
            '<td style="width:4px;padding:0;background:%s;">%s</td>'
            '<td style="padding:2px 0 8px 10px;"><p style="margin:0;font-size:11px;line-height:1.5;color:%s;font-weight:bold;letter-spacing:2px;font-family:%s;">%s</p>'
            '<p style="margin:0;font-size:18px;line-height:1.45;color:%s;font-weight:bold;">%s</p></td>'
            '</tr></tbody></table>' % (INK, BLUE, leaf(''), BLUE, MONO, leaf('检查项目 %02d' % self.chap), INK, leaf(b['text'])))

    def b_case(self, b):
        title, label = (b['args'] + ['', ''])[:2]
        return sec('margin:0 16px 22px;background:#FFFFFF;border:1px solid %s;padding:12px 14px 4px;' % LINE,
            '<p style="margin:0 0 10px;font-size:13px;line-height:1.6;">%s%s</p>' % (self.lab(label or '主诉'), sp('color:%s;font-weight:bold;' % INK, title))
            + ''.join(self.p(t, 'font-size:14px;margin-bottom:10px;') for t in b['paras']))

    def b_lead(self, b):
        return sec('margin:0 16px 24px;padding:12px 14px;background:%s;border-left:3px solid %s;' % (PALE, BLUE),
            '<p style="margin:0 0 4px;font-size:11px;line-height:1.5;color:%s;font-weight:bold;letter-spacing:2px;">%s</p>' % (BLUE, leaf('检查重点'))
            + ''.join(self.p(t, 'margin:0;font-size:16px;color:%s;font-weight:bold;' % INK) for t in b['paras']))

    def b_basis(self, b):
        title, sub = (b['args'] + ['', ''])[:2]
        return sec('margin:0 16px 20px;padding:12px 14px 2px;background:#F3F4F6;border:1px dashed #B9C0C9;',
            '<p style="margin:0 0 8px;font-size:13px;line-height:1.6;">%s%s</p>' % (self.lab(title, INK), sp('color:%s;font-size:12px;' % SUB, sub))
            + ''.join(self.p(t, 'font-size:14px;margin-bottom:10px;') for t in b['paras']))

    # 检验项目表：项目 / 结果 / 说明 / 标志
    def b_report(self, b):
        title, sub = (b['args'] + ['', ''])[:2]
        head = ('<tr>' + ''.join('<td style="padding:7px 4px;background:%s;color:%s;font-size:11px;line-height:1.4;font-weight:bold;text-align:%s;width:%s;">%s</td>'
                % (PALE, BLUE, al, w, leaf(t)) for t, al, w in (('检查项目', 'left', '30%'), ('结果', 'left', '24%'), ('提示', 'left', '34%'), ('标志', 'center', '12%'))) + '</tr>')
        trs = []
        for row in b['rows']:
            item, res, note, fk = (row + ['', '', '', 'warn'])[:4]
            c = FLAG.get(fk, FLAG['warn'])[1]
            trs.append('<tr><td style="padding:9px 4px;border-bottom:1px dashed #D3D7DC;font-size:13px;line-height:1.45;color:%s;font-weight:bold;vertical-align:top;">%s</td>'
                       '<td style="padding:9px 4px;border-bottom:1px dashed #D3D7DC;font-size:13px;line-height:1.45;color:%s;font-weight:bold;vertical-align:top;">%s</td>'
                       '<td style="padding:9px 4px;border-bottom:1px dashed #D3D7DC;font-size:12px;line-height:1.5;color:%s;vertical-align:top;">%s</td>'
                       '<td style="padding:9px 0;border-bottom:1px dashed #D3D7DC;text-align:center;vertical-align:top;"><p style="margin:0;line-height:20px;font-size:12px;">%s</p></td></tr>' % (
                           INK, self.rich(item), c if fk != 'warn' else INK, self.rich(res), SUB, self.rich(note), self.flag(fk)))
        return sec('margin:0 16px 24px;background:#FFFFFF;border:1px solid %s;border-top:3px solid %s;padding:12px 12px 10px;' % (LINE, BLUE),
            '<p style="margin:0 0 8px;font-size:15px;line-height:1.5;color:%s;font-weight:bold;">%s</p>' % (INK, leaf(title))
            + '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody>%s%s</tbody></table>' % (head, ''.join(trs))
            + ('<p style="margin:8px 0 0;font-size:11px;line-height:1.6;color:%s;">%s</p>' % (MUTE, self.rich(sub)) if sub else ''))

    # 检验原文：样本名 + 原文（虚线框）+ 判读
    def b_clause(self, b):
        name, ins, lead = (b['args'] + ['', '', ''])[:3]
        return sec('margin:0 16px 16px;background:#FFFFFF;border:1px solid %s;' % LINE,
            sec('padding:8px 12px;border-bottom:1px solid %s;' % LINE,
                '<p style="margin:0;font-size:15px;line-height:1.5;color:%s;font-weight:bold;">%s%s</p>' % (INK, self.lab('样本'), leaf(name))
                + '<p style="margin:2px 0 0;font-size:12px;line-height:1.6;color:%s;">%s</p>' % (MUTE, self.rich(ins + '。' + lead + '：')))
            + sec('margin:10px 12px;padding:8px 10px;border:1px dashed #C5CAD1;',
                '<p style="margin:0;font-size:14px;line-height:1.8;color:%s;text-align:justify;">%s</p>' % (SUB, self.rich(b['text'])))
            + sec('padding:8px 12px;background:%s;' % PALE,
                '<p style="margin:0;font-size:14px;line-height:1.6;color:%s;font-weight:bold;">%s%s</p>' % (
                    INK, sp('color:%s;margin-right:6px;' % BLUE, '判读｜'), leaf(b['note']))))

    def b_key(self, b):
        return sec('margin:4px 16px 24px;padding:12px 14px;background:#FFFFFF;border:1px solid %s;border-left:3px solid %s;' % (LINE, BLUE),
            '<p style="margin:0 0 4px;font-size:11px;line-height:1.5;color:%s;font-weight:bold;letter-spacing:2px;">%s</p>' % (BLUE, leaf('判读要点'))
            + ''.join(self.p(t, 'margin:0;color:%s;font-weight:bold;' % INK) for t in b['paras']))

    def b_example(self, b):
        return sec('margin:0 16px 20px;padding:12px 14px 2px;background:#FFFFFF;border:1px solid %s;' % LINE,
            '<p style="margin:0 0 8px;font-size:13px;line-height:1.6;">%s%s</p>' % (self.lab('病例', INK), sp('color:%s;font-weight:bold;' % INK, b['args'][0] if b['args'] else ''))
            + ''.join(self.p(t, 'font-size:14px;margin-bottom:10px;') for t in b['paras']))

    def b_term(self, b):
        return sec('margin:0 16px 22px;padding:12px 14px 2px;background:%s;' % PALE,
            '<p style="margin:0 0 8px;font-size:13px;line-height:1.6;">%s%s</p>' % (self.lab('名词释义'), sp('color:%s;font-weight:bold;' % INK, b['args'][0] if b['args'] else ''))
            + ''.join(self.p(t, 'font-size:14px;margin-bottom:10px;') for t in b['paras']))

    def b_warn(self, b):
        return sec('margin:0 16px 22px;padding:12px 14px 2px;background:#FFFFFF;border:1px solid #F0C4C4;border-left:3px solid %s;' % BAD,
            '<p style="margin:0 0 8px;font-size:14px;line-height:20px;">%s%s</p>' % (
                self.flag('bad'), sp('color:%s;font-weight:bold;margin-left:6px;' % BAD, '异常提示｜' + (b['args'][0] if b['args'] else '')))
            + ''.join(self.p(t, 'font-size:14px;margin-bottom:10px;') for t in b['paras']))

    # 异常项标签：一组红框小标签
    def b_chips(self, b):
        title, sub = (b['args'] + ['', ''])[:2]
        chips = ''.join(sp('display:inline-block;margin:0 6px 8px 0;padding:3px 9px;border:1px solid %s;background:#FDECEC;color:%s;font-size:13px;line-height:1.5;font-weight:bold;' % ('#E7A3A3', BAD), '✕ ' + r[0])
                        for r in b['rows'])
        return sec('margin:0 16px 22px;padding:12px 12px 4px;background:#FFFFFF;border:1px solid %s;' % LINE,
            '<p style="margin:0 0 10px;font-size:14px;line-height:1.5;color:%s;font-weight:bold;">%s</p>' % (INK, leaf(title))
            + '<p style="margin:0;line-height:1.5;">%s</p>' % chips
            + '<p style="margin:2px 0 6px;font-size:11px;line-height:1.6;color:%s;">%s</p>' % (MUTE, self.rich(sub)))

    def table(self, rows):
        head, body = rows[0], rows[1:]
        n = len(head)
        w0, wi = 32, (100 - 32) // (n - 1)
        th = ''.join('<td style="padding:7px 3px;background:%s;color:%s;font-size:11px;line-height:1.4;font-weight:bold;text-align:%s;width:%d%%;">%s</td>'
                     % (PALE, BLUE, 'left' if i == 0 else 'center', w0 if i == 0 else wi, leaf(c)) for i, c in enumerate(head))
        trs = []
        for row in body:
            tds = []
            for i, c in enumerate(row):
                hot = c.startswith('==')
                c = c.strip('=')
                inner = leaf(c) if not hot else sp('color:%s;font-weight:bold;' % BAD, c + ' ▲')
                tds.append('<td style="padding:8px 3px;border-bottom:1px dashed #D3D7DC;font-size:13px;line-height:1.4;text-align:%s;color:%s;%s%s">%s</td>'
                           % ('left' if i == 0 else 'center', INK if i == 0 else SUB, 'font-weight:bold;' if i == 0 else '',
                              'background:#FDF3F3;' if hot else '', inner))
            trs.append('<tr>%s</tr>' % ''.join(tds))
        return '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody><tr>%s</tr>%s</tbody></table>' % (th, ''.join(trs))

    def b_table(self, b):
        title, sub = (b['args'] + ['', ''])[:2]
        return sec('margin:0 16px 24px;background:#FFFFFF;border:1px solid %s;border-top:3px solid %s;padding:12px 12px 10px;' % (LINE, BLUE),
            '<table style="width:100%%;border-collapse:collapse;margin-bottom:8px;"><tbody><tr>'
            '<td style="padding:0;"><p style="margin:0;font-size:15px;line-height:1.5;color:%s;font-weight:bold;">%s</p></td>'
            '<td style="padding:0;text-align:right;width:84px;"><p style="margin:0;font-size:11px;line-height:1.5;color:%s;">%s</p></td>'
            '</tr></tbody></table>' % (INK, leaf(title), BAD, leaf('▲ 与他款不同'))
            + self.table(b['rows'])
            + '<p style="margin:8px 0 0;font-size:11px;line-height:1.6;color:%s;">%s</p>' % (MUTE, self.rich(sub)))

    def b_bars(self, b):
        title, unit = (b['args'] + ['', ''])[:2]
        mx = max(v for _, v in b['items'])
        rows = []
        for name, v in b['items']:
            w = max(4, int(round(v / mx * 100)))
            nm, _, subt = name.partition(' · ')
            rows.append('<tr><td style="width:40%%;padding:7px 6px 7px 0;font-size:12px;line-height:1.35;color:%s;vertical-align:middle;border-bottom:1px dashed #E1E4E8;">%s%s</td>'
                        '<td style="padding:7px 0;vertical-align:middle;border-bottom:1px dashed #E1E4E8;">%s</td>'
                        '<td style="width:46px;padding:7px 0 7px 6px;vertical-align:middle;border-bottom:1px dashed #E1E4E8;"><p style="margin:0;font-size:13px;line-height:1;color:%s;font-weight:bold;font-family:%s;text-align:right;">%s</p></td></tr>' % (
                            INK, leaf(nm), ('<br>' + sp('color:%s;font-size:11px;' % MUTE, subt)) if subt else '',
                            sec('background:#ECEEF1;height:8px;line-height:8px;font-size:0;',
                                blank('width:%d%%;height:8px;background:%s;line-height:8px;font-size:0;' % (w, BLUE if v == mx else '#9DB5D6'))),
                            BLUE if v == mx else INK, MONO, leaf('%g' % v)))
        return sec('margin:0 16px 24px;background:#FFFFFF;border:1px solid %s;border-top:3px solid %s;padding:12px;' % (LINE, BLUE),
            '<p style="margin:0 0 4px;font-size:15px;line-height:1.5;color:%s;font-weight:bold;">%s</p>' % (INK, leaf(title))
            + '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody>%s</tbody></table>' % ''.join(rows)
            + '<p style="margin:8px 0 0;font-size:11px;line-height:1.6;color:%s;">%s</p>' % (MUTE, self.rich(unit)))

    # 计算单：虚线框推演 + 两格结果
    def b_calc(self, b):
        cards = b['cards']
        tds = ''
        for i, (label, num, note) in enumerate(cards):
            hot = i == len(cards) - 1
            tds += ('<td style="width:50%%;padding:10px 8px;vertical-align:top;text-align:center;%s">'
                    '<p style="margin:0;font-size:11px;line-height:1.5;color:%s;">%s</p>'
                    '<p style="margin:2px 0;font-size:28px;line-height:1.25;font-weight:bold;font-family:%s;color:%s;">%s</p>'
                    '<p style="margin:0;font-size:11px;line-height:1.5;color:%s;">%s</p></td>' % (
                        '' if i == 0 else 'border-left:1px dashed #C5CAD1;', MUTE, leaf(label), MONO, BLUE if hot else INK, leaf(num), SUB, leaf(note)))
        return sec('margin:0 16px 22px;background:#FFFFFF;border:1px solid %s;padding:12px 14px;' % LINE,
            '<p style="margin:0 0 10px;font-size:13px;line-height:1.6;">%s</p>' % self.lab('计算单 · ' + b['args'][0])
            + ''.join(self.p(t, 'font-size:14px;margin-bottom:8px;') for t in b['lines'])
            + self.dash('10px 0 8px')
            + '<p style="margin:0 0 4px;font-size:12px;line-height:1.5;color:%s;font-weight:bold;text-align:center;">%s</p>' % (INK, leaf(b['cards_title']))
            + '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody><tr>%s</tr></tbody></table>' % tds)

    def numlist(self, items, labels):
        out = []
        for i, t in enumerate(items):
            out.append('<tr><td style="width:44px;vertical-align:top;padding:10px 0;border-bottom:1px dashed #D3D7DC;">'
                       '<p style="margin:0;font-size:12px;line-height:22px;">%s</p></td>'
                       '<td style="vertical-align:top;padding:10px 0 10px 4px;border-bottom:1px dashed #D3D7DC;">%s</td></tr>' % (
                           sp('display:inline-block;width:34px;height:22px;line-height:22px;border:1px solid %s;color:%s;text-align:center;font-weight:bold;font-family:%s;letter-spacing:0;' % (BLUE, BLUE, MONO), '%02d' % (i + 1)),
                           self.p(t, 'margin:0;font-size:14px;')))
        return '<table style="width:100%%;border-collapse:collapse;"><tbody>%s</tbody></table>' % ''.join(out)

    def b_steps(self, b):
        return sec('margin:0 16px 22px;padding:10px 14px 4px;background:#FFFFFF;border:1px solid %s;' % LINE,
            '<p style="margin:0 0 2px;font-size:13px;line-height:1.6;">%s</p>' % self.lab('复查清单')
            + self.numlist(b['items'], None))

    def b_quote(self, b):
        return sec('margin:8px 16px 26px;padding:14px 4px;border-top:1px solid %s;border-bottom:1px solid %s;' % (BLUE, BLUE),
            ''.join('<p style="margin:0;font-size:17px;line-height:1.7;color:%s;font-weight:bold;text-align:center;">%s</p>' % (INK, self.rich(t)) for t in b['paras']))

    # 诊断意见：人群 → 建议 对照，再接原文
    def b_rx(self, b):
        title = b['args'][0] if b['args'] else '诊断意见'
        trs = ''.join('<tr><td style="width:46%%;padding:9px 8px 9px 0;border-bottom:1px dashed #D3D7DC;vertical-align:top;"><p style="margin:0;font-size:13px;line-height:1.5;color:%s;">%s</p></td>'
                      '<td style="padding:9px 0;border-bottom:1px dashed #D3D7DC;vertical-align:top;"><p style="margin:0;font-size:14px;line-height:1.5;color:%s;font-weight:bold;">%s</p></td></tr>' % (
                          SUB, leaf(r[0]), BLUE if i == 0 else INK, leaf('→ ' + r[1])) for i, r in enumerate(b['rows']))
        return sec('margin:0 16px 22px;background:#FFFFFF;border:2px solid %s;' % BLUE,
            sec('padding:8px 14px;background:%s;' % BLUE,
                '<p style="margin:0;font-size:15px;line-height:1.5;color:#FFFFFF;font-weight:bold;letter-spacing:2px;">%s</p>' % leaf('Rx　' + title))
            + sec('padding:6px 14px 4px;', '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody>%s</tbody></table>' % trs)
            + sec('padding:10px 14px 0;', ''.join(self.p(t, 'font-size:14px;margin-bottom:12px;') for t in b['paras'])))

    def b_verdict(self, b):
        return sec('margin:0 16px 22px;background:#FFFFFF;border:2px solid %s;' % BLUE,
            sec('padding:8px 14px;background:%s;' % BLUE,
                '<p style="margin:0;font-size:15px;line-height:1.5;color:#FFFFFF;font-weight:bold;letter-spacing:2px;">%s</p>' % leaf('体检结论'))
            + sec('padding:14px;', ''.join('<p style="margin:0;font-size:18px;line-height:1.6;color:%s;font-weight:bold;">%s</p>' % (INK, self.title_html(t)) for t in b['paras'])
                  + '<p style="margin:10px 0 0;font-size:11px;line-height:1.5;color:%s;text-align:right;">%s</p>' % (MUTE, leaf('检验：喵叔 · 喵叔说保'))))

    def b_end(self, b):
        it = b['items']
        return sec('margin:30px 16px 16px;padding:16px 4px 4px;border-top:3px double %s;text-align:center;' % BLUE,
            '<p style="margin:0 0 10px;font-size:14px;line-height:1.8;color:%s;">%s</p>' % (SUB, self.rich(it[0]))
            + '<p style="margin:0 0 12px;font-size:15px;line-height:1.8;color:%s;font-weight:bold;">%s</p>' % (INK, self.rich(it[1]))
            + '<p style="margin:0;font-size:13px;line-height:1.6;">%s</p>' % sp(
                'display:inline-block;padding:4px 14px;border:1px solid %s;color:%s;font-weight:bold;' % (BLUE, BLUE), it[2]))

    def b_disclaimer(self, b):
        return sec('margin:16px 16px 10px;padding:10px 0 0;border-top:1px dashed #C5CAD1;',
            '<p style="margin:0 0 4px;font-size:11px;line-height:1.6;color:%s;font-weight:bold;">%s</p>' % (MUTE, leaf('报告说明'))
            + ''.join('<p style="margin:0;font-size:11px;line-height:1.7;color:%s;text-align:justify;">%s</p>' % (MUTE, self.rich(t)) for t in b['paras']))
