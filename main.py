import uvicorn
from fastapi import FastAPI, Request, Header, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from uuid import uuid4
from typing import Annotated
import json
app = FastAPI() #Создали API
templates = Jinja2Templates(directory= "Templates") #Указали, где находятся html файлы
app.mount("/static", StaticFiles(directory= "static"), name = "static") #Указали, где находятся статические файлы(картинки и т.д.)

with open("Books.json", 'r', encoding="utf8") as jsonfile:
    db = json.load(jsonfile)

class Book:
    def __init__(self, bookID, title, authors, isbn, isbn13, language_code, num_pages, text_reviews_count, publication_date, publisher):
        self.bookID:int = bookID
        self.title:str = title
        self.authors:str = authors
        self.average_rating:int = 0
        self.isbn:str = isbn
        self.isbn13:str = isbn13
        self.language_code:str = language_code
        self.num_pages:int = num_pages
        self.ratings_count:int = 0
        self.text_reviews_count:int = text_reviews_count
        self.publication_date:str = publication_date
        self.publisher:str = publisher

book_db = []
for r in db:
    book_db.append(Book(r["bookID"], r["title"], r["authors"], r["isbn"], r["isbn13"], r["language_code"], r["num_pages"], r["text_reviews_count"], r["publication_date"], r["publisher"]))


@app.get("/", response_class= HTMLResponse) #Запрос на получение информации (отправляем get запрос)
async def read_root(request: Request): #async превращает функцию в асинхронную, т.е. функцию которая может ждать
    return templates.TemplateResponse(request= request, name= "index.html")


@app.get("/books", response_class= HTMLResponse)
async def list_books(request: Request, hx_request: Annotated[str | None, Header()] = None):
    if hx_request:
        return templates.TemplateResponse(request= request, name= "book_list.html", context= {"books": book_db})
    return JSONResponse(content= jsonable_encoder(book_db))


@app.get("/books/add", response_class= HTMLResponse)
async def add_book_form(request: Request, hx_request: Annotated[str | None, Header()] = None):
    return templates.TemplateResponse(request= request, name="process_book.html", context= {"title": "Add New Book"})


@app.post("/books/add", response_class= HTMLResponse)
async def add_book(request: Request, bookID: Annotated[int, Form()], title: Annotated[str, Form()], authors: Annotated[str, Form()], isbn: Annotated[str, Form()], isbn13: Annotated[str, Form()], language_code: Annotated[str, Form()], num_pages: Annotated[int, Form()], text_reviews_count: Annotated[int, Form()], publication_date: Annotated[str, Form()], publisher: Annotated[str, Form()]):
    #db_len = len(book_db) + 1
    #print(db_len)
    book_db.append(Book(bookID, title, authors, isbn, isbn13, language_code, num_pages, text_reviews_count, publication_date, publisher))
    #print(book_db[-1].title)
    return templates.TemplateResponse(request= request, name= "book_list.html", context= {"books": book_db})


@app.put("/books/update/{book_id}", response_class=HTMLResponse)
async def update_book(request: Request, bookID: Annotated[int, Form()], title: Annotated[str, Form()], authors: Annotated[str, Form()], isbn: Annotated[str, Form()], isbn13: Annotated[str, Form()], language_code: Annotated[str, Form()], num_pages: Annotated[int, Form()], text_reviews_count: Annotated[int, Form()], publication_date: Annotated[str, Form()], publisher: Annotated[str, Form()]):
    for index, book in enumerate(book_db):
        if book.bookID == bookID:
            book.title = title
            book.authors = authors
            book.isbn = isbn
            book.isbn13 = isbn13
            book.language_code = language_code
            book.num_pages = num_pages
            book.text_reviews_count = text_reviews_count
            book.publication_date = publication_date
            book.publisher = publisher
            break
    return templates.TemplateResponse(request= request, name= "book_list.html", context= {"books": book_db})
    

@app.get("/books/update", response_class= HTMLResponse)
async def update_book_form(request: Request, hx_request: Annotated[str | None, Header()] = None):
    return templates.TemplateResponse(request= request, name="process_book.html", context= {"title": "Update Book"})


@app.delete("/books/delete/{book_id}", response_class= HTMLResponse)
async def delete_book(request: Request, book_id: str):
    for index, book in enumerate(book_db):
        if str(book.bookID) == book_id:
            del book_db[index]
            break
    return templates.TemplateResponse(request= request, name="book_list.html", context= {"books": book_db})


@app.post("/search", response_class= HTMLResponse)
async def search(request: Request, search: Annotated[str, Form()]):
    search_res = []
    for index, book in enumerate(book_db):
        if str(book.title) == search:
            search_res.append(book)
        if str(book.authors) == search:
            search_res.append(book)
        if str(book.publication_date).split("/")[-1] == str(search):
            search_res.append(book)
    return templates.TemplateResponse(request= request, name="book_list.html", context= {"books": search_res})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=20000)