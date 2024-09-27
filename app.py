from fastapi import FastAPI, Depends, HTTPException, status
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import schemas

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


@app.post("/add")
def add_task(task: schemas.TodoCreate, db: Session = Depends(get_db)):
    new_todo = models.Todo(task=task.task)
    db.add(new_todo)
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.put("/update/{todo_id}")
def update_status(
    todo_id: int, update_info: schemas.TodoUpdate, db: Session = Depends(get_db)
):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")

    update_task = update_info.model_dump(exclude_unset=True)

    for key, value in update_task.items():
        setattr(todo, key, value)

    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.delete("/delete/{todo_id}")
def delete_task(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(todo)
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.post("/add/steps/{todo_id}")
def add_steps(todo_id: int, step: schemas.StepCreate, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    
    new_step = models.Steps(todo_id=todo_id, step=step.step)
    db.add(new_step)
    db.commit()
    db.refresh(new_step)
    return new_step


@app.put("/update/steps/{step_id}")
def update_steps(
    step_id: int,
    step: schemas.StepUpdate,
    db: Session = Depends(get_db),
):
    new_step = db.query(models.Steps).filter(models.Steps.id == step_id).first()

    if not new_step:
        raise HTTPException(status_code=404, detail="Step not found")

    update_step = step.model_dump(exclude_unset=True)

    for key, value in update_step.items():
        setattr(new_step, key, value)

    db.commit()
    db.refresh(new_step)
    todo = db.query(models.Todo).filter(models.Todo.id == new_step.todo_id).first()
    steps = db.query(models.Steps).filter(models.Steps.todo_id == todo.id).all()
    result = {"task": todo, "step": steps}
    return result


@app.delete("/delete/steps/{step_id}")
def delete_step(step_id: int, db: Session = Depends(get_db)):
    step = db.query(models.Steps).filter(models.Steps.id == step_id).first()

    if not step:
        raise HTTPException(status_code=404, detail="Step not found")

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
        .filter(models.Todo.task.like(f"{search_term}%"))
        .order_by(models.Todo.due_date.asc())
        .all()
    )
    return {"todos": searched_todos}
