
from pydantic import BaseModel
import uuid
from datetime import datetime,date

class Book(BaseModel):
    id:uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at:datetime
    updated_at:datetime

    model_config = {
        "from_attributes": True
    }
 


# class BookDetailModel(Book):
#     reviews: List[ReviewModel]
#     tags:List[TagModel]


class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str