from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from database import init_db, get_session
from sqlmodel import Session, select, update
from model.users import User
from controller import user, order, file_upload

app = FastAPI(title="Restful API explanation")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(user.user_route)
app.include_router(order.order_route)
app.include_router(file_upload.file_upload_route)

