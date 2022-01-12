from typing import  List
from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
import fastapi
from fastapi.param_functions import Body
from starlette.status import HTTP_404_NOT_FOUND
from random import randrange
from .utils import hash
from .routers import posts, users, auth, vote


# from sqlalchemy import engine
from sqlalchemy.orm import Session
from . import models
from .database import Base, engine, get_db
from . import schemas

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

my_posts = [{"title": "title 1","content" : "new content", "id": 1}, {"title": "title 21","content" : "new fresh content", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/') 
def root():
    return {"message" : "Hello world!"}



