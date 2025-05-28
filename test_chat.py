import asyncio
from openai import AzureOpenAI

async def main():
    client = AzureOpenAI(
        azure_endpoint="http://localhost:8787",
        api_version="2025-01-01-preview",
        max_retries=5,
        api_key="changeme",
    )

    history = []  # 保存对话历史

    while True:
        prompt = input("你：")
        if prompt.strip().lower() in {"exit", "quit"}:
            break

        # 把历史和当前消息拼接起来发给模型
        history.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model="o3",
            messages=history,
        )

        answer = response.choices[0].message.content
        # 分割线
        print("-" * 50)
        print("AI：", answer)
        print("-" * 50)

        # 保存助手回复到历史
        history.append({"role": "assistant", "content": answer})

asyncio.run(main())
