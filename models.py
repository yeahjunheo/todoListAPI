from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    complete = Column(Boolean, default=False)
    due_date = Column(Date)
    memo = Column(String(500))


class Steps(Base):
    __tablename__ = "steps"

    id = Column(Integer, primary_key=True)
    todo_id = Column(Integer, ForeignKey("todos.id", ondelete="CASCADE"))
    step = Column(String(200))
