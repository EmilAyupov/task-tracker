from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.database import Base, engine, get_db
from app.schemas import TaskCreate, TaskUpdate

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tasks", status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    new_task = models.Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.get("/tasks/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db),  # noqa: B008
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        return task
    else:
        raise HTTPException(status_code=404, detail="Task not found")


@app.patch("/tasks/{task_id}")
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),  # noqa: B008
):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if db_task:
        fields = task_data.model_dump(exclude_unset=True)
        for key, value in fields.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
        return db_task
    else:
        raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),  # noqa: B008
):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
