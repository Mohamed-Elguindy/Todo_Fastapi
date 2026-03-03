from unittest.mock import DEFAULT

from fastapi import FastAPI ,HTTPException
from typing import Optional,List
from enum import IntEnum
from pydantic import BaseModel ,Field

app = FastAPI()

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class todoBaseModel(BaseModel):
    todoName: str = Field(...,min_length=3,max_length=100,description="Task Name")
    priority: Priority = Field(default=Priority.LOW,description="Task priority")

class Todo(todoBaseModel):
    todoID: int = Field(...,description="Task ID")


class todoCreate(todoBaseModel):
    pass

class todoUpdate(BaseModel):
    todoName: Optional[str] = Field(None,min_length=3,max_length=100,description="Task Name")
    priority: Optional[Priority] = Field(None,description="Task priority")


allTodo = [
    Todo(todoID=1, todoName="Task 1", priority=Priority.MEDIUM),
    Todo(todoID=2, todoName="Task 2", priority=Priority.MEDIUM),
    Todo(todoID=3, todoName="Task 3", priority=Priority.HIGH),
    Todo(todoID=4, todoName="Task 4", priority=Priority.LOW),
]
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/todos/{id}" , response_model=Todo)
def get_todo(id:int):
    for item in allTodo:
        if item.todoID == id:
            return item
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/todos", response_model=List[Todo])
def get_todos(lastdo: int =None):
    if lastdo :
        return allTodo[:lastdo]
    return allTodo

@app.post("/todos", response_model=Todo)
def add_todo(todo : todoCreate):
    lastdo = len(allTodo)+1
    newTodo = Todo(todoID=lastdo, todoName=todo.todoName, priority =todo.priority)
    allTodo.append(newTodo)
    return newTodo

@app.put("/todos/{id}" , response_model=Todo)
def edit_todo(id:int ,updated_todo : todoUpdate):
    for item in allTodo:
        if item.todoID == id:
            if updated_todo.todoName is not None:
               item.todoName = updated_todo.todoName
            if updated_todo.priority is not None:
                item.priority = updated_todo.priority
            return item
        else:
            raise HTTPException(status_code=404, detail="Task not found")

@app.delete('/todos/{todo_id}')
def delete_todo(todo_id: int):
    for index, todo in enumerate(allTodo):
        if todo.todoID == todo_id:
            deleted_todo = allTodo.pop(index)
            return deleted_todo
    raise HTTPException(status_code=404, detail="Task not found")