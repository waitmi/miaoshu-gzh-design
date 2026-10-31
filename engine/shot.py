"""手机宽截图 + 375px 版面自检（自写）。依赖 playwright（python）+ Chromium。

浏览器查找顺序：环境变量 GZH_CHROMIUM → playwright 自带浏览器 → /usr/bin/chromium 等系统路径。
字体：仓库 fonts/ 下若有 NotoSansSC.woff2 / NotoSerifSC.woff2（或环境变量 GZH_FONT_DIR 指向的目录），
截图时把公众号字体栈映射到它们；没有则使用系统字体。字体只影响本地截图，不进入 body.html。
"""
import os
import shutil
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LAYOUT_JS = r'''
() => {
  const PUN = '，。、；：？！）」』”’》…';
  const issues = [];
  const root = document.body.firstElementChild;
  const W = root.getBoundingClientRect().right;
  document.querySelectorAll('p, td').forEach(el => {
    if (el.tagName === 'TD' && el.querySelector('p')) return;
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    const chars = [];
    let n;
    while ((n = walker.nextNode())) {
      for (let i = 0; i < n.data.length; i++) {
        const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + 1);
        const rc = r.getClientRects()[0];
        if (rc && n.data[i].trim()) chars.push({c: n.data[i], top: Math.round(rc.top), bottom: Math.round(rc.bottom), right: rc.right});
      }
    }
    if (!chars.length) return;
    const lines = [];
    chars.forEach(ch => {
      const L = lines[lines.length - 1];
      // 同一行判定：字框纵向重叠（大号数字 + 小号单位混排也算一行）
      if (L && ch.top < L.bottom - 2 && ch.bottom > L.top + 2) { L.cs.push(ch); L.top = Math.min(L.top, ch.top); L.bottom = Math.max(L.bottom, ch.bottom); }
      else lines.push({top: ch.top, bottom: ch.bottom, cs: [ch]});
    });
    const txt = chars.map(c => c.c).join('');
    lines.forEach((L, i) => {
      if (i > 0 && PUN.includes(L.cs[0].c)) issues.push('行首标点「' + L.cs[0].c + '」：' + txt.slice(0, 18));
      L.cs.forEach(ch => { if (ch.right > W + 0.5) issues.push('越界：' + txt.slice(0, 18)); });
    });
    if (lines.length > 1) {
      const last = lines[lines.length - 1].cs.filter(c => !PUN.includes(c.c));
      if (last.length <= 1) issues.push('孤字：' + txt.slice(-12));
    }
  });
  const over = [];
  document.querySelectorAll('section,table').forEach(el => { if (el.scrollWidth > el.clientWidth + 1 && getComputedStyle(el).overflow !== 'hidden') over.push(el.tagName); });
  if (over.length) issues.push('容器溢出 ×' + over.length);
  return {issues: [...new Set(issues)], height: document.body.scrollHeight};
}
'''


def font_dir():
    for d in (os.environ.get('GZH_FONT_DIR'), os.path.join(ROOT, 'fonts')):
        if d and os.path.exists(os.path.join(d, 'NotoSansSC.woff2')):
            return d
    return None


def font_css():
    d = font_dir()
    if not d:
        return ''
    css = "@font-face{font-family:'PingFang SC';src:url('file://%s/NotoSansSC.woff2');font-weight:100 900;}" % d
    if os.path.exists(os.path.join(d, 'NotoSerifSC.woff2')):
        css += "@font-face{font-family:'Songti SC';src:url('file://%s/NotoSerifSC.woff2');font-weight:100 900;}" % d
    return css


def shot_html(body, width=375):
    return ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>%s body{margin:0;width:%dpx;}</style>'
            '</head><body>%s</body></html>' % (font_css(), width, body))


def launch(p):
    exe = os.environ.get('GZH_CHROMIUM')
    if exe:
        return p.chromium.launch(executable_path=exe, args=['--no-sandbox'])
    try:
        return p.chromium.launch(args=['--no-sandbox'])
    except Exception:
        for c in ('/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome'):
            if os.path.exists(c) or shutil.which(os.path.basename(c)):
                return p.chromium.launch(executable_path=c, args=['--no-sandbox'])
        raise


def screenshot(body, png_path, width=375, scale=2, check=True):
    """把正文 HTML 截成手机长图；check=True 时同时返回版面自检结果 {issues, height}。"""
    from playwright.sync_api import sync_playwright
    fd, tmp = tempfile.mkstemp(suffix='.html')
    os.close(fd)
    open(tmp, 'w', encoding='utf-8').write(shot_html(body, width))
    try:
        with sync_playwright() as p:
            b = launch(p)
            pg = b.new_page(viewport={'width': width, 'height': 800}, device_scale_factor=scale)
            pg.goto('file://' + tmp)
            pg.evaluate('document.fonts.ready')
            pg.wait_for_timeout(600)
            res = pg.evaluate(LAYOUT_JS) if check else {'issues': [], 'height': 0}
            pg.screenshot(path=png_path, full_page=True)
            b.close()
    finally:
        os.remove(tmp)
    return res
