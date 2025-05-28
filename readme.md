# Azure OpenAI Proxy

项目初衷是简化 Azure OpenAI 访问流程，将复杂的 Azure AD 认证封装在代理服务中。用户只需配置环境变量 `AZURE_CLIENT_ID` 和 `AZURE_OPENAI_ENDPOINT`，无需处理复杂认证。

1.用于生成 Azure AD 访问令牌（`AZURE_OPENAI_AD_TOKEN`），方便部分程序直接使用 Token 访问，绕过代理服务（如支持此方式的 SDK 或框架）。

2.搭建代理客户端，客户端通过统一的 `PROXY_URL` 和 `PROXY_API_KEY` 调用，兼容各种不支持 Azure AD 的工具。

---

## 环境配置

复制示例配置文件并编辑：

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 AZURE_CLIENT_ID、AZURE_OPENAI_ENDPOINT 和 PROXY_API_KEY
```

环境变量说明：

* `AZURE_CLIENT_ID` (string，必填)：Managed Identity Client ID
* `AZURE_OPENAI_ENDPOINT` (string，必填)：Azure OpenAI 服务终端地址，例如 `https://xxx.openai.azure.com`
* `PROXY_API_KEY` (string，必填)：代理服务访问密钥，客户端调用代理时需携带

---

## 直接生成 Azure AD 访问令牌 (推荐)

使用方法：

```bash
source ./generate_ad_token.sh
```

执行后，当前终端环境变量 `AZURE_OPENAI_AD_TOKEN` 会被设置，可直接供支持 Token 认证的程序使用。

---

## 构建与启动代理服务

```bash
docker build -t azure-openai-proxy .
docker run -d --name azure-openai-proxy --env-file .env --network [你的docker网络名称] -p 8787:8787 azure-openai-proxy
```

---

## 使用示例

Python 客户端示例（详见 `test_sdk.py` 和 `test_chat.py`）

```python
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint="http://localhost:8787",  # 容器内使用容器名替代 localhost
    api_version="2025-01-01-preview",
    api_key="你的代理API_KEY",
)

messages = [{"role": "user", "content": "中国的首都是哪里？"}]

response = client.chat.completions.create(
    model="o3",
    messages=messages,
)

print("Response:", response.choices[0].message.content)
```

---

## HTTP 请求示例

```
POST http://localhost:8787/openai/deployments/o3/chat/completions?api-version=2025-01-01-preview
Headers:
  api_key: <你的代理API Key>
Content-Type: application/json
Body:
{
  "model": "o3",
  "messages": [{"role": "user", "content": "测试"}]
}
```

---

## 测试

```bash
python test_chat.py
python test_proxy.py
python test_sdk.py
```

---

## 查看日志

```bash
docker logs -f azure-openai-proxy
```
