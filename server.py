
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CIVILIZATION API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://roalay67-afk.github.io"
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "app": "CIVILIZATION",
        "status": "online"
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/gifts")
def gifts():
    # Пока возвращаем пустой список.
    # Подключение реального каталога MRKT будет следующим этапом.
    return {"gifts": []}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "10000"))
    )
