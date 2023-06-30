import concurrent.futures
import time
from threading import Thread

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.api.api import get_db
from src.db.crud.crud import get_and_update_tasks
from src.tasks.tasks import parse_page_task


class TasksScheduler:
    def __init__(self, max_workers=4):
        self._max_workers = max_workers

    def __run(self, db: Session = next(get_db())):
        while True:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self._max_workers) as executor:
                exec_future = {executor.submit(parse_page_task, db, task): task for task in get_and_update_tasks(db)}
                for future in concurrent.futures.as_completed(exec_future):
                    url = exec_future[future]
                    try:
                        data = future.result()
                    except SQLAlchemyError as e:
                        print(e)
                    except Exception as e:
                        print('%r generated an exception: %s' % (url, e))
                    else:
                        print(data)

    def run(self):
        t = Thread(target=self.__run)
        t.setDaemon(True)
        t.start()
