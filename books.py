from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {
        'title': 'Title One',
        'author': 'Author One',
        'category': 'Science'
    },
    {
        'title': 'Title Two',
        'author': 'Author Two',
        'category': 'Math'
    },
    {
        'title': 'Title One',
        'author': 'Author Three',
        'category': 'History'
    },
    {
        'title': 'Title Four',
        'author': 'Author Two',
        'category': 'Science'
    },
    {
        'title': 'Title Three',
        'author': 'Author Three',
        'category': 'History'
    },
    {
        'title': 'Title Four',
        'author': 'Author Four',
        'category': 'Math'
    }
]


@app.get("/api/books")
async def read_all_books():
    return BOOKS


@app.get("/api/books/mybook")
async def read_my_book():
    return {'book': 'My favorite book'}


@app.get("/api/books/{book_title}")
async def read_book_by_title(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

    return {'message': 'Book Not Found'}


@app.get("/api/books/")
async def find_books_by_query_category(category: str):
    books = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books.append(book)
    return books


@app.get("/api/books/{book_author}/")
async def find_books_by_path_author_and_by_query_category(book_author: str, category: str):
    books = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get(
                'category').casefold() == category.casefold():
            books.append(book)
    return books
