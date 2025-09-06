from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating:Optional[int]=None

@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.get("/posts")
def get_posts():
    return {"data": "this is your posts!"}

@app.post("/createposts")
def create_posts(new_post: Post):
    return {
        "message": "Successfully created post!",
        "data": new_post,
    
    }
