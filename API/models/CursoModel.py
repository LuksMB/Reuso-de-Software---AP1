from pydantic import BaseModel

class Curso(BaseModel):
    title: str
    description: str | None = None
    ch: int