from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()

class Post(BaseModel):
    title: str
    description: str
    published: bool = True

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

my_posts = [{"title": "first post", "content": "this is my first post", "id": 1}, {"title": "second post", "content": "this is my second post", "id": 2}]    


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i        
@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts= cursor.fetchall()
    return {"data": posts} 

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    cursor.execute("""INSERT INTO posts (title,description,published) VALUES (%s,%s,%s) RETURNING *""",
                   (new_post.title,new_post.description,new_post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {
        "message": "Successfully created post!",
        "data": new_post,    
    }

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return {"data": post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, updated_post: Post):
    cursor.execute("""UPDATE posts SET title=%s, description=%s, published=%s WHERE id = %s RETURNING *""",(updated_post.title,updated_post.description,updated_post.published,id))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    return {"message": "Successfully updated post!","data": post}