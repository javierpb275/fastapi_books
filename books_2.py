from fastapi import FastAPI

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
