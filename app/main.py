from fastapi import FastAPI,Depends

from .database import engine,get_db
from sqlalchemy.orm import Session
from . import models
from .routers import post,user,auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"message": "Hello World!"}
