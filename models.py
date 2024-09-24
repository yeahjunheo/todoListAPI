from email.policy import default
from sqlalchemy import Boolean, Column, Integer, String, Date
from sqlalchemy import Relationship
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
    todo_id = 
    step = Column(String(200))