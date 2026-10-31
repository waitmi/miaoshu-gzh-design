"""主题⑧　选购清单 · 产品列表推荐（xuangou）
浅灰页底 + 海军蓝头图 + 金色大月份 + 白色筛选胶囊；每个分类一条彩色横幅（6 色轮换），
下挂白色产品卡（左侧分类色条、✓ 圆标、示例角标、彩色标签要点、「适合」要点铺浅底），
淡蓝「顾问沟通提醒」框，深海军蓝「重要提示」页脚。
移植自喵叔长图模板 v1（longpost，2026-10-30「重疾险·医疗险选购清单」），改为公众号可粘贴的全内联写法：
头图不用背景图和毛玻璃，改纯色块 + 色块天际线；色条用 border-left；不用渐变、阴影只做极浅一层。
适合：月度选购清单、按需求分类的产品列表、「这几类各看哪几款」的推荐型文章。
"""
from base import sp, sec, blank, leaf, SANS
import miaolan

NAVY, NAVY2, BLUE, GOLD = '#051A4C', '#0B2A66', '#0288D1', '#F5B83D'
PAGE, TXT, SUB, MUTE, LINE = '#F3F6FA', '#1B2433', '#4A5568', '#8794A3', '#EEF1F5'
# 分类轮换色：(主色, 浅底)，与长图模板 theme.palette 一致
CATS = [('#0288D1', '#E3F3FC'), ('#B57A12', '#FBF1DE'), ('#2E7D5B', '#E4F2EB'),
        ('#C2506E', '#FAE8ED'), ('#5B5BD6', '#ECECFB'), ('#0F7F7F', '#E0F2F2')]


class T(miaolan.T):
    id = 'xuangou'
    name = '选购清单 · 产品列表推荐'
    P = dict(bg=PAGE, text='#2E3A4B', title=NAVY, muted=MUTE, line='#DDE4EC',
             primary=BLUE, plight='#E8F4FB', hl='#DDF0FB', ul='#8CCDF0', gold=GOLD,
             goldlight='#FFF6E0', red='#C2506E', redlight='#FAE8ED')
    font = SANS
    # 继承自①的组件：白卡放在浅灰页底上，其余沿用品牌蓝
    REMAP = {'#F7FAFD': '#FFFFFF', '#F6F8FA': '#FFFFFF', '#F2A900': GOLD, '#3A4556': '#2E3A4B',
             '#FFF7E0': '#FFF6E0', '#EEF7FD': '#E8F4FB'}

    def render(self, blocks):
        # 头图胶囊要列出全部分类，先扫一遍
        self.cats = [b for b in blocks if b['type'] == 'products']
        self.cat = 0
        return super().render(blocks)

    def cat_color(self, i, b=None):
        c = (b['args'][3] if b and len(b['args']) > 3 and b['args'][3].startswith('#') else None)
        base = CATS[i % len(CATS)]
        return (c, base[1]) if c else base

    # ---------- 头图：海军蓝块 + 品牌胶囊 + 金色月份 + 标题 + 英文 + 天际线 + 白色筛选胶囊 ----------
    def skyline(self):
        hs = [18, 30, 22, 40, 26, 14, 34, 48, 24, 30, 16, 38, 28, 20, 44, 26, 32, 18, 36, 22]
        tds = ''.join('<td style="padding:0 1px;vertical-align:bottom;">%s</td>' % blank(
            'height:%dpx;background:%s;line-height:%dpx;font-size:0;' % (h, '#16376F' if i % 3 else '#1D4585', h))
            for i, h in enumerate(hs))
        return ('<table style="width:100%%;border-collapse:collapse;table-layout:fixed;margin:0;">'
                '<tbody><tr>%s</tr></tbody></table>' % tds)

    def header(self):
        m = self.meta
        month = m.get('month', '')
        chips = [sp('color:%s;font-weight:bold;margin-right:10px;' % BLUE, m.get('chiplead', '本月精选' if month else '本期清单'))]
        for i, b in enumerate(self.cats):
            short = b['args'][2] if len(b['args']) > 2 and b['args'][2] else (b['args'][0] if b['args'] else '')
            n = len(b.get('products', []))
            chips.append(sp('white-space:nowrap;color:%s;margin-right:4px;' % TXT, '%s %d款' % (short, n)))
            if i < len(self.cats) - 1:
                chips.append(sp('color:#A9B4C2;margin-right:4px;', '·'))
        inner = (
            '<p style="margin:0 0 16px;font-size:12px;line-height:1.6;">%s</p>' % sp(
                'display:inline-block;padding:2px 12px;border:1px solid #3C5B91;border-radius:14px;background:#123672;'
                'color:#FFFFFF;font-weight:bold;letter-spacing:1px;', '喵叔说保')
            + sec('padding:14px 16px 14px;background:%s;border:1px solid #1E3F7A;border-radius:12px;' % NAVY2,
                ('<p style="margin:0 0 2px;font-size:38px;line-height:1.15;color:%s;font-weight:900;letter-spacing:0;">%s</p>' % (GOLD, leaf(month)) if month else '')
                + '<p style="margin:0 0 6px;font-size:22px;line-height:1.4;color:#FFFFFF;font-weight:bold;letter-spacing:1px;">%s</p>' % self.head_title()
                + ('<p style="margin:0 0 6px;font-size:13px;line-height:1.5;color:#D5DEEC;">%s</p>' % leaf(m['sub']) if m.get('sub') else '')
                + ('<p style="margin:0;font-size:9px;line-height:1.4;color:#8EA3C6;letter-spacing:3px;">%s</p>' % leaf(m['en']) if m.get('en') else ''))
            + sec('margin:18px 0 0;', self.skyline())
            + sec('margin:0;padding:7px 12px;background:#FFFFFF;border-radius:10px;',
                '<p style="margin:0;font-size:12px;line-height:1.8;">%s</p>' % ''.join(chips)))
        return sec('background:%s;padding:16px 16px 18px;margin:0 0 22px;' % NAVY, inner)

    # ---------- 章节：海军蓝圆号 + 标题 ----------
    def b_h2(self, b):
        self.chap += 1
        return sec('margin:30px 16px 14px;',
            '<p style="margin:0;padding:0 0 8px;font-size:18px;line-height:1.5;color:%s;font-weight:bold;border-bottom:2px solid %s;">%s%s</p>' % (
                NAVY, BLUE,
                sp('display:inline-block;width:24px;height:24px;line-height:24px;margin-right:8px;border-radius:12px;background:%s;'
                   'color:#FFFFFF;font-size:12px;text-align:center;vertical-align:2px;' % NAVY, '%02d' % self.chap),
                leaf(b['text'])))

    # ---------- 产品列表：分类横幅 + 产品卡 ----------
    def b_products(self, b):
        name, tag = (b['args'] + ['', ''])[:2]
        c, tint = self.cat_color(self.cat, b)
        self.cat += 1
        no = sp('display:inline-block;width:22px;height:22px;line-height:20px;border:1px solid #FFFFFF;border-radius:12px;'
                'color:#FFFFFF;font-size:10px;font-weight:bold;text-align:center;box-sizing:border-box;', '%02d' % self.cat)
        nm = '<p style="margin:0;font-size:16px;line-height:1.4;color:#FFFFFF;font-weight:bold;letter-spacing:1px;">%s%s</p>' % (
            no, sp('margin-left:8px;', name))
        if len(name) + len(tag) <= 19:
            # 一行放得下：左名右标签
            banner = ('<table style="width:100%%;border-collapse:collapse;table-layout:fixed;margin:0;"><tbody><tr>'
                      '<td style="padding:7px 0 7px 8px;vertical-align:middle;background:%s;border-radius:10px 0 0 10px;">%s</td>'
                      '<td style="width:44%%;padding:7px 10px 7px 4px;vertical-align:middle;background:%s;border-radius:0 10px 10px 0;">'
                      '<p style="margin:0;font-size:11px;line-height:1.45;color:#FFFFFF;text-align:right;">%s</p></td>'
                      '</tr></tbody></table>' % (c, nm, c, leaf(tag)))
        else:
            # 分类名较长：标签换到第二行，避免名称被挤断
            banner = sec('padding:7px 10px 7px 8px;background:%s;border-radius:10px;' % c,
                nm + ('<p style="margin:2px 0 0 30px;font-size:11px;line-height:1.45;color:#FFFFFF;">%s</p>' % leaf(tag) if tag else ''))
        intro = ''.join(self.p(t, 'font-size:14px;margin:10px 2px 0;') for t in b.get('intro', []))
        cards = []
        for pd in b.get('products', []):
            ck = sp('display:inline-block;width:20px;height:20px;line-height:20px;margin-right:8px;border-radius:10px;background:%s;'
                    'color:%s;font-size:12px;font-weight:bold;text-align:center;vertical-align:1px;' % (tint, c), '✓')
            badge = (sp('display:inline-block;margin-left:6px;padding:0 6px;border-radius:4px;background:%s;color:%s;'
                        'font-size:11px;line-height:1.6;font-weight:normal;vertical-align:1px;' % (tint, c), pd['badge'])
                     if pd['badge'] else '')
            title = ('<p style="margin:0 0 6px;padding:0 0 9px;font-size:16px;line-height:1.5;color:%s;font-weight:bold;'
                     'border-bottom:1px solid %s;">%s%s%s</p>' % (TXT, LINE, ck, leaf(pd['name']), badge))
            pts = []
            for lab, txt, sep in pd['points']:
                fit = '适合' in lab
                dot = sp('display:inline-block;width:5px;height:5px;margin:0 7px 0 1px;border-radius:3px;background:%s;vertical-align:3px;' % c, '')
                lead = sp('color:%s;font-weight:bold;' % c, lab + sep) if lab else ''
                st = ('margin:8px 0 0;font-size:14px;line-height:1.78;color:%s;text-align:left;' % SUB)
                if fit:
                    st += 'background:%s;padding:6px 10px;border-radius:6px;color:%s;' % (tint, TXT)
                    pts.append('<p style="%s">%s%s</p>' % (st, lead, self.rich(txt)))
                else:
                    pts.append('<p style="%s">%s%s%s</p>' % (st, dot, lead, self.rich(txt)))
            cards.append(sec('margin:11px 0 0;padding:13px 14px 13px 14px;background:#FFFFFF;border-left:4px solid %s;'
                             'border-radius:12px;box-shadow:0 2px 10px rgba(15,32,64,0.06);' % c,
                             title + ''.join(pts)))
        return sec('margin:20px 16px 0;', banner + intro + ''.join(cards))

    # ---------- 提醒框（warn / key）：淡蓝「顾问沟通提醒」，首段加粗深色，其余浅灰 ----------
    def remind(self, title, paras):
        ps = []
        for i, t in enumerate(paras):
            st = ('margin:0 0 4px;font-size:14px;line-height:1.7;text-align:left;color:%s;%s' %
                  (('#2E3A4B', 'font-weight:bold;') if i == 0 else ('#5F6B7A', '')))
            ps.append('<p style="%s">%s</p>' % (st, self.rich(t)))
        return sec('margin:24px 16px 4px;padding:12px 15px 10px;background:#EAF5FC;border:1px solid #C9E5F6;border-radius:12px;',
            ('<p style="margin:0 0 6px;font-size:16px;line-height:1.5;color:%s;font-weight:bold;letter-spacing:1px;">%s</p>' % (BLUE, leaf(title)) if title else '')
            + ''.join(ps))

    def b_warn(self, b):
        return self.remind(b['args'][0] if b['args'] else '', b['paras'])

    def b_key(self, b):
        return self.remind('', b['paras'])

    def b_lead(self, b):
        return sec('margin:0 16px 8px;padding:12px 15px;background:#FFFFFF;border-radius:12px;border-left:4px solid %s;' % GOLD,
            ''.join(self.p(t, 'margin:0;font-size:15px;color:%s;text-align:left;' % TXT) for t in b['paras']))

    # ---------- 结尾 + 深海军蓝「重要提示」页脚 ----------
    def b_end(self, b):
        it = b['items']
        return sec('margin:28px 16px 0;padding:16px 16px 14px;background:#FFFFFF;border-radius:12px;text-align:center;',
            '<p style="margin:0 0 10px;font-size:14px;line-height:1.8;color:#2E3A4B;">%s</p>' % self.rich(it[0])
            + '<p style="margin:0 0 12px;font-size:15px;line-height:1.8;color:%s;font-weight:bold;">%s</p>' % (NAVY, self.rich(it[1]))
            + '<p style="margin:0;font-size:13px;line-height:1.6;">%s</p>' % sp(
                'display:inline-block;padding:4px 14px;border-radius:14px;background:%s;color:#FFFFFF;font-weight:bold;' % BLUE, it[2]))

    def b_disclaimer(self, b):
        ps = ''.join('<p style="margin:0 0 8px;font-size:12px;line-height:1.75;color:#C3CDDD;text-align:justify;">%s</p>' % self.rich(t)
                     for t in b['paras'])
        date = self.meta.get('date', '')
        return sec('margin:26px 0 0;padding:20px 18px 18px;background:%s;' % NAVY,
            '<p style="margin:0 0 10px;font-size:16px;line-height:1.5;color:%s;font-weight:bold;letter-spacing:1px;">%s</p>' % (GOLD, leaf('重要提示'))
            + ps
            + ('<p style="margin:10px 0 0;font-size:11px;line-height:1.6;color:#7F90AE;">%s</p>' % leaf('整理日期：' + date + '　·　喵叔说保') if date else ''))
