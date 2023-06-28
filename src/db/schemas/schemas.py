from pydantic import BaseModel


class TaskBody(BaseModel):
    url: str


class TaskBase(BaseModel):
    id: str
    url: str
