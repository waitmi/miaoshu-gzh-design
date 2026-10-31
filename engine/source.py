"""原文读取与比对工具（自写）。

原文约定：Markdown，正文在第一个单独一行的 `---` 之前（之后的内部记录不发布、不参与比对）；
以 # 开头的标题行、> 开头的引用行不计入正文段落。
"""
import re


def source_paragraphs(path):
    body = open(path, encoding='utf-8').read().replace('\r', '').split('\n---\n')[0]
    out = []
    for ln in body.split('\n'):
        s = ln.strip()
        if s and not s.startswith('#') and not s.startswith('>'):
            out.append(s)
    return out


def norm(s):
    return re.sub(r'[\s，。、；：？！「」『』“”‘’（）()·|,.:;!?\-—…]', '', s)


def coverage(paras, text):
    """返回原文中缺失/被改动的段落（按逗号句号切片逐片比对）。"""
    nt = norm(text)
    return [p for p in paras
            if any(norm(f) not in nt for f in re.split(r'[，。；：？！]', p) if norm(f))]
