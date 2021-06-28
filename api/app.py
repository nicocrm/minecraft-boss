from fastapi import FastAPI

from config import config
from repository import Repository

app = FastAPI()
repo = Repository(config["minecraft_dir"])


@app.get("/")
async def index():
    return repo.list_servers()
