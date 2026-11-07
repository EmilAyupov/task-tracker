from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, pattern=r".*\S.*")
    description: str | None = None
    completed: bool = False


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, pattern=r".*\S.*")
    description: str | None = None
    completed: bool | None = None
