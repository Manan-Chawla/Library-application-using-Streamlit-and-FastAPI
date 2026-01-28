from fastapi import FastAPI,Depends
from sqlmodel import Session,select
from db import get_session,engine,create_db_and_tables
from models import Book

app=FastAPI(title="Lib's api")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/books/",response_model=Book)
def create_book(book:Book,session:Session=Depends(get_session)):
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@app.get("/books/",response_model=list[Book])
def read_books(session:Session=Depends(get_session)):
    books=session.exec(select(Book)).all()
    return books

@app.get("/books/{book_id}",response_model=Book)
def getbook_id(book_id:int,session:Session=Depends(get_session)):
     book=session.get(Book,book_id)
     if not book:
         raise HTTPException(status_code=404,detail="Book not found")
     return book