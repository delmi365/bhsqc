# -*- coding: utf-8 -*-
"""校验第三本书（把话说清楚）的输出。"""
import os, re, zipfile

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
BASE = "把话说清楚_关系场景对话与回应手册"
rep = []

hp = os.path.join(OUT, BASE + "_电子书.html")
ep = os.path.join(OUT, BASE + ".epub")
mp = os.path.join(OUT, BASE + "_全书手稿.md")

h = open(hp, encoding="utf-8").read()
rep.append("HTML: %d bytes" % os.path.getsize(hp))
rep.append("封面: %s / 分部页: %d" % ("有" if 'class="cover"' in h else "无",
                                    len(re.findall(r'class="partpage"', h))))
rep.append("章 h2.ch: %d" % len(re.findall(r'<h2 class="ch">', h)))
rep.append("场景 h3: %d" % len(re.findall(r"<h3>", h)))
rep.append("表格: %d / 引用块: %d" % (len(re.findall(r"<table>", h)), len(re.findall(r"<blockquote>", h))))
rep.append("有序列表: %d / 无序列表: %d" % (len(re.findall(r"<ol", h)), len(re.findall(r"<ul>", h))))
rep.append("目录链接: %d" % len(re.findall(r'href="#sec-', h)))
rep.append("残留裸管道行: %d / 残留 ** : %d" % (len(re.findall(r"^\|", h, re.M)), h.count("**")))
rep.append("页脚已替换: %s" % ("是" if "涉及拒绝、边界与不适场景的回应方式" in h else "否"))

titles = [re.sub(r"<[^>]+>", "", t) for t in re.findall(r'<h2 class="ch">(.*?)</h2>', h, re.S)]
rep.append("--- 章节清单 (%d) ---" % len(titles))
rep += ["  " + t for t in titles]

txt = re.sub(r"<script.*?</script>", "", h, flags=re.S)
txt = re.sub(r"<style.*?</style>", "", txt, flags=re.S)
txt = re.sub(r"<[^>]+>", "", txt)
rep.append("HTML 纯文本字数(含目录/页脚): %d" % len(re.sub(r"\s+", "", txt)))

BAN = ["把妹", "进挪", "猫绳", "服从性测试", "ASD", "LMR", "变现", "供养者", "炮友", "跪舔"]
hits = [(w, h.count(w)) for w in BAN if w in h]
rep.append("违禁词抽查: %s" % (", ".join("%s×%d" % x for x in hits) if hits else "全部为 0，通过"))

z = zipfile.ZipFile(ep)
infos = z.infolist()
rep.append("EPUB: %d bytes, 条目 %d" % (os.path.getsize(ep), len(infos)))
rep.append("EPUB 首项: %s (type=%d, 0=STORED)" % (infos[0].filename, infos[0].compress_type))
rep.append("EPUB 坏文件: %s" % str(z.testzip()))
opf = z.read("OEBPS/content.opf").decode("utf-8")
rep.append("OPF: item %d, itemref %d" % (opf.count("<item "), opf.count("<itemref")))
rep.append("NAV 目录项: %d / NCX navPoint: %d"
           % (len(re.findall(r"<li>", z.read("OEBPS/nav.xhtml").decode("utf-8"))),
              len(re.findall(r"<navPoint", z.read("OEBPS/toc.ncx").decode("utf-8")))))

m = open(mp, encoding="utf-8").read()
rep.append("手稿: %d bytes, 字数(去空白) %d, h1 %d"
           % (os.path.getsize(mp), len(re.sub(r"\s+", "", m)), len(re.findall(r"^# ", m, re.M))))
rep.append("手稿中'可以这样说'出现次数: %d" % m.count("可以这样说"))

open(os.path.join(OUT, "_report3.txt"), "w", encoding="utf-8").write("\n".join(rep))
print("done")
