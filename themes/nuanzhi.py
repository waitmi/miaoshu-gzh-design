"""主题②　暖纸编辑 · 测评风
米黄纸底 + 墨色 + 砖红锚点 + 荧光黄关键词；标题用宋体，杂志式大章节号。
静态化自视频 T67 暖纸编辑风 / T01 荧光笔笔记 / T04 对比擂台 / T03 打分卡 / T05 案卷档案。
"""
from base import sp, sec, blank, leaf, SANS, SERIF
import miaolan

INK, RED, OCHRE, PAPER = '#2A2522', '#B5452F', '#D49A2A', '#F6F0E4'


class T(miaolan.T):
    id = 'nuanzhi'
    name = '暖纸编辑 · 测评风'
    P = dict(bg=PAPER, text='#3D3731', title=INK, muted='#9A8F80', line='#E2D6C0', primary=RED,
             plight='#FBF4E6', hl='#FFE7A0', ul='#FFE08A', gold=OCHRE, goldlight='#FFF4D6',
             red=RED, redlight='#FBE9E4')
    font = SANS
    REMAP = {'#051A4C': INK, '#0288D1': RED, '#F2A900': OCHRE, '#EEF7FD': '#FBF4E6',
             '#D6E9F5': '#E4D5BA', '#F7FAFD': '#FFFCF5', '#E3EAF2': '#E6DAC6', '#55606F': '#5A5148',
             '#EEF2F6': '#ECE2D0', '#7FC6EE': '#D9A08F', '#F1F4F8': '#F1E8D8', '#DDF0FB': '#FBE3DA',
             '#DCE6F0': '#E4D5BA', '#F6F8FA': '#F2EADB', '#F5F9FC': '#FBF6EC', '#FFF7E0': '#FFF4D6',
             '#8A94A3': '#9A8F80', '#3A4556': '#3D3731', '#FFD666': '#FFE08A'}

    def mark_style(self, kind):
        return {
            'anchor': 'color:%s;font-weight:bold;' % RED,
            'hl': 'background:#FFE7A0;',
            # 荧光笔：纯色浅黄底，不用渐变
            'ul': 'background:#FFE9A6;font-weight:600;color:%s;' % INK,
        }[kind]

    def header(self):
        m = self.meta
        return sec('padding:26px 20px 6px;margin:0 0 22px;',
            '<p style="margin:0 0 4px;font-size:12px;line-height:1.6;color:#9A8F80;letter-spacing:3px;">%s</p>' % leaf('喵叔说保 · 每日排坑')
            + blank('height:0;border-top:2px solid %s;margin:0 0 3px;line-height:0;font-size:0;' % INK)
            + blank('height:0;border-top:1px solid %s;margin:0 0 16px;line-height:0;font-size:0;' % INK)
            + '<p style="margin:0 0 2px;font-size:46px;line-height:1.1;color:#E3CDBF;font-family:%s;font-weight:bold;letter-spacing:2px;">%s</p>' % (SERIF, leaf('No.' + m.get('date', '')[-5:].replace('.', '')))
            + '<p style="margin:0 0 10px;font-size:13px;line-height:1.6;color:%s;font-weight:bold;letter-spacing:2px;">%s</p>' % (RED, leaf(m.get('kicker', '')))
            + '<p style="margin:0 0 14px;font-size:24px;line-height:1.45;color:%s;font-family:%s;font-weight:bold;">%s</p>' % (INK, SERIF, self.title_html(m['title']))
            + '<p style="margin:0;padding:8px 0 0;border-top:1px solid #D8C9AE;font-size:12px;line-height:1.6;color:#9A8F80;">%s</p>' % leaf('文｜喵叔　　' + m.get('date', '')))

    def b_h2(self, b):
        self.chap += 1
        return sec('margin:38px 16px 18px;padding-bottom:10px;border-bottom:1px solid #D8C9AE;',
            '<table style="width:100%%;border-collapse:collapse;"><tbody><tr>'
            '<td style="width:58px;padding:0;vertical-align:bottom;"><p style="margin:0;font-size:42px;line-height:1;color:%s;font-family:%s;font-weight:bold;">%s</p></td>'
            '<td style="padding:0 0 2px 4px;vertical-align:bottom;"><p style="margin:0;font-size:20px;line-height:1.4;color:%s;font-family:%s;font-weight:bold;">%s</p></td>'
            '</tr></tbody></table>' % (RED, SERIF, leaf('%02d' % self.chap), INK, SERIF, self.rich(b['text'], guard=False)))

    # 案卷档案袋
    def b_case(self, b):
        title, label = (b['args'] + ['', ''])[:2]
        return sec('margin:0 16px 24px;',
            '<p style="margin:0;font-size:12px;line-height:1.6;">%s</p>' % sp(
                'display:inline-block;padding:4px 14px 2px;background:#D8BF8F;color:%s;font-weight:bold;letter-spacing:2px;border-radius:6px 6px 0 0;' % INK,
                '案卷 · ' + label)
            + sec('background:#E9D9B6;padding:12px;border-radius:0 8px 8px 8px;',
                sec('background:#FFFCF5;padding:14px 14px 4px;border-radius:4px;',
                    '<p style="margin:0 0 10px;padding-bottom:8px;border-bottom:1px dashed #D8C9AE;font-size:15px;line-height:1.5;color:%s;font-family:%s;font-weight:bold;">%s</p>' % (INK, SERIF, leaf(title))
                    + ''.join(self.p(t, 'font-size:14px;margin-bottom:10px;') for t in b['paras'])
                    + '<p style="margin:0 0 10px;text-align:right;font-size:13px;line-height:1.4;">%s</p>' % sp(
                        'display:inline-block;padding:3px 10px;border:2px solid %s;border-radius:4px;color:%s;font-weight:bold;letter-spacing:3px;' % (RED, RED), '待核条款'))))

    def b_lead(self, b):
        return sec('margin:0 16px 26px;padding:4px 0 4px 14px;border-left:3px solid %s;' % RED,
            ''.join(self.p(t, 'margin:0;font-size:17px;line-height:1.75;color:%s;font-family:%s;font-weight:bold;' % (INK, SERIF)) for t in b['paras']))

    # 荧光笔笔记卡
    def b_clause(self, b):
        name, ins, lead = (b['args'] + ['', '', ''])[:3]
        return sec('margin:0 16px 16px;background:#FFFDF8;border:1px solid #E6DAC6;border-radius:6px;padding:14px 14px 12px;box-shadow:0 2px 0 #E6DAC6;',
            '<p style="margin:0;font-size:16px;line-height:1.5;color:%s;font-family:%s;font-weight:bold;">%s</p>' % (INK, SERIF, sp('background:#FFE9A6;padding:0 3px;', name))
            + '<p style="margin:2px 0 10px;font-size:12px;line-height:1.6;color:#9A8F80;">%s</p>' % self.rich(ins + '。' + lead + '：')
            + '<p style="margin:0 0 10px;font-size:14px;line-height:1.85;color:#5A5148;font-family:%s;text-align:justify;">%s%s%s</p>' % (
                SERIF, sp('color:%s;font-weight:bold;' % RED, '「'), self.rich(b['text'], guard=False), sp('color:%s;font-weight:bold;' % RED, '」'))
            + '<p style="margin:0;padding-top:8px;border-top:1px dashed #E2D3B8;font-size:14px;line-height:1.6;color:%s;font-weight:bold;">%s%s</p>' % (
                RED, sp('margin-right:6px;', '✎'), leaf(b['note'])))

    def b_quote(self, b):
        return sec('margin:10px 28px 28px;padding:12px 0;border-top:1px solid %s;border-bottom:1px solid %s;text-align:center;' % (INK, INK),
            ''.join('<p style="margin:0;font-size:17px;line-height:1.8;color:%s;font-family:%s;font-weight:bold;">%s</p>' % (INK, SERIF, self.rich(t)) for t in b['paras']))

    # 对比擂台：左列维度，产品成列，差异项砖红圆章
    def table(self, rows):
        head, body = rows[0], rows[1:]
        n = len(head)
        w0, wi = 32, (100 - 32) // (n - 1)
        th = ''.join('<td style="padding:8px 3px;border-bottom:2px solid %s;color:%s;font-size:12px;line-height:1.4;font-weight:bold;text-align:%s;width:%d%%;">%s</td>'
                     % (INK, INK, 'left' if i == 0 else 'center', w0 if i == 0 else wi, leaf(c)) for i, c in enumerate(head))
        trs = []
        for row in body:
            tds = []
            for i, c in enumerate(row):
                hot = c.startswith('==')
                c = c.strip('=')
                inner = leaf(c) if not hot else sp('display:inline-block;padding:0 7px;border-radius:10px;background:%s;color:#FFFFFF;font-weight:bold;' % RED, c)
                tds.append('<td style="padding:9px 3px;border-bottom:1px solid #E2D6C0;font-size:13px;line-height:1.4;text-align:%s;color:%s;%s">%s</td>'
                           % ('left' if i == 0 else 'center', INK if i == 0 else '#5A5148', 'font-weight:bold;' if i == 0 else '', inner))
            trs.append('<tr>%s</tr>' % ''.join(tds))
        return '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;background:#FFFDF8;"><tbody><tr>%s</tr>%s</tbody></table>' % (th, ''.join(trs))

    def b_table(self, b):
        title, sub = (b['args'] + ['', ''])[:2]
        return sec('margin:0 16px 26px;padding:14px 12px 10px;background:#FFFDF8;border:1px solid #E6DAC6;border-radius:6px;',
            '<p style="margin:0 0 8px;font-size:12px;line-height:1.6;">%s</p>' % sp(
                'display:inline-block;padding:0 8px;background:%s;color:#FFFFFF;font-weight:bold;letter-spacing:2px;' % INK, '对比擂台')
            + '<p style="margin:0 0 8px;font-size:16px;line-height:1.5;color:%s;font-family:%s;font-weight:bold;">%s</p>' % (INK, SERIF, leaf(title))
            + self.table(b['rows'])
            + '<p style="margin:8px 0 0;font-size:12px;line-height:1.6;color:#9A8F80;">%s</p>' % self.rich(sub))

    # 打分进度条：细条 + 数值在右
    def b_bars(self, b):
        title, unit = (b['args'] + ['', ''])[:2]
        mx = max(v for _, v in b['items'])
        rows = []
        for name, v in b['items']:
            nm, _, sub = name.partition(' · ')
            w = int(round(v / mx * 100))
            rows.append('<tr><td style="width:40%%;padding:7px 6px 7px 0;font-size:13px;line-height:1.35;color:%s;font-weight:bold;">%s%s</td>'
                        '<td style="padding:7px 0;vertical-align:middle;">%s</td>'
                        '<td style="width:15%%;padding:7px 0 7px 6px;font-size:14px;line-height:1.3;color:%s;font-weight:bold;text-align:right;">%s</td></tr>' % (
                            INK, leaf(nm), ('<br>' + sp('color:#9A8F80;font-size:11px;font-weight:normal;', sub)) if sub else '',
                            sec('background:#ECE2D0;height:8px;border-radius:4px;line-height:8px;font-size:0;',
                                sec('width:%d%%;height:8px;background:%s;border-radius:4px;line-height:8px;font-size:0;' % (w, RED if v == mx else OCHRE), '<span leaf=""><br></span>')),
                            RED if v == mx else INK, leaf('%d' % v)))
        return sec('margin:0 16px 26px;padding:14px 12px;background:#FFFDF8;border:1px solid #E6DAC6;border-radius:6px;',
            '<p style="margin:0 0 6px;font-size:16px;line-height:1.5;color:%s;font-family:%s;font-weight:bold;">%s</p>' % (INK, SERIF, leaf(title))
            + '<table style="width:100%%;border-collapse:collapse;"><tbody>%s</tbody></table>' % ''.join(rows)
            + '<p style="margin:6px 0 0;font-size:12px;line-height:1.6;color:#9A8F80;">%s</p>' % self.rich(unit))

    def b_verdict(self, b):
        return sec('margin:0 16px 24px;padding:18px 16px;background:#FFFDF8;border:2px solid %s;border-radius:4px;' % RED,
            '<p style="margin:0 0 6px;font-size:13px;line-height:1.4;">%s</p>' % sp(
                'display:inline-block;padding:2px 10px;border:2px solid %s;border-radius:4px;color:%s;font-weight:bold;letter-spacing:4px;' % (RED, RED), '判断线')
            + ''.join('<p style="margin:0;font-size:19px;line-height:1.6;color:%s;font-family:%s;font-weight:bold;">%s</p>' % (INK, SERIF, self.title_html(t)) for t in b['paras']))

    def b_end(self, b):
        it = b['items']
        return sec('margin:32px 16px 16px;padding:18px 16px 16px;border-top:2px solid %s;border-bottom:1px solid %s;text-align:center;' % (INK, INK),
            '<p style="margin:0 0 10px;font-size:14px;line-height:1.8;color:#5A5148;">%s</p>' % self.rich(it[0])
            + '<p style="margin:0 0 12px;font-size:16px;line-height:1.8;color:%s;font-family:%s;font-weight:bold;">%s</p>' % (INK, SERIF, self.rich(it[1]))
            + '<p style="margin:0;font-size:13px;line-height:1.6;">%s</p>' % sp(
                'display:inline-block;padding:4px 14px;background:%s;color:#FFFFFF;font-weight:bold;letter-spacing:1px;' % RED, it[2]))
