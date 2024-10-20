from fastapi import FastAPI

from agent.mrs_agent import mrs_agent
from packet.mrs_packet import RunMrsRequest, RunMrsResponse

app: FastAPI = FastAPI()


@app.get('/healthcheck')
async def healthcheck() -> object:
    return {'status': 'ok'}


@app.post('/run')
async def run(request: RunMrsRequest) -> RunMrsResponse:
    return await mrs_agent.run(request=request)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
