from pydantic import BaseModel,EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    description: str
    published: bool = True

class CreatePost(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass