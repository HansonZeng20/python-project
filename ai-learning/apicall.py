import logging
import os
import time
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("MOONSHOT_API_KEY", "")
URL = "https://api.moonshot.cn/v1/chat/completions"
MODEL = "kimi-k2.6"
SYSTEM_PROMPT = "你是编程助手，擅长Python和AI工程化"


def call_api_with_retry(
    url: str,
    headers: Optional[dict] = None,
    json: Optional[dict] = None,
    max_retry: int = 3,
    timeout: float = 30.0,
    backoff: float = 1.0,
) -> dict:
    """带重试的 POST 请求封装。"""
    for attempt in range(1, max_retry + 1):
        try:
            logger.info("尝试第 %d 次请求...", attempt)
            response = requests.post(url, headers=headers, json=json, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            logger.warning("请求失败: %s", exc)
            if attempt == max_retry:
                raise
            time.sleep(backoff * attempt)
    return {}


def chat_with_ai(
    message: str,
    model: str = MODEL,
    system_prompt: str = SYSTEM_PROMPT,
    api_key: Optional[str] = None,
) -> str:
    """调用 Moonshot API 进行对话。"""
    key = api_key or API_KEY
    if not key:
        raise ValueError("API Key 未设置，请通过参数传入或设置 MOONSHOT_API_KEY 环境变量")

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
    }

    result = call_api_with_retry(URL, headers=headers, json=data)
    logger.debug("API 返回: %s", result)
    return result["choices"][0]["message"]["content"]


if __name__ == "__main__":
    try:
        reply = chat_with_ai("你好，你是什么模型")
        print(reply)
    except Exception as exc:
        logger.error("调用失败: %s", exc)
        raise
