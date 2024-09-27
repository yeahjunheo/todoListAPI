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
async def home(db: Session = Depends(get_db)):
    todos = db.query(models.Todo).order_by(models.Todo.due_date.asc()).all()
    result = {"todos": todos}
    return result

@app.get("/steps/{todo_id}")
def get_steps(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    steps = db.query(models.Steps).filter(models.Steps.todo_id == todo_id).all()
    result = {"task": todo, "steps": steps}
    return result


@app.post("/add")
def add_task(title: str = Form(..., min_length=1, max_length=100), db: Session = Depends(get_db)):
    new_todo = models.Todo(title=title)
    db.add(new_todo)
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.put("/update/status/{todo_id}")
def update_status(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.put("/update/date/{todo_id}")
def update_date(
    todo_id: int, due_date: date = Form(...), db: Session = Depends(get_db)
):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.due_date = due_date
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.put("/update/memo/{todo_id}")
def update_memo(todo_id: int, memo: str = Form(..., max_length=100), db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.memo = memo
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.post("/update/steps/{todo_id}")
def update_steps(todo_id: int, step: str = Form(..., min_length=1, max_length=100), db: Session = Depends(get_db)):
    new_step = models.Steps(todo_id=todo_id, step=step)
    db.add(new_step)
    db.commit()
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    steps = db.query(models.Steps).filter(models.Steps.todo_id == todo_id).all()
    result = {"task": todo, "step": steps}
    return result


@app.get("/delete/{todo_id}")
def delete_task(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/delete/step/{step_id}")
def delete_step(step_id: int, db: Session = Depends(get_db)):
    step = db.query(models.Steps).filter(models.Steps.id == step_id).first()
    todo = db.query(models.Todo).filter(models.Todo.id == step.todo_id).first()
    db.delete(step)
    db.commit()
    steps = db.query(models.Steps).filter(models.Steps.todo_id == todo.id).all()
    result = {"task": todo, "step_id": steps}
    return result


@app.get("/search")
def search_task(search_term: str, db: Session = Depends(get_db)):
    searched_todos = (
        db.query(models.Todo)
        .filter(models.Todo.title.like(f"{search_term}%"))
        .order_by(models.Todo.due_date.asc())
        .all()
    )
    return {"todos": searched_todos}
