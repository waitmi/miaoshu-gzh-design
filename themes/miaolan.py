"""主题①　喵叔蓝 · 科普卡片（日常主力）
IP 蓝 #0288D1 + 海军蓝 #051A4C，金色只做点睛；白底、灰阶承重。
"""
from base import Theme, sp, sec, blank, leaf, SANS

NAVY, BLUE, GOLD = '#051A4C', '#0288D1', '#F2A900'


class T(Theme):
    id = 'miaolan'
    name = '喵叔蓝 · 科普卡片'
    P = dict(bg='#FFFFFF', text='#3A4556', title=NAVY, muted='#8A94A3', line='#E3EAF2',
             primary=BLUE, plight='#EEF7FD', hl='#DDF0FB', ul='#8CCDF0', gold=GOLD,
             goldlight='#FFF7E0', red='#D9472B', redlight='#FFF3EF')
    font = SANS

    def tagx(self, text, bg, fg, size=12):
        return sp('display:inline-block;padding:0 7px;margin-right:6px;border-radius:3px;background:%s;'
                  'color:%s;font-size:%dpx;font-weight:bold;letter-spacing:1px;' % (bg, fg, size), text)

    # 标题区：海军蓝头图卡，呼应封面
    def header(self):
        m, P = self.meta, self.P
        return sec('background:%s;padding:26px 20px 22px;margin:0 0 26px;' % NAVY,
            '<p style="margin:0 0 14px;font-size:12px;line-height:1.6;">%s%s</p>' % (
                sp('display:inline-block;padding:2px 10px;border:1px solid #4F7BB0;border-radius:4px;'
                   'background:#13366A;color:#FFFFFF;font-weight:bold;letter-spacing:2px;', '喵叔说保'),
                sp('color:#9FB4D3;letter-spacing:1px;margin-left:8px;', '防坑｜买对｜赔好'))
            + '<p style="margin:0 0 6px;font-size:13px;line-height:1.6;color:#7FC6EE;letter-spacing:2px;">%s</p>' % leaf(m.get('kicker', ''))
            + '<p style="margin:0 0 14px;font-size:22px;line-height:1.45;color:#FFFFFF;font-weight:bold;letter-spacing:1px;">%s</p>' % self.title_html(m['title'])
            + blank('width:36px;height:3px;background:%s;margin:0 0 12px;line-height:3px;font-size:0;' % GOLD)
            + '<p style="margin:0;font-size:12px;line-height:1.6;color:#8FA3BF;">%s</p>' % leaf(m.get('date', '') + ' · 喵叔'))

    def b_h2(self, b):
        self.chap += 1
        return sec('margin:34px 16px 16px;',
            '<p style="margin:0 0 6px;font-size:13px;line-height:1.4;">%s</p>' % sp(
                'display:inline-block;padding:1px 9px;border-radius:4px;background:%s;color:#FFFFFF;font-weight:bold;letter-spacing:1px;' % BLUE,
                '%02d' % self.chap)
            + '<p style="margin:0;padding:0 0 10px;font-size:19px;line-height:1.5;color:%s;font-weight:bold;'
              'border-bottom:1px solid %s;">%s</p>' % (NAVY, self.P['line'], leaf(b['text'])))

    def b_case(self, b):
        title, label = (b['args'] + ['', ''])[:2]
        return sec('margin:0 16px 22px;border:1px solid #DCE6F0;border-radius:10px;background:#F7FAFD;padding:14px 14px 4px;',
            '<p style="margin:0 0 10px;font-size:13px;line-height:1.6;">%s%s</p>' % (
                self.tagx(label, BLUE, '#FFFFFF', 12), sp('color:%s;font-weight:bold;' % NAVY, title))
            + ''.join(self.p(t, 'font-size:14px;margin-bottom:10px;') for t in b['paras']))

    def b_lead(self, b):
        return sec('margin:0 16px 24px;padding:14px 16px;background:%s;border-radius:8px;border-left:4px solid %s;' % (self.P['plight'], BLUE),
            ''.join(self.p(t, 'margin:0;font-size:16px;color:%s;font-weight:500;' % NAVY) for t in b['paras']))

    def b_clause(self, b):
        name, ins, lead = (b['args'] + ['', '', ''])[:3]
        return sec('margin:0 16px 14px;border:1px solid #D6E9F5;border-radius:8px;overflow:hidden;',
            sec('background:%s;padding:9px 14px;' % self.P['plight'],
                '<p style="margin:0;font-size:15px;line-height:1.6;color:%s;font-weight:bold;">%s</p>' % (NAVY, leaf(name))
                + '<p style="margin:0;font-size:12px;line-height:1.6;color:%s;">%s</p>' % (self.P['muted'], self.rich(ins + '。' + lead + '：')))
            + sec('padding:10px 14px 2px;',
                '<p style="margin:0 0 10px;font-size:14px;line-height:1.8;color:#55606F;text-align:justify;">%s%s</p>' % (
                    self.tagx('原文', '#E3EAF2', '#55606F', 12), self.rich(b['text'])))
            + sec('padding:9px 14px;border-top:1px dashed #D6E9F5;',
                '<p style="margin:0;font-size:14px;line-height:1.7;color:%s;font-weight:bold;">%s%s</p>' % (
                    NAVY, self.tagx('人话', GOLD, NAVY, 12), leaf(b['note']))))

    def b_key(self, b):
        return sec('margin:4px 16px 24px;padding:12px 14px;border:1px solid %s;border-radius:8px;' % BLUE,
            ''.join(self.p(t, 'margin:0;color:%s;font-weight:bold;' % NAVY) for t in b['paras']))

    def b_example(self, b):
        return sec('margin:0 16px 20px;padding:12px 14px 2px;background:#F6F8FA;border-radius:8px;',
            '<p style="margin:0 0 8px;font-size:13px;line-height:1.6;">%s%s</p>' % (
                self.tagx('举例', NAVY, '#FFFFFF'), sp('color:%s;font-weight:bold;' % NAVY, b['args'][0] if b['args'] else ''))
            + ''.join(self.p(t, 'font-size:14px;margin-bottom:10px;') for t in b['paras']))

    def b_term(self, b):
        return sec('margin:0 16px 22px;padding:12px 14px 2px;background:%s;border-radius:8px;' % self.P['plight'],
            '<p style="margin:0 0 8px;font-size:13px;line-height:1.6;">%s%s</p>' % (
                self.tagx('名词', BLUE, '#FFFFFF'), sp('color:%s;font-weight:bold;' % NAVY, b['args'][0]))
            + ''.join(self.p(t, 'font-size:14px;margin-bottom:10px;') for t in b['paras']))

    def b_quote(self, b):
        return sec('margin:8px 16px 26px;padding:16px 18px;background:%s;border-radius:8px;text-align:center;' % NAVY,
            ''.join('<p style="margin:0;font-size:16px;line-height:1.75;color:#FFFFFF;font-weight:bold;letter-spacing:1px;">%s</p>' % self.rich(t)
                    for t in b['paras']))

    def table(self, rows):
        head, body = rows[0], rows[1:]
        n = len(head)
        w0 = 32
        wi = (100 - w0) // (n - 1)
        th = ''.join('<td style="padding:8px 3px;background:%s;color:#FFFFFF;font-size:12px;line-height:1.4;font-weight:bold;'
                     'text-align:center;border:1px solid %s;width:%d%%;">%s</td>' % (NAVY, NAVY, w0 if i == 0 else wi, leaf(c))
                     for i, c in enumerate(head))
        trs = []
        for r, row in enumerate(body):
            bg = '#FFFFFF' if r % 2 == 0 else '#F5F9FC'
            tds = []
            for i, c in enumerate(row):
                hot = c.startswith('==')
                c = c.strip('=')
                st = ('padding:8px 4px;font-size:13px;line-height:1.4;border:1px solid #E3EAF2;background:%s;text-align:%s;color:%s;%s'
                      % (bg, 'left' if i == 0 else 'center', NAVY if i == 0 else ('#FFFFFF' if hot else '#55606F'),
                         'font-weight:bold;' if i == 0 or hot else ''))
                inner = leaf(c) if not hot else sp('display:inline-block;padding:0 6px;border-radius:3px;background:%s;' % BLUE, c)
                tds.append('<td style="%s">%s</td>' % (st, inner))
            trs.append('<tr>%s</tr>' % ''.join(tds))
        return ('<table style="width:100%%;border-collapse:collapse;table-layout:fixed;margin:0;">'
                '<tbody><tr>%s</tr>%s</tbody></table>' % (th, ''.join(trs)))

    def b_table(self, b):
        title, sub = (b['args'] + ['', ''])[:2]
        return sec('margin:0 16px 24px;',
            '<p style="margin:0 0 8px;font-size:15px;line-height:1.5;color:%s;font-weight:bold;">%s</p>' % (NAVY, leaf(title))
            + self.table(b['rows'])
            + '<p style="margin:6px 0 0;font-size:12px;line-height:1.6;color:%s;">%s</p>' % (self.P['muted'], self.rich(sub)))

    def b_bars(self, b):
        title, unit = (b['args'] + ['', ''])[:2]
        mx = max(v for _, v in b['items'])
        rows = []
        for name, v in b['items']:
            w = int(round(v / mx * 100))
            hot = v == mx
            nm, _, sub = name.partition(' · ')
            lab = leaf(nm) + ('<br>' + sp('color:#8A94A3;font-size:11px;', sub) if sub else '')
            rows.append('<tr><td style="width:42%%;padding:6px 6px 6px 0;font-size:13px;line-height:1.35;color:%s;vertical-align:middle;">%s</td>'
                        '<td style="padding:6px 0;vertical-align:middle;">%s</td></tr>' % (NAVY, lab,
                            sec('background:#EEF2F6;border-radius:4px;',
                                sec('width:%d%%;background:%s;border-radius:4px;text-align:right;padding:0 6px;box-sizing:border-box;' % (w, BLUE if hot else '#7FC6EE'),
                                    '<p style="margin:0;font-size:12px;line-height:22px;color:#FFFFFF;font-weight:bold;">%s</p>' % leaf('%d' % v)))))
        return sec('margin:0 16px 24px;padding:14px;border:1px solid #E3EAF2;border-radius:8px;',
            '<p style="margin:0 0 6px;font-size:15px;line-height:1.5;color:%s;font-weight:bold;">%s</p>' % (NAVY, leaf(title))
            + '<table style="width:100%%;border-collapse:collapse;"><tbody>%s</tbody></table>' % ''.join(rows)
            + '<p style="margin:6px 0 0;font-size:12px;line-height:1.6;color:%s;">%s</p>' % (self.P['muted'], self.rich(unit)))

    def b_warn(self, b):
        return sec('margin:0 16px 22px;padding:12px 14px 2px;background:%s;border-left:4px solid %s;border-radius:0 8px 8px 0;' % (self.P['goldlight'], GOLD),
            '<p style="margin:0 0 8px;font-size:13px;line-height:1.6;">%s%s</p>' % (
                self.tagx('避坑', GOLD, NAVY), sp('color:%s;font-weight:bold;' % NAVY, b['args'][0] if b['args'] else ''))
            + ''.join(self.p(t, 'font-size:14px;margin-bottom:10px;') for t in b['paras']))

    def datacards(self, title, cards):
        tds = []
        for i, (label, num, note) in enumerate(cards):
            hot = i == len(cards) - 1
            tds.append('<td style="width:50%%;padding:0 %s 0 %s;vertical-align:top;">%s</td>' % (
                '4px' if i == 0 else '0', '0' if i == 0 else '4px',
                sec('background:%s;border-radius:8px;padding:12px 10px;text-align:center;' % (BLUE if hot else '#F1F4F8'),
                    '<p style="margin:0;font-size:12px;line-height:1.5;color:%s;">%s</p>' % ('#DDF0FB' if hot else self.P['muted'], leaf(label))
                    + '<p style="margin:2px 0;font-size:30px;line-height:1.3;font-weight:bold;color:%s;">%s</p>' % ('#FFFFFF' if hot else NAVY, leaf(num))
                    + '<p style="margin:0;font-size:12px;line-height:1.5;color:%s;">%s</p>' % ('#DDF0FB' if hot else self.P['muted'], leaf(note)))))
        return ('<p style="margin:0 0 8px;font-size:13px;line-height:1.5;color:%s;font-weight:bold;text-align:center;">%s</p>' % (NAVY, leaf(title))
                + '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody><tr>%s</tr></tbody></table>' % ''.join(tds))

    def b_calc(self, b):
        return sec('margin:0 16px 22px;padding:14px 14px 14px;border:1px solid #D6E9F5;border-radius:10px;',
            '<p style="margin:0 0 10px;font-size:13px;line-height:1.6;">%s</p>' % self.tagx(b['args'][0], BLUE, '#FFFFFF')
            + ''.join(self.p(t, 'font-size:14px;margin-bottom:8px;') for t in b['lines'])
            + sec('margin-top:12px;', self.datacards(b['cards_title'], b['cards'])))

    def b_duo(self, b):
        tds = []
        for i, (k, v) in enumerate(b['items']):
            tds.append('<td style="width:50%%;vertical-align:top;padding:0 %s 0 %s;">%s</td>' % (
                '4px' if i == 0 else '0', '0' if i == 0 else '4px',
                sec('border:1px solid %s;border-radius:8px;padding:10px;background:%s;' % ('#D6E9F5' if i == 0 else BLUE, '#FFFFFF' if i == 0 else self.P['plight']),
                    '<p style="margin:0 0 6px;font-size:15px;line-height:1.5;color:%s;font-weight:bold;">%s</p>' % (NAVY if i == 0 else BLUE, leaf(k))
                    + '<p style="margin:0;font-size:13px;line-height:1.7;color:#55606F;text-align:left;">%s</p>' % self.rich(v))))
        return sec('margin:0 16px 22px;',
            '<p style="margin:0 0 8px;font-size:15px;line-height:1.5;color:%s;font-weight:bold;">%s</p>' % (NAVY, leaf(b['args'][0]))
            + '<table style="width:100%%;border-collapse:collapse;table-layout:fixed;"><tbody><tr>%s</tr></tbody></table>' % ''.join(tds))

    def numlist(self, items, labels):
        out = []
        for i, t in enumerate(items):
            out.append('<tr><td style="width:30px;vertical-align:top;padding:2px 0 12px;">%s</td><td style="vertical-align:top;padding:0 0 12px 8px;">%s</td></tr>' % (
                '<p style="margin:0;font-size:13px;line-height:24px;">%s</p>' % sp(
                    'display:inline-block;width:24px;height:24px;line-height:24px;border-radius:12px;background:%s;color:#FFFFFF;text-align:center;font-weight:bold;' % BLUE,
                    labels[i]),
                self.p(t, 'margin:0;font-size:14px;')))
        return '<table style="width:100%%;border-collapse:collapse;"><tbody>%s</tbody></table>' % ''.join(out)

    def b_gates(self, b):
        return sec('margin:0 16px 20px;', self.numlist(b['items'], ['1', '2', '3', '4', '5']))

    def b_steps(self, b):
        return sec('margin:0 16px 20px;padding:14px 14px 2px;background:#F7FAFD;border-radius:10px;',
            self.numlist(b['items'], ['1', '2', '3', '4', '5']))

    def b_verdict(self, b):
        return sec('margin:0 16px 22px;padding:18px 16px;background:%s;border-radius:10px;' % NAVY,
            '<p style="margin:0 0 8px;font-size:12px;line-height:1.6;">%s</p>' % self.tagx('判断线', GOLD, NAVY)
            + ''.join('<p style="margin:0;font-size:18px;line-height:1.6;color:#FFFFFF;font-weight:bold;">%s</p>' % self.title_html(t, color='#FFD666')
                      for t in b['paras']))

    def b_end(self, b):
        it = b['items']
        return sec('margin:30px 16px 16px;padding:18px 16px 14px;background:%s;border-radius:10px;text-align:center;' % self.P['plight'],
            '<p style="margin:0 0 10px;font-size:14px;line-height:1.8;color:%s;">%s</p>' % (self.P['text'], self.rich(it[0]))
            + '<p style="margin:0 0 12px;font-size:15px;line-height:1.8;color:%s;font-weight:bold;">%s</p>' % (NAVY, self.rich(it[1]))
            + '<p style="margin:0;font-size:13px;line-height:1.6;">%s</p>' % sp(
                'display:inline-block;padding:4px 14px;border-radius:14px;background:%s;color:#FFFFFF;font-weight:bold;' % BLUE, it[2]))

    # 产品列表（选购清单）：⑧ xuangou 的主组件。①–⑦ 用这一版通用实现（继承主题自动换色）：
    # 分类标题条 + 细框产品卡 + 「标签：正文」要点；标签含「适合」的要点铺浅底。
    def b_products(self, b):
        name, tag = (b['args'] + ['', ''])[:2]
        self.cat = getattr(self, 'cat', 0) + 1
        head = ('<p style="margin:0 0 4px;font-size:13px;line-height:1.6;">%s%s</p>' % (
                    self.tagx('%02d' % self.cat, BLUE, '#FFFFFF'), sp('color:%s;font-size:16px;font-weight:bold;' % NAVY, name))
                + ('<p style="margin:0 0 12px;font-size:12px;line-height:1.6;color:#8A94A3;">%s</p>' % leaf(tag) if tag else ''))
        intro = ''.join(self.p(t, 'font-size:14px;margin-bottom:12px;') for t in b.get('intro', []))
        cards = []
        for pd in b.get('products', []):
            title = ('<p style="margin:0 0 8px;padding:0 0 8px;font-size:15px;line-height:1.5;color:%s;font-weight:bold;'
                     'border-bottom:1px dashed #D6E9F5;">%s%s</p>' % (
                         NAVY, leaf(pd['name']),
                         sp('display:inline-block;margin-left:6px;padding:0 6px;border-radius:3px;background:#EEF7FD;color:%s;'
                            'font-size:11px;line-height:1.6;font-weight:normal;' % BLUE, pd['badge']) if pd['badge'] else ''))
            pts = []
            for lab, txt, sep in pd['points']:
                fit = '适合' in lab
                lead = sp('color:%s;font-weight:bold;' % (NAVY if fit else BLUE), lab + sep) if lab else ''
                pts.append('<p style="margin:0 0 8px;font-size:14px;line-height:1.75;color:#55606F;text-align:justify;%s">%s%s</p>' % (
                    'background:#FFF7E0;padding:6px 8px;border-radius:4px;' if fit else '', lead, self.rich(txt)))
            cards.append(sec('margin:0 0 12px;padding:12px 14px 4px;border:1px solid #D6E9F5;border-radius:8px;background:#FFFFFF;',
                             title + ''.join(pts)))
        return sec('margin:8px 16px 24px;', head + intro + ''.join(cards))

    def b_disclaimer(self, b):
        return sec('margin:0 16px 10px;padding:10px 0 0;border-top:1px solid %s;' % self.P['line'],
            ''.join('<p style="margin:0;font-size:12px;line-height:1.7;color:%s;text-align:justify;">%s</p>' % (self.P['muted'], self.rich(t))
                    for t in b['paras']))
