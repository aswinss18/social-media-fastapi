from fastapi import FastAPI,Response,status,HTTPException,Depends
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import engine,get_db
from sqlalchemy.orm import Session
from . import schemas,models,utils
from .routers import post,user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

while True:
    try:
       conn =psycopg2.connect(host='localhost',database='social-media-fastapi',user='postgres',password='4166',cursor_factory=RealDictCursor)
       cursor = conn.cursor()
       print("🟢 🟢 🟢 Database connection was successful! 🟢 🟢 🟢")
       break
    except Exception as error:
       print("🔴 🔴 🔴 Database connection was failed! 🔴 🔴 🔴")
       print("Error:",error)
       time.sleep(3)

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"message": "Hello World!"}
