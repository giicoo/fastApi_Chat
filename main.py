from datetime import timedelta
from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pymongo import MongoClient
from sqlalchemy.orm import Session
from starlette import status
from app.chats import settings
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
import app.db as db
import app.auth as auth
import app.config as cfg
from app.routers import users, chats
from app.chats import chat

root = FastAPI()

root.include_router(users.router)
root.include_router(chats.router)
root.include_router(chat.router)

@root.on_event("startup")
def startup_db_client():
    root.mongodb_client = MongoClient(cfg.ATLAS_URI)
    root.database = root.mongodb_client[cfg.DB_NAME]

    root.manager =settings.ConnectionManager(root.database)
    print("Connected to the MongoDB database!")

@root.on_event("shutdown")
def shutdown_db_client():
    root.mongodb_client.close()

@root.get("/users/me/", response_model=db.schems.User)
async def read_users_me(
    current_user: Annotated[db.schems.User, Depends(auth.funcs.get_current_user)]
):
    return current_user

@root.get('/')
async def index(request: Request):
    return cfg.template.TemplateResponse('home.html', context={'request': request})