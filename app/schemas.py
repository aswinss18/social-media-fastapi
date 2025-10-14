from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    description: str
    published: bool = True

class CreatePost(PostBase):
    pass
