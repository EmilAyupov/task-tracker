from sqlalchemy import Boolean, Column, Integer, String

from app.database import Base


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, nullable=False, default=False)
