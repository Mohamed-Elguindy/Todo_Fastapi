from fastapi import FastAPI

app = FastAPI()

allTodo = [
    {"id": 1, "task": "Set up FastAPI project in IntelliJ", "priority": "High", "completed": True},
    {"id": 2, "task": "Configure Virtualenv and install dependencies", "priority": "High", "completed": True},
    {"id": 3, "task": "Create GET and POST endpoints for Todos", "priority": "Medium", "completed": False},
    {"id": 4, "task": "Connect to a database (SQLAlchemy or Tortoise)", "priority": "Medium", "completed": False},
    {"id": 5, "task": "Test endpoints using Swagger UI (/docs)", "priority": "Low", "completed": False}
]
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/todos/{id}")
def get_todo(id:int):
    for item in allTodo:
        if item["id"] == id:
            return item

@app.get("/todos")
def get_todos(lastdo: int =None):
    if lastdo :
        return allTodo[:lastdo]
    return allTodo

@app.post("/todos")
def add_todo(todo : dict):
    lastdo = len(allTodo)+1
    new_todo= {
        "id": lastdo,
        "task" : todo["task"],
        "priortiy":todo["priority"],
        "completed": todo["completed"]
    }
    allTodo.append(new_todo)
    return todo