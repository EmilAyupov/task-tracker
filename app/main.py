from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.database import Base, engine, get_db
from app.schemas import TaskCreate, TaskResponse, TaskUpdate

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tasks", status_code=201, response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Annotated[Session, Depends(get_db)],  # noqa: B008
):
    new_task = models.Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],  # noqa: B008
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        return task
    else:
        raise HTTPException(status_code=404, detail="Task not found")


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Annotated[Session, Depends(get_db)],  # noqa: B008
):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if "title" in task_data.model_fields_set:
        if task_data.title is None:
            raise HTTPException(status_code=422, detail="title cannot be null")
        db_task.title = task_data.title

    if "description" in task_data.model_fields_set:
        db_task.description = task_data.description

    if "completed" in task_data.model_fields_set:
        if task_data.completed is None:
            raise HTTPException(status_code=422, detail="completed cannot be null")
        db_task.completed = task_data.completed

    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/tasks/{task_id}", status_code=204, response_model=None)
def delete_task(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],  # noqa: B008
):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
