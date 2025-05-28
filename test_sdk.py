from openai import AzureOpenAI

proxy_url = "http://localhost:8787"

client = AzureOpenAI(
    azure_endpoint=proxy_url,
    api_version="2025-01-01-preview",
    max_retries=5,
    api_key="changeme",  # 替换为你的代理API Key
)

messages = [{"role": "user", "content": "直接回答：中国的首都是哪里？"}]

response = client.chat.completions.create(
    model="o3",
    messages=messages,
)

print("Input:", messages[0]["content"])
print("Output:", response.choices[0].message.content)
