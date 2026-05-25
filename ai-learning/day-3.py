"""
day-3.py — Prompt Engineering 实践
Phase 1 筑基期 | 角色 Prompt、CoT 思维链、Few-shot 示例、结构化 JSON 输出

学习目标：
1. 角色 Prompt — 通过 system prompt 让模型扮演特定角色
2. CoT (Chain-of-Thought) 思维链 — 引导模型分步思考
3. Few-shot 示例 — 用少量示例教会模型输出格式
4. 结构化 JSON 输出 — 让模型返回可解析的数据结构
"""

import json
import os
import time
from typing import Any

from dotenv import load_dotenv

from apicall import chat_with_ai

load_dotenv()

# 每次 API 调用后等待的秒数，避免连续请求导致超时
# 注意：apicall.py 内部已有 5 秒速率限制，这里可以设为 0
REQUEST_DELAY = 0


# ============================================================
# 1. 角色 Prompt — 让模型扮演不同角色
# ============================================================

def demo_role_prompt():
    """演示：同一个问题，不同角色给出不同回答风格。"""
    question = "什么是递归函数？给一个 Python 例子。"

    roles = [
        ("资深 Python 工程师", "你是资深 Python 工程师，回答专业简洁。"),
        ("小学老师", "你是小学老师，用生动比喻解释。"),
        ("面试官", "你是技术面试官，指出考点和易错点。"),
    ]

    print("=" * 60)
    print("【1. 角色 Prompt 演示】")
    print("=" * 60)

    for role_name, system_prompt in roles:
        print(f"\n>>> 角色：{role_name}")
        print(f"    system_prompt: {system_prompt[:40]}...")
        reply = chat_with_ai(question, system_prompt=system_prompt)
        print(f"\n{reply}\n")
        print("-" * 60)


# ============================================================
# 2. CoT 思维链 — 引导模型分步思考
# ============================================================

def demo_cot_prompt():
    """演示：CoT (Chain-of-Thought) 思维链，让模型显式展示推理过程。"""

    # 不使用 CoT — 直接要答案
    question_direct = """
一个农场有鸡和兔，头共 35 个，脚共 94 只。鸡和兔各有多少只？
直接给出答案。
"""

    # 使用 CoT — 要求分步推理
    question_cot = """
一个农场有鸡和兔，头共 35 个，脚共 94 只。鸡和兔各有多少只？

请按以下步骤思考并回答：
1. 设未知数：设鸡有 x 只，兔有 y 只
2. 列方程：根据头和脚的数量列出方程组
3. 解方程：逐步求解
4. 验证：检查答案是否符合题意
5. 最终答案：给出鸡和兔的数量
"""

    print("=" * 60)
    print("【2. CoT 思维链演示】")
    print("=" * 60)

    print("\n>>> 不使用 CoT（直接要答案）：")
    reply_direct = chat_with_ai(question_direct)
    print(reply_direct)
    print("\n" + "-" * 60)

    print("\n>>> 使用 CoT（分步推理）：")
    reply_cot = chat_with_ai(question_cot)
    print(reply_cot)
    print("\n" + "-" * 60)


# ============================================================
# 3. Few-shot 示例 — 用示例教会模型格式
# ============================================================

def demo_few_shot_prompt():
    """演示：Few-shot 学习，用 2-3 个示例让模型学会输出格式。"""

    # 任务：情感分析，将文本分类为正面/负面/中性
    prompt = """
请对以下用户评论进行情感分析，输出格式为：情感 -> 原因（一句话）

示例 1：
评论：这款手机电池续航太棒了，用了一整天还有电！
结果：正面 -> 用户对电池续航非常满意

示例 2：
评论：物流慢得要死，等了一周才到。
结果：负面 -> 用户对物流速度非常不满

示例 3：
评论：商品收到了，和描述基本一致。
结果：中性 -> 用户没有表达明显的情感倾向

现在请分析：
评论：客服态度超好，有问题秒回，还主动帮我解决了退换货！
结果：
"""

    print("=" * 60)
    print("【3. Few-shot 示例演示】")
    print("=" * 60)

    print("\n>>> Few-shot 情感分析：")
    reply = chat_with_ai(prompt)
    print(reply)
    print("\n" + "-" * 60)


# ============================================================
# 4. 结构化 JSON 输出 — 让模型返回可解析的数据
# ============================================================

def demo_json_output():
    """演示：通过 Prompt 要求模型输出标准 JSON，便于程序解析。"""

    # 任务：从一段文本中提取结构化信息
    prompt = """
请从以下招聘信息中提取关键字段，并以 JSON 格式输出。
要求：
- 只输出 JSON，不要有任何其他文字
- 如果某个字段信息缺失，用 null 表示
- JSON 格式如下：

{
  "job_title": "职位名称",
  "company": "公司名称",
  "salary_min": 最低薪资（数字，单位千）,
  "salary_max": 最高薪资（数字，单位千）,
  "location": "工作地点",
  "requirements": ["要求1", "要求2"],
  "benefits": ["福利1", "福利2"]
}

招聘信息：
"""

    job_description = """
阿里巴巴 - 高级 Python 后端工程师
地点：杭州
薪资：25k-50k·16薪

岗位职责：
1. 负责电商核心系统的后端开发与优化
2. 设计高并发、高可用的系统架构

任职要求：
1. 5年以上 Python 开发经验，精通 Django/FastAPI
2. 熟悉 MySQL、Redis、消息队列
3. 有大型分布式系统开发经验
4. 熟悉 Docker、Kubernetes

我们提供：
- 六险一金
- 免费三餐
- 租房补贴
- 年度体检
"""

    print("=" * 60)
    print("【4. 结构化 JSON 输出演示】")
    print("=" * 60)

    print("\n>>> 提取结构化信息（JSON 输出）：")
    reply = chat_with_ai(prompt + job_description)
    print(reply)

    # 尝试解析 JSON
    print("\n>>> 解析结果：")
    try:
        # 清理可能的 markdown 代码块标记
        cleaned = reply.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        data = json.loads(cleaned)
        print(json.dumps(data, indent=2, ensure_ascii=False))

        # 验证关键字段
        print("\n>>> 字段验证：")
        required_fields = ["job_title", "company", "salary_min", "salary_max",
                           "location", "requirements", "benefits"]
        for field in required_fields:
            value = data.get(field)
            status = "✅" if value is not None else "⚠️"
            print(f"  {status} {field}: {value}")

    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")
        print("原始输出：")
        print(reply)

    print("\n" + "-" * 60)


# ============================================================
# 5. 综合练习 — 角色 + CoT + Few-shot + JSON 输出
# ============================================================

def demo_comprehensive():
    """综合练习：将四种技巧结合，完成一个实际任务。"""

    system_prompt = """
你是一位专业的代码审查助手，擅长分析代码质量、发现潜在问题并提供改进建议。
你的分析风格严谨、细致，注重可维护性和性能。
"""

    user_prompt = """
请对以下 Python 代码进行审查，并按指定格式输出结果。

审查步骤：
1. 先通读代码，理解其功能
2. 逐行分析潜在问题（类型安全、异常处理、性能等）
3. 给出改进建议
4. 输出结构化结果

输出格式（必须为标准 JSON）：
{
  "code_function": "代码功能描述",
  "issues": [
    {
      "severity": "error/warning/info",
      "line": 行号,
      "description": "问题描述",
      "suggestion": "改进建议"
    }
  ],
  "overall_score": 1-10,
  "summary": "总体评价"
}

待审查代码：
```python
def divide(a, b):
    return a / b

def process_data(data):
    result = []
    for i in range(len(data)):
        if data[i] > 0:
            result.append(data[i] * 2)
    return result

def read_file(path):
    f = open(path, 'r')
    content = f.read()
    return content
```
"""

    print("=" * 60)
    print("【5. 综合练习 — 角色 + CoT + JSON 输出】")
    print("=" * 60)

    print("\n>>> 代码审查结果：")
    reply = chat_with_ai(user_prompt, system_prompt=system_prompt)
    print(reply)

    # 尝试解析
    print("\n>>> 解析审查结果：")
    try:
        cleaned = reply.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        result = json.loads(cleaned)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")

    print("\n" + "-" * 60)


# ============================================================
# 主程序
# ============================================================

DEMO_FUNCTIONS = {
    "1": ("角色 Prompt", demo_role_prompt),
    "2": ("CoT 思维链", demo_cot_prompt),
    "3": ("Few-shot 示例", demo_few_shot_prompt),
    "4": ("JSON 结构化输出", demo_json_output),
    "5": ("综合练习", demo_comprehensive),
}


def run_all():
    """运行所有演示，每次请求之间有延迟。"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "Prompt Engineering 实践 — Day 3" + " " * 17 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")

    for key, (name, func) in DEMO_FUNCTIONS.items():
        print(f"\n[ {key}/5 ] 正在运行: {name} ...")
        try:
            func()
        except Exception as e:
            print(f"\n❌ {name} 运行失败: {e}")
            break
        if key != "5":
            print(f"\n⏳ 等待 {REQUEST_DELAY} 秒后继续...")
            time.sleep(REQUEST_DELAY)

    print("\n✅ 演示完成！")
    print("\n学习要点回顾：")
    print("  1. 角色 Prompt — 用 system prompt 定义模型身份和回答风格")
    print("  2. CoT 思维链 — 要求模型展示推理过程，提升复杂任务准确率")
    print("  3. Few-shot 示例 — 用示例定义输出格式，减少歧义")
    print("  4. JSON 结构化输出 — 明确指定 schema，便于程序解析")
    print("  5. 组合使用 — 实际场景中通常多种技巧结合使用")


def run_single(choice: str):
    """运行单个演示。"""
    if choice not in DEMO_FUNCTIONS:
        print(f"无效选项: {choice}")
        return
    name, func = DEMO_FUNCTIONS[choice]
    print(f"\n>>> 运行: {name}")
    func()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # 命令行参数指定要运行的 demo，例如: python day-3.py 2
        run_single(sys.argv[1])
    else:
        # 交互式选择
        print("\nPrompt Engineering 实践 — Day 3")
        print("-" * 40)
        for key, (name, _) in DEMO_FUNCTIONS.items():
            print(f"  {key}. {name}")
        print("  0. 运行全部")
        print("-" * 40)

        choice = input("请选择要运行的演示 (0-5): ").strip()
        if choice == "0":
            run_all()
        else:
            run_single(choice)
