import os, json

HERE = os.path.dirname(os.path.abspath(__file__))

# 默认管理口令（部署后可改此处重新生成）
PWD = "admin888"

tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
data = json.load(open(os.path.join(HERE, "site_data.json"), encoding="utf-8"))

js = json.dumps(data, ensure_ascii=False)
# 防止数据中出现 </script> 破坏页面
js = js.replace("</", "<\\/")

html = tpl.replace("__DATA__", js).replace("__PWD__", PWD)

out = os.path.join(HERE, "index.html")
open(out, "w", encoding="utf-8").write(html)
print("written:", out, "size:", len(html), "bytes")
print("categories:", len(data), "items:", sum(len(c.get("items", [])) for c in data))
