from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

class TextRequest(BaseModel):
    text: str


class ItemList(BaseModel):
    ministers: list[str]
    
class MinisterRequest(BaseModel):
    minister: str
    
class MinisterInput(BaseModel):
    minister: str
    constituency: str
    