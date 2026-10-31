"""主题③　深蓝鎏金 · 数据测算
深海蓝 #0B1F3A + 鎏金 #C9A45C + 钴蓝 #1D4E89；白底正文，数据/算账/结论模块用深蓝底金字。
适合养老金、年金、分红、医保档位等算账文章。静态化自视频 T07 数据仪表盘 / T06 黑板讲解 / T74 工程蓝图 / 深蓝鎏金。
"""
from base import sp, sec, blank, leaf, SANS, SERIF
import miaolan

NAVY, GOLD, COBALT, MONO = '#0B1F3A', '#C9A45C', '#1D4E89', "'DIN Alternate','Roboto Mono','SF Mono',Menlo,'PingFang SC','Microsoft YaHei',sans-serif"


class T(miaolan.T):
    id = 'shenlan'
    name = '深蓝鎏金 · 数据测算'
    P = dict(bg='#FFFFFF', text='#323A48', title=NAVY, muted='#8A919C', line='#E4E7EC', primary=COBALT,
             plight='#F3F5F8', hl='#F3E9D2', ul=GOLD, gold=GOLD, goldlight='#FAF5EA',
             red='#B4442E', redlight='#FBEFEB')
    REMAP = {'#051A4C': NAVY, '#0288D1': COBALT, '#F2A900': GOLD, '#EEF7FD': '#F3F5F8',
             '#D6E9F5': '#DCE2EA', '#F7FAFD': '#F8F9FB', '#E3EAF2': '#E4E7EC', '#55606F': '#4C5564',
             '#EEF2F6': '#EDEFF3', '#7FC6EE': '#8FA9C9', '#F1F4F8': '#F2F4F7', '#DDF0FB': '#E7DAB9',
             '#DCE6F0': '#DCE2EA', '#F6F8FA': '#F6F7F9', '#F5F9FC': '#F8F9FB', '#FFF7E0': '#FAF5EA',
             '#8A94A3': '#8A919C', '#3A4556': '#323A48', '#FFD666': '#E2C58A'}

    def mark_style(self, kind):
        return {
            'anchor': 'color:%s;font-weight:bold;' % COBALT,
            'hl': 'background:#F3E9D2;',
            'ul': 'border-bottom:2px solid %s;font-weight:600;padding-bottom:1px;color:%s;' % (GOLD, NAVY),
        }[kind]

    def header(self):
        m = self.meta
        stats = [('4', '款产品'), ('730/1095', '天间隔'), ('50万', '保额算例')]
        tds = ''.join('<td style="width:33%%;padding:10px 4px;text-align:center;border-left:%s;vertical-align:top;">'
                      '<p style="margin:0;font-size:18px;line-height:1.3;color:%s;font-weight:bold;font-family:%s;">%s</p>'
                      '<p style="margin:2px 0 0;font-size:11px;line-height:1.4;color:#93A3BC;">%s</p></td>'
                      % ('0' if i == 0 else '1px solid #2A4066', GOLD, MONO, leaf(a), leaf(c)) for i, (a, c) in enumerate(stats))
        return sec('background:%s;padding:24px 18px 18px;margin:0 0 26px;' % NAVY,
            '<p style="margin:0 0 14px;font-size:11px;line-height:1.6;color:%s;letter-spacing:3px;">%s</p>' % (GOLD, leaf('喵叔说保 · 算清楚再买'))
            + '<p style="margin:0 0 4px;font-size:13px;line-height:1.6;color:#93A3BC;">%s</p>' % leaf(m.get('kicker', ''))
            + '<p style="margin:0 0 14px;font-size:22px;line-height:1.45;color:#FFFFFF;font-weight:bold;">%s</p>' % self.title_html(m['title'])
            + blank('width:100%;height:0;border-top:1px solid #C9A45C;margin:0 0 4px;line-height:0;font-size:0;')
            + '<table style="width:100%%;border-collapse:collapse;"><tbody><tr>%s</tr></tbody></table>' % tds
            + '<p style="margin:10px 0 0;font-size:11px;line-height:1.6;color:#6F819E;">%s</p>' % leaf('喵叔　' + m.get('date', '') + '　｜　数据均取自正文'))

    def b_h2(self, b):
        self.chap += 1
        return sec('margin:36px 16px 16px;',
            '<p style="margin:0 0 4px;font-size:12px;line-height:1.4;color:%s;font-weight:bold;letter-spacing:3px;font-family:%s;">%s</p>' % (GOLD, MONO, leaf('PART %02d' % self.chap))
            + '<p style="margin:0 0 8px;font-size:19px;line-height:1.5;color:%s;font-weight:bold;">%s</p>' % (NAVY, self.rich(b['text']))
            + blank('width:24px;height:3px;background:%s;line-height:3px;font-size:0;' % GOLD))

    def b_lead(self, b):
        return sec('margin:0 16px 24px;padding:14px 16px;background:#F3F5F8;border-left:3px solid %s;' % GOLD,
            ''.join(self.p(t, 'margin:0;font-size:16px;color:%s;font-weight:500;' % NAVY) for t in b['paras']))

    # 条款规格卡：深蓝细顶条 + 编号 + 金色人话
    def b_clause(self, b):
        name, ins, lead = (b['args'] + ['', '', ''])[:3]
        self.cl = getattr(self, 'cl', 0) + 1
        return sec('margin:0 16px 16px;border-top:3px solid %s;background:#F8F9FB;' % NAVY,
            '<table style="width:100%%;border-collapse:collapse;"><tbody><tr>'
            '<td style="padding:10px 12px 2px;"><p style="margin:0;font-size:15px;line-height:1.5;color:%s;font-weight:bold;">%s</p></td>'
            '<td style="padding:10px 12px 2px;text-align:right;width:60px;"><p style="margin:0;font-size:12px;line-height:1.5;color:%s;font-weight:bold;font-family:%s;">%s</p></td>'
            '</tr></tbody></table>' % (NAVY, leaf(name), GOLD, MONO, leaf('原文 %02d' % self.cl))
            + '<p style="margin:0;padding:0 12px 8px;font-size:12px;line-height:1.6;color:#8A919C;">%s</p>' % self.rich(ins + '。' + lead + '：')
            + '<p style="margin:0;padding:0 12px 10px;font-size:14px;line-height:1.8;color:#4C5564;text-align:justify;">%s</p>' % self.rich(b['text'])
            + '<p style="margin:0;padding:9px 12px;background:%s;font-size:14px;line-height:1.6;color:#FFFFFF;font-weight:bold;">%s%s</p>' % (
                NAVY, sp('color:%s;margin-right:6px;' % GOLD, '人话 ▸'), leaf(b['note'])))

    def b_quote(self, b):
        return sec('margin:8px 16px 26px;padding:4px;background:%s;' % NAVY,
            sec('border:1px solid %s;padding:14px 14px;text-align:center;' % GOLD,
                ''.join('<p style="margin:0;font-size:16px;line-height:1.75;color:#F4E7C8;font-weight:bold;letter-spacing:1px;">%s</p>' % self.rich(t) for t in b['paras'])))

    def table(self, rows):
        head, body = rows[0], rows[1:]
        n = len(head)
        w0, wi = 32, (100 - 32) // (n - 1)
        th = ''.join('<td style="padding:8px 3px;background:%s;color:%s;font-size:12px;line-height:1.4;font-weight:bold;text-align:%s;width:%d%%;">%s</td>'
                     % (NAVY, GOLD, 'left' if i == 0 else 'center', w0 if i == 0 else wi, leaf(c)) for i, c in enumerate(head))
        trs = []
        for r, row in enumerate(body):
            tds = []
            for i, c in enumerate(row):
                hot = c.startswith('==')
                c = c.strip('=')
                inner = leaf(c) if not hot else sp('color:%s;font-weight:bold;border-bottom:2px solid %s;' % (NAVY, GOLD), c)
                tds.append('<td style="padding:8px 3px;border-bottom:1px solid #E4E7EC;background:%s;font-size:13px;line-height:1.4;text-align:%s;color:%s;%s">%s</td>'
                           % ('#FAF5EA' if hot else ('#FFFFFF' if r % 2 == 0 else '#F8F9FB'), 'left' if i == 0 else 'center',
                              NAVY if i == 0 else '#4C5564', 'font-weight:bold;' if i == 0 else '', inner))
            trs.append('<tr>%s</tr>' % ''.join(tds))
        return '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody><tr>%s</tr>%s</tbody></table>' % (th, ''.join(trs))

    # 深色数据面板：金色条
    def b_bars(self, b):
        title, unit = (b['args'] + ['', ''])[:2]
        mx = max(v for _, v in b['items'])
        rows = []
        for name, v in b['items']:
            nm, _, sub = name.partition(' · ')
            w = int(round(v / mx * 100))
            rows.append('<tr><td style="width:40%%;padding:7px 6px 7px 0;font-size:13px;line-height:1.35;color:#FFFFFF;">%s%s</td>'
                        '<td style="padding:7px 0;vertical-align:middle;">%s</td>'
                        '<td style="width:17%%;padding:7px 0 7px 6px;font-size:15px;line-height:1.3;color:%s;font-weight:bold;text-align:right;font-family:%s;">%s</td></tr>' % (
                            leaf(nm), ('<br>' + sp('color:#7F92AE;font-size:11px;', sub)) if sub else '',
                            sec('background:#1C3354;height:10px;line-height:10px;font-size:0;',
                                sec('width:%d%%;height:10px;background:%s;line-height:10px;font-size:0;' % (w, GOLD if v == mx else '#5E7598'), '<span leaf=""><br></span>')),
                            GOLD if v == mx else '#C9D3E3', MONO, leaf('%d' % v)))
        return sec('margin:0 16px 26px;padding:16px 14px 12px;background:%s;' % NAVY,
            '<p style="margin:0 0 4px;font-size:11px;line-height:1.5;color:%s;letter-spacing:2px;">%s</p>' % (GOLD, leaf('DATA'))
            + '<p style="margin:0 0 8px;font-size:16px;line-height:1.5;color:#FFFFFF;font-weight:bold;">%s</p>' % leaf(title)
            + '<table style="width:100%%;border-collapse:collapse;"><tbody>%s</tbody></table>' % ''.join(rows)
            + '<p style="margin:8px 0 0;font-size:11px;line-height:1.6;color:#7F92AE;">%s</p>' % self.rich(unit))

    # 黑板式算账：深蓝板 + 金色结果
    def b_calc(self, b):
        cards = b['cards']
        tds = []
        for i, (label, num, note) in enumerate(cards):
            hot = i == len(cards) - 1
            tds.append('<td style="width:50%%;padding:12px 6px;text-align:center;vertical-align:top;border-left:%s;">'
                       '<p style="margin:0;font-size:12px;line-height:1.5;color:#93A3BC;">%s</p>'
                       '<p style="margin:4px 0;font-size:32px;line-height:1.2;color:%s;font-weight:bold;font-family:%s;">%s</p>'
                       '<p style="margin:0;font-size:11px;line-height:1.5;color:%s;">%s</p></td>'
                       % ('0' if i == 0 else '1px solid #2A4066', leaf(label), GOLD if hot else '#FFFFFF', MONO, leaf(num),
                          '#E2C58A' if hot else '#7F92AE', leaf(note)))
        return sec('margin:0 16px 22px;background:%s;padding:16px 14px 12px;' % NAVY,
            '<p style="margin:0 0 10px;font-size:12px;line-height:1.5;">%s</p>' % sp(
                'display:inline-block;padding:1px 8px;border:1px solid %s;color:%s;font-weight:bold;letter-spacing:2px;' % (GOLD, GOLD), b['args'][0])
            + ''.join('<p style="margin:0 0 8px;font-size:14px;line-height:1.8;color:#DCE3EE;text-align:justify;">%s</p>' % self.rich(t) for t in b['lines'])
            + sec('margin-top:10px;border-top:1px dashed #3A5279;padding-top:10px;',
                '<p style="margin:0 0 4px;font-size:12px;line-height:1.5;color:%s;text-align:center;font-weight:bold;">%s</p>' % (GOLD, leaf(b['cards_title']))
                + '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody><tr>%s</tr></tbody></table>' % ''.join(tds)))

    def b_verdict(self, b):
        return sec('margin:0 16px 22px;padding:4px;background:%s;' % NAVY,
            sec('border:1px solid %s;padding:16px 14px;' % GOLD,
                '<p style="margin:0 0 6px;font-size:11px;line-height:1.5;color:%s;letter-spacing:3px;">%s</p>' % (GOLD, leaf('判断线 · CONCLUSION'))
                + ''.join('<p style="margin:0;font-size:18px;line-height:1.6;color:#FFFFFF;font-weight:bold;">%s</p>' % self.title_html(t, color='#E2C58A') for t in b['paras'])))

    def b_end(self, b):
        it = b['items']
        return sec('margin:30px 16px 16px;padding:18px 16px 16px;background:#F3F5F8;text-align:center;border-top:3px solid %s;' % GOLD,
            '<p style="margin:0 0 10px;font-size:14px;line-height:1.8;color:#4C5564;">%s</p>' % self.rich(it[0])
            + '<p style="margin:0 0 12px;font-size:15px;line-height:1.8;color:%s;font-weight:bold;">%s</p>' % (NAVY, self.rich(it[1]))
            + '<p style="margin:0;font-size:13px;line-height:1.6;">%s</p>' % sp(
                'display:inline-block;padding:4px 14px;background:%s;color:%s;font-weight:bold;' % (NAVY, GOLD), it[2]))
