import json

import requests
from sqlalchemy.orm import Session

from src.db.crud.crud import update_task
from src.db.models.models import Task
from bs4 import BeautifulSoup


def parse_page_task(db: Session, task: Task):
    page = requests.get(task.url)
    soup = BeautifulSoup(page.content, features="html.parser")
    result = {"tags": {}, "scripts": []}
    for tag in soup.find_all():
        if tag.name in result.keys():
            result["tags"][tag.name] += 1
        else:
            result["tags"][tag.name] = 1

    sources = soup.findAll('script', {"src": True})
    for source in sources:
        result["scripts"].append(task.url + source.get('src'))

    task.data = str(result)
    task.status = 20
    return update_task(db, task)
