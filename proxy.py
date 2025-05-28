# proxy.py
import os
from fastapi import FastAPI, Request, Header, HTTPException, Response
import httpx
from azure.identity import ManagedIdentityCredential, get_bearer_token_provider
from dotenv import load_dotenv
# load_dotenv()  # 自动读取当前目录下的 .env 文件，加载环境变量

app = FastAPI()

# 环境变量读取
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")  # 如 https://xxx.openai.azure.com
PROXY_API_KEY = os.getenv("PROXY_API_KEY")
TIME_OUT_LIMIT = int(os.getenv("TIME_OUT_LIMIT", 600))  # 默认超时时间600秒

# Azure AD 认证准备
credential = ManagedIdentityCredential(client_id=CLIENT_ID)
token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

async def get_token():
    return token_provider()

@app.api_route("/openai/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_openai(full_path: str, request: Request, api_key: str = Header(None)):
    # 验证客户端API Key
    if api_key != PROXY_API_KEY:
        print(f"Invalid API Key: {api_key} vs {PROXY_API_KEY}")
        raise HTTPException(status_code=401, detail="Invalid API Key") 

    # 准备转发URL，完整路径
    url = f"{AZURE_OPENAI_ENDPOINT}/openai/{full_path}"

    # 处理请求头，去掉原有 Authorization
    headers = dict(request.headers)
    headers.pop("authorization", None)
    headers.pop("host", None)

    # 注入Azure AD Token
    token = await get_token()
    headers["Authorization"] = f"Bearer {token}"

    body = await request.body()
    async with httpx.AsyncClient(timeout=TIME_OUT_LIMIT) as client:
        try:
            resp = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=body,
                params=request.query_params,
            )
        except Exception as e:
            print(f"Request to Azure OpenAI failed: {e}")
            raise

    # 过滤响应头
    excluded_headers = {"content-encoding", "transfer-encoding", "connection"}
    response_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded_headers}

    return Response(content=resp.content, status_code=resp.status_code, headers=response_headers)
