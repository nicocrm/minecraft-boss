from pydantic import BaseModel

class Server(BaseModel):
    name: str
    description: str
    is_running: bool
