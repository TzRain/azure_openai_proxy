# Azure OpenAI Proxy

项目实现了一个 FastAPI 代理服务，负责管理 Azure AD 认证，转发请求到 Azure OpenAI。

## 结构

* `proxy.py`：代理服务主程序
* `Dockerfile`：构建镜像配置
* `requirements.txt`：依赖列表
* `test_*.py`：测试脚本

## 配置

环境变量通过 `.env` 文件传入：

* `AZURE_CLIENT_ID`：Managed Identity Client ID
* `AZURE_OPENAI_ENDPOINT`：Azure OpenAI 终端地址
* `PROXY_API_KEY`：自定义的代理服务访问密钥（仅用于代理服务，作为对接第三方服务API_KEY）

## 构建与运行

```bash
docker build -t azure-openai-proxy .
docker run -d --name azure-openai-proxy --env-file .env --network [docker_network_name] -p 8787:8787 azure-openai-proxy
```

## 使用

请求示例：

```http
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

## 测试

直接运行测试脚本：

```bash
python test_chat.py
python test_proxy.py
python test_sdk.py
```

## 查看日志

```bash
docker logs -f azure-openai-proxy
```
