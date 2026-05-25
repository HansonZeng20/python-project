import json
from pathlib import Path

# Python的类没有public/private，靠约定（_前缀表示私有）
class Config:
    def __init__(self, api_key):  # 构造函数
        self.api_key = api_key    # 实例变量
    
    def get_headers(self):        # 实例方法
        return {"Authorization": f"Bearer {self.api_key}"}

# 使用
config = Config(api_key="sk-xxx")
headers = config.get_headers()

# 写一段：读取列表，过滤空值，打印每个元素
items = ["a", None, "b", "", "c"]
for item in items:
    if item:  # Python的空值判断比Java简洁
        print(item)


print(headers)

# 练习：读取一个JSON配置文件，修改值，写回去
config_path = Path("config.json")
with config_path.open("r", encoding="utf-8") as f:
    config = json.load(f)

config["model"] = "deepseek-chat"

with config_path.open("w", encoding="utf-8") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)


