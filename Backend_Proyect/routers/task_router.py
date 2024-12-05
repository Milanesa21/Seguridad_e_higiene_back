from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dataBase.db import get_db
from model.schemas.task_schema import TaskCreate, TaskResponse
from controllers.task_contrellers import create_task, get_tasks_by_date, mark_task_as_completed, delete_task
from datetime import date  # Usamos solo `date`, no `datetime`
from typing import List
from model.task import Task

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])

@task_router.post("/", response_model=TaskResponse)
def add_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva tarea en la base de datos.
    """
    return create_task(db, task)

@task_router.get("/{company_id}/{date}", response_model=List[TaskResponse])
def list_tasks(company_id: int, date: date, db: Session = Depends(get_db)):
    """
    Obtiene las tareas de una empresa específica para una fecha dada.
    """
    tasks = get_tasks_by_date(db, company_id, date)
    
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for the given date")
    
    return tasks

@task_router.get('/{id_empresa}', response_model=List[TaskResponse])
def get_all_tasks(id_empresa: int, db: Session = Depends(get_db)):
    """
    Obtiene todas las tareas de una empresa.
    """
    tasks = db.query(Task).filter(Task.company_id == id_empresa).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return tasks

@task_router.patch("/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion(task_id: int, db: Session = Depends(get_db)):
    """
    Marca o desmarca una tarea como completada.
    """
    task = mark_task_as_completed(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@task_router.delete("/{task_id}", response_model=TaskResponse)
def remove_task(task_id: int, db: Session = Depends(get_db)):
    """
    Elimina una tarea de la base de datos.
    """
    task = delete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
