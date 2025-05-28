import os
import asyncio
import httpx

PROXY_URL = os.getenv("PROXY_URL", "http://localhost:8787/openai/deployments/o3/chat/completions")
PROXY_API_KEY = os.getenv("PROXY_API_KEY", "changeme")
API_VERSION = "2025-01-01-preview"  # 必须带上

async def main():
    headers = {
        "Content-Type": "application/json",
        "api-key": PROXY_API_KEY,
    }
    json_data = {
        "model": "o3",
        "messages": [
            {"role": "user", "content": "直接回答：中国的首都是哪里？"},
        ],
    }

    async with httpx.AsyncClient(timeout=300) as client:
        response = await client.post(
            PROXY_URL,
            headers=headers,
            params={"api-version": API_VERSION},
            json=json_data,
        )
        response.raise_for_status()
        data = response.json()

    print("Input:", json_data["messages"][0]["content"])
    print("Output:", data["choices"][0]["message"]["content"])

if __name__ == "__main__":
    asyncio.run(main())
