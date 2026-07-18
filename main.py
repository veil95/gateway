from fastapi import FastAPI
from view.ws import router


app = FastAPI()
app.include_router(router)


@app.get("/")
async def get():
    return
