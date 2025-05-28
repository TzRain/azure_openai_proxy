明白！我帮你写一个完整的 Python 项目，并配好 Dockerfile，运行时加入 `--network ollama-net`，方便你直接启动使用。

---

# 项目目录结构

```
azure_openai_proxy/
├── Dockerfile
├── main.py
├── auth.py
├── requirements.txt
├── .env
```

---

# 1. `requirements.txt`

```txt
fastapi
uvicorn[standard]
httpx
python-dotenv
azure-identity
```

---

# 2. `.env` 示例（请根据实际改）

```dotenv
AZURE_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_OPENAI_ENDPOINT=https://my-aoai.openai.azure.com
PORT=8787
```

---

# 3. `auth.py`

```python
import os
from azure.identity import ManagedIdentityCredential, AzureCliCredential, ChainedTokenCredential, get_bearer_token_provider

_credential = ChainedTokenCredential(
    ManagedIdentityCredential(client_id=os.getenv("AZURE_CLIENT_ID")),
    AzureCliCredential(),
)

_token_provider = get_bearer_token_provider(_credential, "https://cognitiveservices.azure.com/.default")

async def get_token() -> str:
    return _token_provider()
```

---

# 4. `main.py`

```python
import os
from fastapi import FastAPI, Request, Response
import httpx
from auth import get_token
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
TARGET = os.getenv("AZURE_OPENAI_ENDPOINT")
PORT = int(os.getenv("PORT", 8787))

@app.api_route("/api/aoai/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(full_path: str, request: Request):
    url = f"{TARGET}/openai/deployments/{full_path}"
    headers = dict(request.headers)
    headers["Authorization"] = f"Bearer {await get_token()}"
    headers.pop("host", None)

    async with httpx.AsyncClient() as client:
        if request.method == "GET":
            resp = await client.get(url, headers=headers, params=request.query_params)
        else:
            body = await request.body()
            resp = await client.request(request.method, url, headers=headers, content=body, params=request.query_params)

    excluded_headers = ["content-encoding", "transfer-encoding", "connection"]
    response_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded_headers}
    return Response(content=resp.content, status_code=resp.status_code, headers=response_headers)
```

---

# 5. `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8787"]
```

---

# 6. 构建镜像

```bash
docker build -t azure-openai-proxy:latest .
```

---

# 7. 运行容器，加入指定网络

```bash
docker run -d --name azure-openai-proxy --network ollama-net --env-file .env -p 8787:8787 azure-openai-proxy:latest
```

---

# 8. 使用示例

前端或 SDK 配置：

```js
options.baseURL = "http://<docker_host>:8787/api/aoai";
options.apiKey = "dummy"; // 只要非空即可
```

---

如果需要我帮你写 docker-compose 或 Kubernetes 配置，也可以告诉我！
