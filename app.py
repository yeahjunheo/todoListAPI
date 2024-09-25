"""
API functions

1. add new tasks to TODO list
2. update the status of the task
3. update the deadline of the task
4. update the memo of the task
5. update the steps of the task
6. delete the task
7. search for tasks by name
8. display the tasks in order of oldest to newest (deadline)
"""

from fastapi import FastAPI, Depends, Request, Form, status

from starlette.responses import RedirectResponse

from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from datetime import date

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def home(req: Request, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).order_by(models.Todo.due_date.desc()).all()
    return {"todos": todos}


@app.post("/add")
def add_task(req: Request, title: str = Form(...), db: Session = Depends(get_db)):
    new_todo = models.Todo(title=title)
    db.add(new_todo)
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.put("/update/status/{todo_id}")
def update_status(req: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.put("/update/date/{todo_id}")
def update_date(
    req: Request,
    todo_id: int,
    due_date: date = Form(...),
    db: Session = Depends(get_db),
):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.due_date = due_date
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.put("/update/memo/{todo_id}")
def update_memo(
    req: Request, todo_id: int, memo: str = Form(...), db: Session = Depends(get_db)
):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.memo = memo
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.post("/update/steps/{todo_id}")
def update_steps(
    req: Request, todo_id: int, step: str = Form(...), db: Session = Depends(get_db)
):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    new_step = models.Steps(todo_id=todo_id, step=step)
    db.add(new_step)
    db.commit()
    return {"task": todo, "step": step}


@app.get("/delete/{todo_id}")
def delete_task(req: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/delete/step/{step_id}")
def delete_step(req: Request, step_id: int, db: Session = Depends(get_db)):
    step = db.query(models.Steps).filter(models.Steps.id == step_id).first()
    db.delete(step)
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/search")
def search_task(req: Request, search_term: str, db: Session = Depends(get_db)):
    searched_todos = (
        db.query(models.Todo)
        .filter(models.Todo.title.like(f"{search_term}%"))
        .order_by(models.Todo.due_date.desc())
        .all()
    )
    return {"todos": searched_todos}
