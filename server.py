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
    return {
        "app": "CIVILIZATION",
        "status": "online"
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/gifts")
async def gifts():
    token = os.environ.get("BOT_TOKEN")

    if not token:
        return {
            "gifts": [],
            "error": "BOT_TOKEN не настроен в Render"
        }

    url = (
        f"https://api.telegram.org/"
        f"bot{token}/getAvailableGifts"
    )

    try:
        async with httpx.AsyncClient(
            timeout=20
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

        if not data.get("ok"):
            return {
                "gifts": [],
                "error": "Telegram не смог вернуть каталог"
            }

        result = data.get("result", {})
        items = result.get("gifts", [])

        catalog = []

        for gift in items:
            sticker = gift.get("sticker", {})

            catalog.append({
                "id": gift.get("id"),
                "star_count": gift.get("star_count"),
                "total_count": gift.get("total_count"),
                "remaining_count": gift.get(
                    "remaining_count"
                ),
                "sticker": {
                    "file_id": sticker.get("file_id"),
                    "file_unique_id": sticker.get(
                        "file_unique_id"
                    ),
                    "type": sticker.get("type"),
                    "is_animated": sticker.get(
                        "is_animated", False
                    ),
                    "is_video": sticker.get(
                        "is_video", False
                    ),
                }
            })

        return {
            "gifts": catalog,
            "source": "Telegram",
            "count": len(catalog)
        }

    except httpx.HTTPStatusError as e:
        return {
            "gifts": [],
            "error": (
                f"Telegram вернул HTTP "
                f"{e.response.status_code}"
            )
        }

    except httpx.RequestError:
        return {
            "gifts": [],
            "error": "Не удалось подключиться к Telegram"
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "10000")),
    )
