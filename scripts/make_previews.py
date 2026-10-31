#!/usr/bin/env python3
"""生成 README 用的预览图：每套主题用其示例文章出图，写到 docs/previews/。

  <序号>-<主题id>-top.jpg   首屏（手机一屏，750px 宽）
  <序号>-<主题id>-full.jpg  完整长图（压缩到单张 < 1.5MB）
  <序号>-<主题id>-palette.png 色板
  overview.jpg              8 套总览（首屏 + 一段核心组件）

用法：
  python3 scripts/make_previews.py               全部主题 + 总览
  python3 scripts/make_previews.py tijian heiban 只重出指定主题（不重做总览）
  python3 scripts/make_previews.py --overview    只用已有截图重拼总览
  python3 scripts/make_previews.py --palettes    只重出色板图
"""
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
from builder import build  # noqa: E402
from shot import font_css, launch  # noqa: E402

OUT = os.path.join(ROOT, 'docs', 'previews')
WORK = os.path.join(ROOT, 'output', 'previews')
MAX_BYTES = 1_450_000

# (序号, id, 名称, 适合, 示例标记稿, 核心组件定位文字 a, b)
SHOWCASE = [
    ('1', 'miaolan', '① 喵叔蓝 · 科普卡片', '日常主力：条款释义 / 避坑 / 医保', '同部位复发', '算一笔账', '累计60万'),
    ('2', 'nuanzhi', '② 暖纸编辑 · 测评风', '案例复盘 / 观点长文 / 深度测评', '同部位复发', '同种重疾间隔期', '单位：天'),
    ('3', 'shenlan', '③ 深蓝鎏金 · 数据测算', '养老 / 年金 / 分红 / 医保档位算账', '同部位复发', '算一笔账', '累计60万'),
    ('4', 'wangge', '④ IP蓝瑞士网格 · 清单指南', '选购指南 / 清单 / 先看什么后看什么', '孩子医疗险免赔', '2025年医院账单的量级', '357.7'),
    ('5', 'tijian', '⑤ 保单体检报告单 · 诊断排查', '保单诊断 / 条款排查 / 政策条款解读', '保证续保', '定义四段 · 逐项检查结果', '约定费率'),
    ('6', 'heiban', '⑥ 黑板荧光笔 · 知识笔记', '医保怎么选 / 名词解释 / 一个公式讲清楚', '居民医保一档二档', '黑板推演 · 重庆', '735元'),
    ('7', 'leitai', '⑦ 测评擂台 · 产品横评', '多款横评 / 两款 PK / 单品拆解', '五款重疾横评', '肺结节赔额', '三项只给一项'),
    ('8', 'xuangou', '⑧ 选购清单 · 产品列表推荐', '月度选购清单 / 分类产品推荐 / 适合人群', '重疾医疗选购清单', '大额住院费用', '示例产品B'),
]

FIND = r'''([a, b]) => {
  let best = null;
  document.querySelectorAll('section').forEach(s => {
    const t = s.innerText;
    if (t.includes(a) && t.includes(b)) {
      const r = s.getBoundingClientRect();
      if (!best || r.height < best.h) best = {y: r.top + window.scrollY, h: r.height};
    }
  });
  return best;
}'''


def save_jpg(im, path, width, q=82):
    im = im.convert('RGB')
    if im.width != width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    while True:
        im.save(path, quality=q, optimize=True, progressive=True)
        if os.path.getsize(path) <= MAX_BYTES or q <= 50:
            break
        q -= 6
        if q < 64 and im.width > 600:
            im = im.resize((600, round(im.height * 600 / im.width)), Image.LANCZOS)
    return os.path.getsize(path)


def theme_images(item):
    n, tid, name, use, ex, a, b = item
    out = os.path.join(WORK, tid)
    src = os.path.join(ROOT, 'examples', ex + '.md')  # 附了原文的示例（如⑧）带原文构建，做覆盖比对
    rep, err = build(tid, os.path.join(ROOT, 'examples', ex + '.gzh.md'), out, src if os.path.exists(src) else None)
    print('\n'.join(l for l in rep if l.startswith('—')))
    if err:
        raise SystemExit('%s 有 ERROR，停止' % tid)
    im = Image.open(os.path.join(out, 'preview.png'))
    s1 = save_jpg(im.crop((0, 0, im.width, min(im.height, 1334))), os.path.join(OUT, '%s-%s-top.jpg' % (n, tid)), 750, 86)
    s2 = save_jpg(im, os.path.join(OUT, '%s-%s-full.jpg' % (n, tid)), 750, 80)
    # 核心组件截取
    from playwright.sync_api import sync_playwright
    html = os.path.join(out, '_find.html')
    open(html, 'w', encoding='utf-8').write('<!DOCTYPE html><html><head><meta charset="utf-8"><style>%s body{margin:0;width:375px;}</style></head><body>%s</body></html>'
                                             % (font_css(), open(os.path.join(out, 'body.html'), encoding='utf-8').read()))
    with sync_playwright() as p:
        br = launch(p)
        pg = br.new_page(viewport={'width': 375, 'height': 800}, device_scale_factor=2)
        pg.goto('file://' + html)
        pg.evaluate('document.fonts.ready')
        pg.wait_for_timeout(400)
        r = pg.evaluate(FIND, [a, b])
        br.close()
    os.remove(html)
    y0 = max(0, int(r['y'] * 2) - 40)
    im.crop((0, y0, im.width, y0 + min(int(r['h'] * 2) + 80, 1150))).save(os.path.join(out, 'comp.png'))
    im.crop((0, 0, im.width, 1300)).save(os.path.join(out, 'top.png'))
    print('%s：首屏 %.0fKB，长图 %.0fKB' % (tid, s1 / 1024, s2 / 1024))


def overview():
    cell = ('<td style="vertical-align:top;padding:0 14px 36px;width:752px;">'
            '<p style="margin:0;font:bold 30px/1.4 \'PingFang SC\',sans-serif;color:#111">%s</p>'
            '<p style="margin:0 0 14px;font:22px/1.4 \'PingFang SC\',sans-serif;color:#666">%s</p>'
            '<img src="file://%s/top.png" style="width:750px;display:block;border:1px solid #ccc">'
            '<p style="margin:16px 0 8px;font:bold 20px/1.4 \'PingFang SC\',sans-serif;color:#888">核心组件</p>'
            '<img src="file://%s/comp.png" style="width:750px;display:block;border:1px solid #ccc"></td>')
    cells = [cell % (name, use, os.path.join(WORK, tid), os.path.join(WORK, tid)) for _, tid, name, use, *_ in SHOWCASE]
    guide = [('日常条款释义 / 家庭避坑', '①'), ('案例复盘 / 观点长文', '②'), ('养老 / 年金 / 分红测算', '③'),
             ('选购指南 / 清单排序', '④'), ('保单诊断 / 政策条款解读', '⑤'), ('医保怎么选 / 带公式科普', '⑥'),
             ('多款横评 / 两款 PK', '⑦'), ('月度选购清单 / 分类产品推荐', '⑧')]
    gl = ''.join('<tr><td style="padding:14px 0;border-bottom:1px solid #D9DDE3;font:26px/1.4 \'PingFang SC\',sans-serif;color:#333">%s</td>'
                 '<td style="padding:14px 0;border-bottom:1px solid #D9DDE3;font:bold 30px/1.4 \'PingFang SC\',sans-serif;color:#0288D1;text-align:right">%s</td></tr>' % g
                 for g in guide)
    cells.append('<td style="vertical-align:top;padding:0 14px 36px;width:752px;">'
                 '<p style="margin:0 0 4px;font:bold 30px/1.4 \'PingFang SC\',sans-serif;color:#111">怎么选</p>'
                 '<p style="margin:0 0 18px;font:22px/1.4 \'PingFang SC\',sans-serif;color:#666">按文章类型对号入座，主力用①，每周轮换一套</p>'
                 '<table style="border-collapse:collapse;width:100%%;background:#fff;padding:0 24px;border:1px solid #ccc">'
                 '<tr><td colspan="2" style="padding:6px 24px 10px"><table style="border-collapse:collapse;width:100%%">%s</table></td></tr></table></td>' % gl)
    rows = ''.join('<tr>%s</tr>' % ''.join(cells[i:i + 3]) for i in range(0, len(cells), 3))
    html = ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>%s</style></head>'
            '<body style="margin:0;background:#E9EBEE;padding:30px 16px 0;width:2370px;">'
            '<p style="margin:0 14px 6px;font:bold 44px/1.4 \'PingFang SC\',sans-serif;color:#111">喵叔说保 · 公众号排版 8 套主题</p>'
            '<p style="margin:0 14px 28px;font:24px/1.4 \'PingFang SC\',sans-serif;color:#666">375px 手机宽　｜　每套用最契合的一篇真实文章排版　｜　原文一字不改，只加结构与标签</p>'
            '<table style="border-collapse:collapse">%s</table></body></html>' % (font_css(), rows))
    f = os.path.join(WORK, 'overview.html')
    open(f, 'w', encoding='utf-8').write(html)
    from playwright.sync_api import sync_playwright
    png = os.path.join(WORK, 'overview.png')
    with sync_playwright() as p:
        br = launch(p)
        pg = br.new_page(viewport={'width': 2402, 'height': 1000}, device_scale_factor=1)
        pg.goto('file://' + f)
        pg.evaluate('document.fonts.ready')
        pg.wait_for_timeout(800)
        pg.screenshot(path=png, full_page=True)
        br.close()
    s = save_jpg(Image.open(png), os.path.join(OUT, 'overview.jpg'), 2400, 82)
    print('overview.jpg %.0fKB' % (s / 1024))


PALETTES = {
    'miaolan': [('#051A4C', '海军蓝'), ('#0288D1', 'IP蓝'), ('#F2A900', '金'), ('#3A4556', '正文灰'), ('#EEF7FD', '浅底')],
    'nuanzhi': [('#F6F0E4', '纸底'), ('#2A2522', '墨'), ('#B5452F', '砖红'), ('#D49A2A', '赭黄'), ('#FFE9A6', '荧光黄')],
    'shenlan': [('#0B1F3A', '深海蓝'), ('#C9A45C', '鎏金'), ('#1D4E89', '钴蓝'), ('#323A48', '正文灰'), ('#F3F5F8', '浅底')],
    'wangge': [('#F7F5F0', '米白'), ('#111111', '墨黑'), ('#0288D1', 'IP蓝'), ('#2B2B2B', '正文'), ('#D6D2C8', '细线')],
    'tijian': [('#FBFAF6', '米白'), ('#1F5FA8', '检验蓝'), ('#23955B', '正常'), ('#6B7280', '注意'), ('#D23F3F', '限制')],
    'heiban': [('#FFFDF7', '笔记纸'), ('#26392F', '黑板绿'), ('#F5D76E', '粉笔黄'), ('#FFE873', '荧光黄'), ('#E04F3F', '红笔')],
    'leitai': [('#15181E', '擂台黑'), ('#E5483B', '红方'), ('#2563C9', '蓝方'), ('#2C2F36', '正文'), ('#F4F5F7', '浅灰')],
    'xuangou': [('#051A4C', '海军蓝'), ('#F5B83D', '月份金'), ('#0288D1', '分类蓝'), ('#B57A12', '分类金'),
                ('#2E7D5B', '分类绿'), ('#C2506E', '分类玫红'), ('#F3F6FA', '页底灰')],
}


def palettes():
    """每套主题一条色板图：<序号>-<id>-palette.png（README 用）。"""
    from PIL import ImageDraw, ImageFont
    fd = font_dir_path()
    big = ImageFont.truetype(fd, 22) if fd else ImageFont.load_default()
    small = ImageFont.truetype(fd, 18) if fd else ImageFont.load_default()
    for n, tid, *_ in SHOWCASE:
        cols = PALETTES[tid]
        W, H, sw = 150 * len(cols), 132, 150
        im = Image.new('RGB', (W, H), '#FFFFFF')
        d = ImageDraw.Draw(im)
        for i, (hx, label) in enumerate(cols):
            x = i * sw
            d.rectangle([x + 6, 6, x + sw - 6, 70], fill=hx, outline='#D0D4DA')
            d.text((x + 10, 80), label, fill='#222222', font=big)
            d.text((x + 10, 108), hx, fill='#777777', font=small)
        im.save(os.path.join(OUT, '%s-%s-palette.png' % (n, tid)), optimize=True)
    print('palettes ok')


def font_dir_path():
    from shot import font_dir
    d = font_dir()
    return os.path.join(d, 'NotoSansSC.woff2') if d else None


def main():
    os.makedirs(OUT, exist_ok=True)
    args = sys.argv[1:]
    if args == ['--overview']:
        return overview()
    if args == ['--palettes']:
        return palettes()
    items = [x for x in SHOWCASE if not args or x[1] in args]
    for it in items:
        theme_images(it)
    if not args:
        overview()
        palettes()


if __name__ == '__main__':
    main()
