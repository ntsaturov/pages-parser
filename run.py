from fastapi import FastAPI

from src.api.api import router
from src.scheduler.scheduler import TasksScheduler

TasksScheduler().start()
app = FastAPI()
app.include_router(router)
