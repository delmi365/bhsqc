# -*- coding: utf-8 -*-
"""校验第二本书（不套路）的 HTML / EPUB / 手稿输出。"""
import os, re, zipfile, html as H

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
BASE = "不套路_从认识到长期关系的实操手册"
rep = []

hp = os.path.join(OUT, BASE + "_电子书.html")
ep = os.path.join(OUT, BASE + ".epub")
mp = os.path.join(OUT, BASE + "_全书手稿.md")
mdp = os.path.join(OUT, BASE + "_全书手稿.md")

h = open(hp, encoding="utf-8").read()
rep.append("HTML 文件: %d bytes" % os.path.getsize(hp))
rep.append("封面: %s" % ("有" if 'class="cover"' in h else "无"))
rep.append("分部页: %d" % len(re.findall(r'class="partpage"', h)))
rep.append("章 h2.ch: %d" % len(re.findall(r'<h2 class="ch">', h)))
rep.append("小节 h3: %d" % len(re.findall(r"<h3>", h)))
rep.append("表格: %d" % len(re.findall(r"<table>", h)))
rep.append("引用块: %d" % len(re.findall(r"<blockquote>", h)))
rep.append("有序列表: %d / 无序列表: %d" % (len(re.findall(r"<ol", h)), len(re.findall(r"<ul>", h))))
rep.append("目录链接: %d" % len(re.findall(r'href="#sec-', h)))
rep.append("残留裸管道行: %d" % len(re.findall(r"^\|", h, re.M)))
rep.append("残留 ** 标记: %d" % h.count("**"))
rep.append("残留未转义尖括号脚本: %d" % len(re.findall(r"<script>", h)))

# 章节标题清单
titles = re.findall(r'<h2 class="ch">(.*?)</h2>', h, re.S)
rep.append("--- 章节清单 (%d) ---" % len(titles))
for t in titles:
    rep.append("  " + re.sub(r"<[^>]+>", "", t))

# 字数
txt = re.sub(r"<script.*?</script>", "", h, flags=re.S)
txt = re.sub(r"<style.*?</style>", "", txt, flags=re.S)
txt = re.sub(r"<[^>]+>", "", txt)
txt = re.sub(r"\s+", "", txt)
rep.append("HTML 纯文本字数(含目录/页脚): %d" % len(txt))

# 违禁词抽查（确认原素材的 PUA 行话与敏感内容未在正文出现）
BAN = ["把妹", "进挪", "猫绳", "服从性测试", "ASD", "LMR", "TD ", "拿下她", "变现",
       "供养者", "炮友", "跪舔", "废物测试", "反荡妇"]
hits = []
low = h
for w in BAN:
    c = low.count(w)
    if c:
        hits.append("%s×%d" % (w, c))
rep.append("违禁词抽查: %s" % (", ".join(hits) if hits else "全部为 0，通过"))

# EPUB
z = zipfile.ZipFile(ep)
infos = z.infolist()
rep.append("EPUB: %d bytes, 条目 %d" % (os.path.getsize(ep), len(infos)))
rep.append("EPUB 首项: %s (compress_type=%d, 0=STORED)" % (infos[0].filename, infos[0].compress_type))
rep.append("EPUB 坏文件: %s" % str(z.testzip()))
opf = z.read("OEBPS/content.opf").decode("utf-8")
rep.append("OPF: item %d, itemref %d" % (opf.count("<item "), opf.count("<itemref")))
nav = z.read("OEBPS/nav.xhtml").decode("utf-8")
rep.append("NAV 目录项: %d" % len(re.findall(r"<li>", nav)))
ncx = z.read("OEBPS/toc.ncx").decode("utf-8")
rep.append("NCX navPoint: %d" % len(re.findall(r"<navPoint", ncx)))
bad = [i.filename for i in infos if z.read(i.filename).decode("utf-8", "ignore").count("<h1>") == 0
       and i.filename.startswith("OEBPS/chap")]
rep.append("空章节: %s" % (bad if bad else "无"))

# 手稿
m = open(mp, encoding="utf-8").read()
rep.append("手稿: %d bytes, 字数(去空白): %d" % (os.path.getsize(mp), len(re.sub(r"\s+", "", m))))
rep.append("手稿 h1 数: %d" % len(re.findall(r"^# ", m, re.M)))

open(os.path.join(OUT, "_report2.txt"), "w", encoding="utf-8").write("\n".join(rep))
print("done")
