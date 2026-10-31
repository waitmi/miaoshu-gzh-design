"""article.html 预览页模板（带「复制到公众号」按钮）。
预览页本身只在浏览器里打开用，复制的是 #gzh-body 里的正文 HTML（即 body.html 的内容）。
"""

PREVIEW = '''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · {theme}</title>
</head>
<body style="margin:0;background:#EDEFF2;">
<p style="position:sticky;top:0;z-index:9;margin:0;padding:10px 14px;background:#1F2329;color:#fff;font:14px/1.6 -apple-system,'PingFang SC',sans-serif;">
主题：{theme}　
<button id="cp" style="margin-left:8px;padding:6px 14px;border:0;border-radius:6px;background:#07C160;color:#fff;font-size:14px;cursor:pointer;">复制到公众号</button>
<span id="tip" style="margin-left:10px;color:#9AA4AF;">点按钮后到公众号编辑器 Ctrl/⌘+V</span></p>
<section style="max-width:420px;margin:16px auto 40px;background:#fff;box-shadow:0 2px 12px rgba(0,0,0,.08);">
<section id="gzh-body">{body}</section>
</section>
<script>
document.getElementById('cp').onclick = async function () {{
  var el = document.getElementById('gzh-body'), html = el.innerHTML, tip = document.getElementById('tip');
  try {{
    await navigator.clipboard.write([new ClipboardItem({{
      'text/html': new Blob([html], {{type: 'text/html'}}),
      'text/plain': new Blob([el.innerText], {{type: 'text/plain'}})}})]);
    tip.textContent = '已复制，去公众号编辑器粘贴';
  }} catch (e) {{
    var r = document.createRange(); r.selectNodeContents(el);
    var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
    document.execCommand('copy'); s.removeAllRanges();
    tip.textContent = '已复制（兼容模式），去公众号编辑器粘贴';
  }}
}};
</script>
</body></html>'''


def preview_page(title, theme_name, body):
    return PREVIEW.format(title=title, theme=theme_name, body=body)
