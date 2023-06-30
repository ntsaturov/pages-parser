from datetime import datetime

import requests
from bs4 import BeautifulSoup
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.db.crud.crud import update_task
from src.db.models.models import Task
from sqlalchemy import Result


def parse_page_task(db: Session, row: Result):
    result = {"tags": {}, "scripts": [], "status": True, "message": ""}

    task = Task(id=row[0],
                execution_timestamp=datetime.now(),
                creation_timestamp=row[2],
                status=20,
                url=row[4],
                data=str(result))
    try:
        page = requests.get(row[4], timeout=3)
        soup = BeautifulSoup(page.content, features="html.parser")
        for tag in soup.find_all():
            if tag.name in result.keys():
                result["tags"][tag.name] += 1
            else:
                result["tags"][tag.name] = 1
        sources = soup.findAll('script', {"src": True})
        for source in sources:
            result["scripts"].append(row[4] + source.get('src'))
        result["message"] = "Parsed successfully"
        task.data = str(result)
        status = update_task(db, task)
        if not status:
            raise SQLAlchemyError
    except Exception as e:
        result["status"] = False
        result["message"] = str(e)
        task.status = 21
        task.data = str(result)
        status = update_task(db, task)
        if not status:
            raise e
    return result
