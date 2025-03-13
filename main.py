from fastapi import FastAPI, Request, Header, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from uuid import uuid4
from typing import Annotated
app = FastAPI() #Создали API
templates = Jinja2Templates(directory= "Templates") #Указали, где находятся html файлы
app.mount("/static", StaticFiles(directory= "static"), name = "static") #Указали, где находятся статические файлы(картинки и т.д.)

class Book:
    def __init__(self, title, author, isbn, language_code, num_pages, publication_date, publisher):
        self.bookID = uuid4()
        self.title:str = title
        self.author:str = author
        self.average_rating:int = 0
        self.isbn:str = isbn
        self.language_code:str = language_code
        self.num_pages:int = num_pages
        self.ratings_count:int = 0
        self.publication_date:str = publication_date
        self.publisher:str = publisher

fake_db = [Book("Harry Potter and the Half-Blood Prince (Harry Potter  #6)", "J.K. Rowling", "0439785960", "eng", 652, "9/16/2006", "Scholastic Inc."),
           Book("The Power of One: The Solo Play for Playwrights  Actors  and Directors", "Louis E. Catron", "0325001537", "eng", 240, "2/7/2000", "Heinemann Drama"),
           Book("Dinner with Anna Karenina", "Gloria Goldreich", "0778322270", "eng", 360, "1/28/2006", "Mira Books")]

@app.get("/", response_class= HTMLResponse) #Запрос на получение информации (отправляем get запрос)
async def read_root(request: Request): #async превращает функцию в асинхронную, т.е. функцию которая может ждать
    return templates.TemplateResponse(request= request, name= "index.html")


@app.get("/books", response_class= HTMLResponse)
async def list_books(request: Request, hx_request: Annotated[str | None, Header()] = None):
    if hx_request:
        return templates.TemplateResponse(request= request, name= "book_list.html", context= {"books": fake_db})
    return JSONResponse(content= jsonable_encoder(fake_db))


@app.get("/books/add", response_class= HTMLResponse)
async def add_book_form(request: Request, hx_request: Annotated[str | None, Header()] = None):
    return templates.TemplateResponse(request= request, name="add_book.html")


@app.post("/books/add", response_class= HTMLResponse)
async def add_book(request: Request, title: Annotated[str, Form()], author: Annotated[str, Form()], isbn: Annotated[str, Form()], language_code: Annotated[str, Form()], num_pages: Annotated[int, Form()], publication_date: Annotated[str, Form()], publisher: Annotated[str, Form()]):
    fake_db.append(Book(title, author, isbn, language_code, num_pages, publication_date, publisher))
    print(fake_db[-1].title)
    return templates.TemplateResponse(request= request, name= "book_list.html", context= {"books": fake_db})


@app.put("/books/update/{book_id}", response_class=HTMLResponse)
async def update_book(request: Request, book_id:str, title: Annotated[str, Form()], author: Annotated[str, Form()], isbn: Annotated[str, Form()], language_code: Annotated[str, Form()], num_pages: Annotated[int, Form()], publication_date: Annotated[str, Form()], publisher: Annotated[str, Form()]):
    for index, book in enumerate(fake_db):
        if str(book.bookID) == book_id:
            book.title = title
            book.author = author
            book.isbn = isbn
            book.language_code = language_code
            book.num_pages = num_pages
            book.publication_date = publication_date
            book.publisher = publisher
            break
    return templates.TemplateResponse(request= request, name= "book_list.html", context= {"books": fake_db})
    

@app.get("/books/update", response_class= HTMLResponse)
async def update_book_form(request: Request, hx_request: Annotated[str | None, Header()] = None):
    return templates.TemplateResponse(request= request, name="add_book.html")


@app.delete("/books/delete/{book_id}", response_class= HTMLResponse)
async def delete_book(request: Request, book_id: str):
    for index, book in enumerate(fake_db):
        if str(book.bookID) == book_id:
            del fake_db[index]
            break
    return templates.TemplateResponse(request= request, name="book_list.html", context= {"books": fake_db})


'''def get_full_name(firstname: str, lastname: str)->str: #пример создания функции
    return f"{firstname} {lastname}"'''