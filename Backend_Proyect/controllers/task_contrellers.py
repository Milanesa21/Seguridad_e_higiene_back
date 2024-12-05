from sqlalchemy.orm import Session
from model.task import Task
from model.schemas.task_schema import TaskCreate
from datetime import date  # Usamos solo `date`, no `datetime`

def create_task(db: Session, task: TaskCreate):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks_by_date(db: Session, company_id: int, date: date):
    # Filtramos las tareas por `company_id` y la fecha exacta sin la parte de la hora
    return db.query(Task).filter(Task.company_id == company_id, Task.date == date).all()

def mark_task_as_completed(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.completed = not task.completed
        db.commit()
        db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return task
