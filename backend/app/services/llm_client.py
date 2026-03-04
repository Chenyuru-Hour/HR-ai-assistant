import httpx
import asyncio
from app.core.config import get_settings


class LLMClient:
    def __init__(self):
        settings = get_settings()
        self.provider = settings.llm_provider
        self.api_key = settings.llm_api_key
        self.model = settings.llm_model
        self.chat_url = settings.llm_chat_completions_url

        #创建一个可复用的HTTP客户端实例
        self._client = httpx.AsyncClient(timeout = settings.llm_timeout_seconds)

    async def close(self):
        """关闭HTTP客户端，释放连接资源"""
        await self._client.aclose()

    async def chat(self, prompt: str, system_prompt: str = None) -> str:
        if not self.api_key:
            raise RuntimeError("LLM_API_KEY is not configured")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # 构建消息列表
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0,
        }

        max_retries = 3
        last_exception = None

        for attempt in range(1,max_retries + 1):
            try:
                response = await self._client.post(self.chat_url, headers=headers, json=payload)
                response.raise_for_status()
                break # 请求成功，跳出重试循环
            except httpx.TimeoutException as exc:
                last_exception = RuntimeError("LLM request timeout")
                last_exception.__cause__=exc
            except httpx.HTTPStatusError as exc:
                last_exception = RuntimeError(f"LLM upstream error:{exc.response.status_code}{exc.response.text}")
                last_exception.__cause__=exc
            except httpx.HTTPError as exc:
                last_exception = RuntimeError(f"LLM request failed:{exc}")
                last_exception.__cause__=exc

            # 如果还有重试机会，等待后重试
            if attempt < max_retries:
                await asyncio.sleep(attempt) # 第1次等1秒，第2次等2秒
        else:
            # 循环正常结束时执行，说明全部重试都失败了
            raise last_exception

        data = response.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError,IndexError,TypeError) as exc:
            raise RuntimeError(f"Invalid LLM response format: {data}") from exc

