from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from config import config
from exceptions import ServerControlException
from repository import Repository

app = FastAPI()
repo = Repository(config["minecraft_dir"])


@app.get("/servers")
async def index():
    return [s async for s in repo.list_servers()]


@app.post("/servers/{server_name}/start")
async def start(server_name: str):
    return await repo.start_server(server_name)


@app.post("/servers/{server_name}/stop")
async def stop(server_name: str):
    return await repo.stop_server(server_name)


@app.exception_handler(ServerControlException)
def server_control_exception(_: Request, exc: ServerControlException):
    return JSONResponse(status_code=400, content={"message": str(exc)})
