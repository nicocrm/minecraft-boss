from typing import List
from pydantic import BaseModel

class Server(BaseModel):
    name: str
    description: str
    port: int
    is_running: bool
    mods: List[str]
