from fastapi import FastAPI

from config import config
from repository import Repository

app = FastAPI()
repo = Repository(config["minecraft_dir"])


@app.get("/servers")
async def index():
    return repo.list_servers()

@app.post("/servers/{server_name}/start")
async def start(server_name: str):
    repo.start_server(server_name)
