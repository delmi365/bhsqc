# -*- coding: utf-8 -*-
import os, re, zipfile, sys
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
BASE = "价值交换_生存价值与繁殖价值"
rep = []
names = os.listdir(OUT)
for n in names:
    p = os.path.join(OUT, n)
    rep.append("%s  %d bytes" % (n, os.path.getsize(p)))

htmlp = os.path.join(OUT, BASE + "_电子书.html")
h = open(htmlp, encoding="utf-8").read()
rep.append("html 长度: %d" % len(h))
rep.append("h2.ch 章数: %d" % len(re.findall(r'<h2 class="ch">', h)))
rep.append("h3 小节数: %d" % len(re.findall(r"<h3>", h)))
rep.append("表格数: %d" % len(re.findall(r"<table>", h)))
rep.append("裸管道残留: %d" % len(re.findall(r"^\|", h, re.M)))
rep.append("未转换的 ** 残留: %d" % h.count("**"))
rep.append("目录链接数: %d" % len(re.findall(r'nav\.side|href="#sec-', h)))
# 正文纯文本字数
txt = re.sub(r"<[^>]+>", "", h)
txt = re.sub(r"\s+", "", txt)
rep.append("html 纯文本字数(含UI): %d" % len(txt))

epubp = os.path.join(OUT, BASE + ".epub")
z = zipfile.ZipFile(epubp)
infos = z.infolist()
rep.append("epub 首项: %s / 压缩方式 %d (0=stored)" % (infos[0].filename, infos[0].compress_type))
rep.append("epub 条目数: %d" % len(infos))
rep.append("epub 文件列表: " + ", ".join(i.filename for i in infos[:8]))
opf = z.read("OEBPS/content.opf").decode("utf-8")
rep.append("opf 中 item 数: %d, itemref 数: %d" % (opf.count("<item "), opf.count("<itemref")))
rep.append("epub 坏文件: %s" % str(z.testzip()))
open(os.path.join(OUT, "_report.txt"), "w", encoding="utf-8").write("\n".join(rep))
print("done")
