import uvicorn
from fastapi import FastAPI

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.config import settings
from src.api.hotels import router as hotels_router


app = FastAPI()

app.include_router(hotels_router)


@app.get("/")
def func():
    return "Hello, World!"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
