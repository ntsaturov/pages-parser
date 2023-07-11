import asyncio
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from sqlalchemy import Result
from sqlalchemy.orm import Session


def get_parse_result(task):
    # add a task
    asyncio.create_task(write_to_db())


async def write_to_db():
    print("Successfully write")

async def parse_page_task(db: Session, row: Result):
    result = {"tags": {}, "scripts": [], "status": True, "message": ""}

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

    except Exception as e:
        result["status"] = False
        result["message"] = str(e)

    finally:
        return result
