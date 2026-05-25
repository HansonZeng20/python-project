# 练习1：把一个Java风格的循环改写成Pythonic风格
# Java风格（不要这样写）
items = ["a", None, "b", "", "c"]

result = []
for i in range(len(items)):
    if items[i] is not None:
        result.append(items[i].upper())

# Python风格（这样写）
result = [item.upper() for item in items if item is not None]

# 练习2：给定一个API响应JSON，提取所有name字段
response = {"data": [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]}
names = [item["name"] for item in response["data"]]