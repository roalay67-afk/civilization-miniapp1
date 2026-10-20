import os
import httpx
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
    return {"app": "CIVILIZATION", "status": "online"}

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/gifts")
async def gifts():
    url = "https://api.tgmrkt.io/api/v1/gifts/saling"
    payload = {
        "collectionNames": [],
        "modelNames": [],
        "backdropNames": [],
        "symbolNames": [],
        "ordering": "Price",
        "lowToHigh": True,
        "maxPrice": None,
        "minPrice": None,
        "mintable": None,
        "number": None,
        "count": 20,
        "cursor": "",
        "query": None,
        "promotedFirst": False,
    }

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()

        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            items = data.get("gifts", data.get("items", []))
        else:
            items = []

        return {"gifts": items, "source": "MRKT"}


    except httpx.HTTPStatusError as e:
        return {
            "gifts": [],
            "source": "MRKT",
            "error": f"MRKT вернул HTTP {e.response.status_code}"
        }
    except httpx.RequestError as e:
        return {
            "gifts": [],
            "source": "MRKT",
            "error": f"Ошибка соединения: {type(e).__name__}"
        }
    except Exception as e:
        return {
            "gifts": [],
            "source": "MRKT",
            "error": f"Ошибка обработки: {type(e).__name__}"
        }
```


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "10000"))
    )
