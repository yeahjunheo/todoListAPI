from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    task = Column(String(100))
    status = Column(Boolean, default=False)
    due_date = Column(Date, default=None)
    memo = Column(String(100))

    steps = relationship("Steps", backref="todo", cascade="all, delete-orphan")


class Steps(Base):
    __tablename__ = "steps"

    id = Column(Integer, primary_key=True)
    todo_id = Column(Integer, ForeignKey("todos.id", ondelete="CASCADE"))
    status = Column(Boolean, default=False)
    step = Column(String(100))
