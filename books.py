from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {
        "title": "Title One",
        "author": "Author One",
        "category": "Science"
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


@app.get("/api/books/by_author/{author}")
async def find_books_by_path_author(author: str):
    books = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books.append(book)
    return books


@app.get("/api/books/by_author/")
async def find_books_by_query_author(author: str):
    books = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
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


@app.post("/api/books/create_book")
async def create_book(book: dict = Body()):
    BOOKS.append(book)
    return book


@app.put("/api/books/update_book")
async def update_book(book: dict = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book.get('title').casefold():
            BOOKS[i] = book
            return BOOKS[i]
    return {'message': 'Book Not Found'}


@app.delete("/api/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            deleted_book = BOOKS.pop(i)
            return {"message": f"Book '{deleted_book['title']}' deleted"}
    return {'message': 'Book Not Found'}
