import os, shutil, json, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))   # 教学资料
FILES = os.path.join(HERE, "files")
DOC = {'.pdf','.doc','.docx','.xls','.xlsx','.txt','.ppt','.pptx','.jpg','.jpeg','.png','.csv','.md'}

# 分类元信息：upload=True 表示真实复制并生成链接；False 仅列出（本地文件）
CATS = [
 {"id":"audio","icon":"🎧","name":"一、听力音频","upload":True,
  "desc":"高考日语听力训练相关音频、原文与印刷稿。音频文件过大未上传，仅上传文档部分（PDF/说明）。",
  "scopes":["562858041 高考日语绿宝书.听力","初级听力音频","高考日语初级听力","三轮答案音频原文","高考日语绿宝书（听力）基础巩固印刷用.pdf","听力原文及答案.pdf"]},
 {"id":"ppt","icon":"📊","name":"二、课件 PPT","upload":False,
  "desc":"各年级教学 PPT 课件及配套素材（体积过大，未上传云端，以下为本地文件）。",
  "fixed":[["ppt课件/","4 个","本地文件"],["原ppt课件/","52 个","本地文件"],["PPT素材/","27 个","本地文件"],["听力.pptx","1 个","本地文件"]]},
 {"id":"essay","icon":"✍️","name":"三、作文","upload":True,
  "desc":"高考日语作文范文、模板、万能句与写作格式资料。",
  "scopes":["●高考作文-2021年7月更新.pdf","11篇模板范文.pdf","11篇范文-高考日语作文模块练习.pdf","2022年时事热点相关作文.pdf","高考作文-郁梦婷.pdf","高考日语作文模块练习 11篇.pdf","高考日语作文模块练习.docx","作文写作稿纸.docx","书信万能句.pdf","关于日语作文书信格式.pdf","图表万能句.pdf","议论文万能句.pdf"]},
 {"id":"vocab","icon":"📝","name":"四、词汇与默写","upload":True,
  "desc":"单词默写纸、默写计划、动词/敬语默写表等词汇积累类资料。",
  "scopes":["单词默写纸","单词默写计划.docx","動詞默写表.docx","日语单词默写纸.zip","默写纸","敬语默写表.docx","导学案默写单","1600答案.doc","重点词汇，语法练习.docx"]},
 {"id":"grammar","icon":"🔤","name":"五、语法","upload":True,
  "desc":"助词、助动词、敬语、活用、形式名词等语法专项讲义、练习与图片素材。",
  "scopes":["がは区别.docx","でも、さえ、まで.docx","とたらばなら.docx","に的用法.txt","よう　そう　みたい","ようだ、みたいだ、らしい、そうだ.pdf","何.docx","使役.txt","假定四词.pdf","动词敬语表.pdf","动词敬语表_加水印.pdf","动词活用变形练习.pdf","助数词总结.pdf","助词复习题（答案付き）.pdf","助词复习题（答案無し）.pdf","助词总结.pdf","助词用法整理讲义.docx","助词练习.docx","形式名词-上、わけ、もの、こと.pdf","口語表現，聴解参照.pdf","汾高补助动词梳理2021.6.21.docx","疑问词+か.docx","形变表.xlsx","形变.jpg","形容词1.jpg","形容词2.jpg","语法翻译题","语法翻译题.zip"]},
 {"id":"textbook","icon":"📚","name":"六、教材与教辅","upload":False,
  "desc":"电子教材、人教版资料、假名教学材料及合格性考试资料（体积过大，未上传云端，以下为本地文件）。",
  "fixed":[["电子教材/","25 个","本地文件"],["人教/","191 个","本地文件"],["假名教学材料/","131 个","本地文件"],["合格性考试/","7 个","本地文件"]]},
 {"id":"exam","icon":"📄","name":"七、试卷、真题与参考答案","upload":True,
  "desc":"高考真题、模拟卷、专项练习卷及对应的参考答案、答题卡等。",
  "scopes":["日语高考真题2014-2023.pdf","真题改填空","南充2022高三摸底日语试卷.pdf","单选+完形填空参考答案.pdf","完形选择参考答案.pdf","日语三轮参考答案.pdf","日语二轮参考答案.pdf","日语二轮答案.docx","日语单项选择训练参考答案.doc","日语-合格性考试模拟试题（2022年度）(1).pdf","日语答题卡（七天）.pdf","日语考试注意点.pdf","试卷 2023年12月高三教学测试日语.docx","词汇阅读检测卷6月10号.docx","必修补充练习","补充课课练"]},
 {"id":"culture","icon":"🏯","name":"八、文化常识","upload":True,
  "desc":"日本文化常识题汇总与精简版。",
  "scopes":["（含答案2021年10月更新）文化常识题汇总.pdf","（含答案2023年06月更新）文化常识题汇总.pdf","文常.pdf"]},
 {"id":"grade","icon":"📅","name":"九、成绩、课表与考勤","upload":True,
  "desc":"各年级成绩明细、作息/晚自习课表、教学进度、花名册与考勤相关文件。",
  "scopes":["【2024届高三第二学期期初质量监测】所有班级学生小题得分明细(1).xlsx","9月考日语生成绩.xlsx","高一日语期末成绩.xlsx","高二下学期期末日语成绩.xlsx","高三期初考试成绩.xlsx","21-22作息时间表（2022年5月12日起执行）正.xlsx","23-24高三晚自习周末课表.xlsx","高二下课表.xlsx","教学进度表.xlsx","基础巩固计划.xlsx","暑期花名册.xlsx","考勤表.xlsx","教师表.jpg","手阅卡打分规范.pdf"]},
 {"id":"note","icon":"📒","name":"十、听课笔记与错题","upload":True,
  "desc":"教师听课记录、个人教学笔记与错题收集。",
  "scopes":["笔记.docx","杜宜祥听课笔记.docx","杜宜祥听课记录.docx","错题","错题收集.docx"]},
 {"id":"image","icon":"🖼️","name":"十一、图片与素材","upload":True,
  "desc":"散落的图片素材（多为语法/假名示意图）。",
  "scopes":["ecc1deb6339cd55105dc75d7c1543ac.png","f14819c0abf721b6dd34d33cb341c09.png","はが.png","五十音.png"]},
 {"id":"admin","icon":"📋","name":"十二、行政与合同","upload":True,
  "desc":"教学协议、退费单、补充协议及物品移交清单等行政文书。",
  "scopes":["日语教学协议-插班生.docx","日语班退费单.doc","王华鸣补充协议.doc","物品移交清单(杜宜祥).docx"]},
]

def human(sz):
    if sz >= 1024*1024: return "%.1f MB"%(sz/1024/1024)
    if sz >= 1024: return "%.0f KB"%(sz/1024)
    return "%d B"%sz

# 清理旧 files
if os.path.isdir(FILES):
    shutil.rmtree(FILES)
os.makedirs(FILES, exist_ok=True)

def copy_one(full, rel):
    dst = os.path.join(FILES, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(full, dst)

data = []
total = 0
for c in CATS:
    items = []
    if c["upload"]:
        names = set()
        for p in c["scopes"]:
            full = os.path.join(ROOT, p)
            if os.path.isdir(full):
                for dp,_,fs in os.walk(full):
                    for f in fs:
                        ext = os.path.splitext(f)[1].lower()
                        if ext in DOC:
                            fp = os.path.join(dp,f)
                            rel = os.path.relpath(fp, ROOT)
                            sz = os.path.getsize(fp)
                            link = "files/" + urllib.parse.quote(rel.replace("\\","/"))
                            items.append([f, link, human(sz), rel])
                            copy_one(fp, rel); total += sz
            else:
                ext = os.path.splitext(full)[1].lower()
                if ext in DOC and os.path.exists(full):
                    rel = os.path.relpath(full, ROOT)
                    sz = os.path.getsize(full)
                    link = "files/" + urllib.parse.quote(rel.replace("\\","/"))
                    items.append([os.path.basename(full), link, human(sz), rel])
                    copy_one(full, rel); total += sz
        items.sort(key=lambda x:x[0])
    else:
        for it in c["fixed"]:
            items.append([it[0], None, it[1], ""])
    data.append({"id":c["id"],"icon":c["icon"],"name":c["name"],"desc":c["desc"],
                 "upload":c["upload"],"items":items})

print("copied total: %.1f MB"%(total/1024/1024))
print("categories:", len(data))
for d in data:
    print("  %s: %d items"%(d["name"], len(d["items"])))

# 写出数据供 HTML 使用
with open(os.path.join(HERE,"site_data.json"),"w",encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
print("site_data.json written")
