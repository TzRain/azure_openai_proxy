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
