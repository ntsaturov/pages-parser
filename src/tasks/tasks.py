import asyncio
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from sqlalchemy import Result
from sqlalchemy.orm import Session

from src.db.crud.crud import update_task
from src.db.models.models import Task


class Parser:
    def __init__(self, db: Session):
        self.db = db

    def get_parse_result(self, task):
        result = task.result()

        print(result["status"])

        task = Task(
            id=result["id"],
            execution_timestamp=datetime.now(),
            creation_timestamp=result["creation_timestamp"],
            status=20 if result["status"] else 21,
            url=result["url"],
            data=str(result["data"])
        )
        asyncio.create_task(self.write_to_db(task))

    async def write_to_db(self, task: Task):
        update_task(self.db, task)

    @staticmethod
    async def parse_page_task(row: Result):
        result = {
            "data":
                {
                    "tags": {}, "scripts": []
                },
            "status": True,
            "message": "",
            "id": row[0],
            "creation_timestamp": row[2],
            "url": row[4]
        }

        try:
            page = requests.get(row[4], timeout=3)
            soup = BeautifulSoup(page.content, features="html.parser")
            for tag in soup.find_all():
                if tag.name in result.keys():
                    result["data"]["tags"][tag.name] += 1
                else:
                    result["data"]["tags"][tag.name] = 1
            sources = soup.findAll('script', {"src": True})
            for source in sources:
                result["data"]["scripts"].append(row[4] + source.get('src'))
            result["message"] = "Parsed successfully"

        except Exception as e:
            result["status"] = False
            result["message"] = str(e)

        finally:
            return result
