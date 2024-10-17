from fastapi import FastAPI

app: FastAPI = FastAPI()


@app.get("/healthcheck")
async def healthcheck() -> object:
    return {"status": "ok"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
