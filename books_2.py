from typing import Optional
from datetime import date

from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    def __init__(
            self,
            id: int,
            search: str,
            title: str,
            author: str,
            description: str,
            rating: int,
            published_date: date
    ):
        self.id = id
        self.search = search
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(title='id is not needed')
    search: Optional[str] = Field(title='search is just for filtering')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)  # 0 - 5
    published_date: Optional[date] = Field(title='date when the book was published')

    class Config:
        schema_extra = {
            'example': {
                'title': 'New Book',
                'author': 'New Author',
                'description': 'New Description',
                'rating': 5,
                'published_date': '2023-05-28'
            }
        }


BOOKS = [
    Book(1, 'Computer Science Javier 5', 'Computer Science', 'Javier', 'Great book', 5, date(2021, 1, 1)),
    Book(2, 'FastAPI Roby 5', 'FastAPI', 'Roby', 'Very nice book!', 5, date(2022, 2, 2)),
    Book(3, 'Lord of the rings J.R.R. Tolkien 4', 'Lord of the rings', 'J.R.R. Tolkien', 'Really exciting', 4, date(2023, 3, 3)),
    Book(4, 'Harry Potter J.K. Rowling 4', 'Harry Potter', 'J.K. Rowling', 'Amazing', 4, date(2024, 4, 4)),
    Book(5, 'Whatever Pepe 3', 'Whatever', 'Pepe', 'It is ok...', 3, date(2025, 5, 5)),
    Book(6, 'Whatever 2 Pepe 2', 'Whatever 2', 'Pepe', 'Even worse than the first one', 2, date(2026, 6, 6)),
]


@app.get("/api/books", status_code=status.HTTP_200_OK)
async def read_all_books(
    title: Optional[str] = Query(None, min_length=1, alias="book_title"),
    search: Optional[str] = Query(None, min_length=1),
    author: Optional[str] = Query(None, min_length=1),
    description: Optional[str] = Query(None, min_length=1),
    rating: Optional[int] = Query(None, ge=0, le=5),
    published_date: Optional[date] = Query(None),
    sort_by: Optional[str] = Query("id", regex=r"^(id|title|author|rating|published_date)$"),
    sort_order: Optional[str] = Query("asc", regex=r"^(asc|desc)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    filtered_books = []
    for book in BOOKS:
        if (
            (title is None or book.title.lower().find(title.lower()) != -1)
            and (search is None or book.search.lower().find(search.lower()) != -1)
            and (author is None or book.author.lower().find(author.lower()) != -1)
            and (description is None or book.description.lower().find(description.lower()) != -1)
            and (rating is None or book.rating == rating)
            and (published_date is None or book.published_date == published_date)
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
        "books": [
            remove_keys(book.__dict__, "search")
            for book in paginated_books
        ]
    }


@app.get("/api/books/{id}", status_code=status.HTTP_200_OK)
async def read_book(id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == id:
            response = remove_keys(book.__dict__, "search")
            return response
    raise HTTPException(status_code=404, detail='Book Not Found')


@app.post("/api/books", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    if book_request.published_date is None:
        book_request.published_date = date.today()
    book = Book(**book_request.dict())
    new_book = set_book_search(set_book_id(book))
    BOOKS.append(new_book)
    response = remove_keys(new_book.__dict__, "search")
    return response


@app.put("/api/books/{id}", status_code=status.HTTP_200_OK)
async def update_book(book_request: BookRequest, id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id:
            book_data = book_request.dict()
            book_data["id"] = id
            if book_request.published_date is None:
                book_data["published_date"] = BOOKS[i].published_date
            book = Book(**book_data)
            BOOKS[i] = set_book_search(book)
            response = remove_keys(BOOKS[i].__dict__, "search")
            return response
    raise HTTPException(status_code=404, detail='Book Not Found')


@app.delete("/api/books/{id}", status_code=status.HTTP_200_OK)
async def delete_book(id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id:
            book_deleted = BOOKS.pop(i)
            response = remove_keys(book_deleted.__dict__, "search")
            return response
    raise HTTPException(status_code=404, detail='Book Not Found')


def set_book_id(book: Book) -> Book:
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


def set_book_search(book: Book) -> Book:
    book.search = f"{book.title} {book.author} {book.rating}"
    return book


def remove_keys(dictionary: dict, *keys_to_remove: str) -> dict:
    new_dictionary: dict = dictionary.copy()
    for key in keys_to_remove:
        new_dictionary.pop(key, None)
    return new_dictionary
