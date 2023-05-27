from typing import Optional

from fastapi import FastAPI, Query
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
async def read_all_books(
    title: Optional[str] = Query(None, min_length=1, alias="book_title"),
    author: Optional[str] = Query(None, min_length=1),
    description: Optional[str] = Query(None, min_length=1),
    rating: Optional[int] = Query(None, ge=0, le=5),
    sort_by: Optional[str] = Query(None, regex=r"^(id|title|author|rating)$"),
    sort_order: Optional[str] = Query("asc", regex=r"^(asc|desc)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    filtered_books = []
    for book in BOOKS:
        if (
            (title is None or book.title.lower().find(title.lower()) != -1)
            and (author is None or book.author.lower().find(author.lower()) != -1)
            and (description is None or book.description.lower().find(description.lower()) != -1)
            and (rating is None or book.rating == rating)
        ):
            filtered_books.append(book)

    # Sorting
    if sort_by:
        filtered_books.sort(key=lambda b: getattr(b, sort_by), reverse=(sort_order == "desc"))

    # Pagination
    total_books = len(filtered_books)
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_books = filtered_books[start_index:end_index]

    return {
        "total_books": total_books,
        "books": paginated_books
    }


@app.get("/api/books/{id}")
async def read_book(id: int):
    for book in BOOKS:
        if book.id == id:
            return book
    return {'message': 'Book Not Found'}


@app.post("/api/books")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))
    return new_book


def find_book_id(book: Book) -> Book:
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
