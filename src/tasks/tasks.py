import asyncio
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup
from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.crud.crud import update_task
from src.db.models.models import Task


class Parser:
    def __init__(self, session: AsyncSession):
        self.session = session

    def get_parse_result(self, task):
        result = task.result()

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
        await update_task(self.session, task)

    @staticmethod
    async def _get_page(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.text()
                return data

    async def parse_page(self, row: Result):
        result = {
            "data":
                {
                    "tags": {}, "scripts": [], "message": ""
                },
            "status": True,
            "message": "",
            "id": row[0],
            "creation_timestamp": row[2],
            "url": row[4]
        }

        try:
            page = await self._get_page(row[4])
            soup = BeautifulSoup(page, features="html.parser")
            for tag in soup.find_all():
                if tag.name in result.keys():
                    result["data"]["tags"][tag.name] += 1
                else:
                    result["data"]["tags"][tag.name] = 1
            sources = soup.findAll('script', {"src": True})
            for source in sources:
                result["data"]["scripts"].append(row[4] + source.get('src'))
                result["data"]["message"] = "Parsed successfully"

        except Exception as e:
            result["status"] = False
            result["data"]["message"] = str(e)

        finally:
            return result
