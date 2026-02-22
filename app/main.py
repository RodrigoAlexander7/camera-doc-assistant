from fastapi import FastAPI
from app.api.v1.endpoints import gemini_router

app = FastAPI()

app.include_router(gemini_router.router, prefix="/api/v1/gemini", tags=["gemini"])


@app.get("/")
def read_root():
    return {"mensaje": "hello from fastapi"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
