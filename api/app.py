from typing import cast

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
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


@app.delete("/servers/{server_name}/mods/{mod_name}")
async def remove_mod(server_name: str, mod_name: str):
    return await repo.remove_mod(server_name, mod_name)


@app.post("/servers/{server_name}/mods")
async def add_mod(server_name: str, file: UploadFile = File(...)):
    if not file.filename.endswith(".jar"):
        raise HTTPException(status_code=400, detail="Invalid file type")
    content = cast(bytes, await file.read())
    return await repo.add_mod(server_name, file.filename, content)


@app.exception_handler(ServerControlException)
def server_control_exception(_: Request, exc: ServerControlException):
    return JSONResponse(status_code=400, content={"message": str(exc)})
