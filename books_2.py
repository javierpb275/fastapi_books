from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(title='id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)  # 0 - 5

    class Config:
        schema_extra = {
            'example': {
                'title': 'New Book',
                'author': 'New Author',
                'description': 'New Description',
                'rating': 5
            }
        }


BOOKS = [
    Book(1, 'Computer Science', 'Javier', 'Great book', 5),
    Book(2, 'FastAPI', 'Roby', 'Very nice book!', 5),
    Book(3, 'Lord of the rings', 'Tolkien', 'Really exciting', 4),
    Book(4, 'Harry Potter', 'J.K. Rowling', 'Amazing', 4),
    Book(5, 'Whatever', 'Pepe', 'It is ok...', 3),
    Book(6, 'Whatever 2', 'Pepe', 'Even worst than the first one', 2),
]


@app.get("/api/books")
async def read_all_books():
    return BOOKS


@app.post("/api/books")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))
    return new_book


def find_book_id(book: Book) -> Book:
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

