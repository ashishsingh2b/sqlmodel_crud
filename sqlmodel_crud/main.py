from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from contextlib import asynccontextmanager
from typing import Union


#Importaant : if you are using portery then closed the enviroment

class Task(SQLModel, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    content: str = Field(index=True)
    

URL_DATABASE='postgresql://postgres:password123#@localhost:5432/mytaskdatabase'

engine = create_engine(URL_DATABASE)



def create_db_and_tables():
     SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    create_db_and_tables()
    yield
    

app:FastAPI = FastAPI(lifespan=lifespan)



@app.post("/task/")
def create_hero(task: Task):
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
@app.put("/task/")   
def update_task(task:Task):
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task.id)
        results = session.exec(statement)
        db_task = results.one()
        

        db_task.content = task.content  
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task


@app.get("/task/")
def read_task():
    with Session(engine) as session:
        task = session.exec(select(Task)).all()
        return task
    
@app.delete("/task/")
def delete_task(task:Task):
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task.id)
        results = session.exec(statement)
        db_task = results.one()
        

        session.delete(db_task)
        session.commit()
        return "Task Deleted"
    
