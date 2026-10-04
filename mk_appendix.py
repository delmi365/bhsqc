# -*- coding: utf-8 -*-
"""从 material/unique.json 生成 附录A：164 篇原始条目索引。"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "material", "unique.json")
DST = os.path.join(ROOT, "src2", "10-appendixA.md")

with open(SRC, encoding="utf-8") as f:
    data = json.load(f)

# 原文章节 -> 本书对应章（用于回溯）
CH_MAP = {
    "第1章 心态与认知": "本书第 1–4 章",
    "第2章 形象建设": "本书第 5 章",
    "第3章 搭讪与认识": "本书第 7 章",
    "第4章 聊天与沟通": "本书第 8–11 章",
    "第5章 约会实战": "本书第 13–14 章",
    "第6章 关系升级": "本书第 15–17 章",
    "第7章 私密空间": "本书第 18–19 章",
    "第8章 长期关系": "本书第 20–22 章",
    "第9章 识别与筛选": "本书第 15、24 章",
    "第10章 应对策略": "本书第 23–24 章",
}

out = []
out.append("# 附录 A 原始条目索引（164 篇）")
out.append("")
out.append("原始素材共 172 篇，去掉 8 篇全文重复后为 164 篇。下面按原文档的章节顺序列出全部条目的原始标题，"
           "方便你回溯任何一条内容的出处。")
out.append("")
out.append("**关于标题的说明：** 这里保留原始标题原样，不做改写，因为它们是你回溯检索用的标识。"
           "其中大量出现的“把妹”“TD”等词是原文用语，本书正文中已全部替换或删除，参见附录 C。")
out.append("")
out.append("标题后的括号里是本篇字数；最后一行标注了这一组条目主要被编入了本书的哪些章节。")
out.append("")

total = 0
for ch, arts in data.items():
    n = len(arts)
    out.append("## %s（%d 篇）" % (ch, n))
    out.append("")
    for i, a in enumerate(arts, 1):
        title = re.sub(r"\s+", " ", a.get("title", "").strip())
        body = re.sub(r"\s+", "", a.get("content", ""))
        total += 1
        out.append("%d. %s（%d 字）" % (i, title, len(body)))
    out.append("")
    out.append("> 主要编入：%s" % CH_MAP.get(ch, "—"))
    out.append("")

out.append("---")
out.append("")
out.append("**合计：%d 篇。**" % total)

os.makedirs(os.path.dirname(DST), exist_ok=True)
with open(DST, "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("wrote", DST, "entries", total)
