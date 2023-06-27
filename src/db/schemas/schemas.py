from pydantic import BaseModel


class TaskBase(BaseModel):
    id: str
    url: str
