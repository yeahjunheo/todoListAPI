"""
the DB for this api should look something like this:

one main table that holds the todos, with their title, due date,
memo, id, and completion status.

as for the steps, since the relation to task to steps will be one-to-many,
we can create another table with a foreign key to the task id from the todo
table. This is followed by the contents of the step and its own id.

one consideration is that if the foreign key gets deleted, the corressponding
steps should also be deleted. Hence, the cascade.
"""

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
