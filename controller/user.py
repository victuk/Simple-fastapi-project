from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from database import get_session
from sqlmodel import Session, select, update
from sqlalchemy.orm import joinedload
from model.users import User
from model.profiles import Profile
from service.user import register_user_service, update_user_service, login_user

user_route = APIRouter(
    prefix="/users",
    tags=["users"]
)

class LoginDetails(BaseModel):
    email: str
    password: str

class RegistrationDetails(LoginDetails):
    full_name: str
    username: str
    address: str


@user_route.get("/")
def user_list(session: Session = Depends(get_session)):
    v = select(User)
    users = session.exec(v).all()
    return users

@user_route.get("/{id}")
def user_by_position(id: str, session: Session = Depends(get_session)):
    user = session.get(User, id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@user_route.post("/register")
def register_user(reg_details: RegistrationDetails, session: Session = Depends(get_session)):
    return register_user_service(reg_details, session)

@user_route.post("/login")
def login(login_details: LoginDetails, session: Session = Depends(get_session)):
    return login_user(login_details, session)


@user_route.put("{id}")
def update_user(reg_details: RegistrationDetails, id: str, session: Session = Depends(get_session)):
    return update_user_service(reg_details, id, session)

@user_route.delete("{id}")
def remove_user(id: str, session: Session = Depends(get_session)):
    user = session.get(User, id)
    session.delete(user)
    session.commit()
    return "Deleted Successfully"
