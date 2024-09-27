from pydantic import BaseModel
from datetime import date


class Todo(BaseModel):
    task: str


class TodoCreate(Todo):
    pass


class TodoUpdate(Todo):
    status: bool = False
    due_date: date | None = None
    memo: str | None = None


class TodoRead(Todo):
    id: int
    status: bool = False
    due_date: date | None = None
    memo: str | None = None

    class ConfigDict:
        from_attributes = True


class Step(BaseModel):
    step: str


class StepCreate(Step):
    pass


class StepUpdate(Step):
    status: bool = False


class StepRead(Step):
    id: int
    todo_id: int
    status: bool = False

    class ConfigDict:
        from_attributes = True
