from datetime import datetime

from sqlalchemy import Column, String, VARCHAR, TIMESTAMP, Integer

from src.db.connector import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(VARCHAR, primary_key=True, index=True, unique=True)
    execution_timestamp = Column(TIMESTAMP)
    creation_timestamp = Column(TIMESTAMP, default=datetime.now())
    status = Column(Integer, default=0)
    url = Column(VARCHAR)
    data = Column(String)
