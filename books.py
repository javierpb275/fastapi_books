from fastapi import FastAPI

app = FastAPI()


@app.get("/api/hello")
def first_api():
    return {"message": "Hello World"}
