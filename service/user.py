from fastapi import HTTPException
from bcrypt import gensalt, hashpw, checkpw
from model.users import User
from model.profiles import Profile
from sqlmodel import Session, select, update
from jose import jwt
from sqlalchemy.orm import joinedload
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from service.mail import send_email
from datetime import datetime, timedelta, timezone
from model.user_sessions import UserSession

load_dotenv()



def hash_passwords(password: str):
    salt = gensalt(rounds=10)
    hashed_password = hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def compare_password(plain_password: str, hashed_password: str):
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')

    do_passwords_match = checkpw(plain_password.encode('utf-8'), hashed_password)
    return do_passwords_match


def register_user_service(user, session):
    v = user.model_dump()

    new_profile = Profile()
    new_profile.username = v["username"]
    new_profile.address = v["address"]

    
    new_user = User()
    
    hashed_password = hash_passwords(v["password"])
    new_user.full_name = v["full_name"]
    new_user.email = v["email"]
    new_user.password = hashed_password
    new_user.profile = new_profile
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return new_user




async def login_user(user, session: Session):
    u = User(**user.model_dump())
    user_from_db = select(User).where(User.email == u.email).options(joinedload(User.profile))
    result = session.exec(user_from_db).first()
    
    if result == None:
        raise HTTPException(status_code=404, detail="No user found")
    
    print("user.password", user.password)
    print("result.password", result.password)
    passwords_match = compare_password(user.password, result.password)
    
    if passwords_match == False:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    
    secret = os.getenv("AUTH_TOKEN")
    
    token = jwt.encode({
        "sub": str(result.id),
        "email": result.email,
        "role": "user",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=3)
    }, secret, algorithm="HS256")
    
    refresh_token = jwt.encode({
        "sub": str(result.id),
        "exp": datetime.now(timezone.utc) + timedelta(days=1)
    }, secret, algorithm="HS256")
    
    new_session = UserSession()
    
    new_session.user_id = result.id
    new_session.refresh_token = refresh_token
    
    session.add(new_session)
    session.commit()
    session.refresh(new_session)
    
    await send_email(
    emailDetails={
        "email": [result.email],
        "subject": "Welcome",
        "body": "Welcome to our backend",
    }
    )
    
    return {
        "message": "Logged in successfully",
        "access_token": token,
        "refresh_token": refresh_token,
        "user_with_profile": result.model_dump(exclude={"password"})
    }
        

def rotate_token(token: str, session: Session):
    try:
        secret = os.getenv("AUTH_TOKEN")
        user_details = jwt.decode(token=token, key=secret, algorithms="HS256")
    
        
        query = select(UserSession).where(UserSession.refresh_token == token, UserSession.user_id == user_details["sub"])
        
        user_session = session.exec(query).first()
        
        if user_session is None:
            raise HTTPException(status_code=400, detail="Session not found")
        
        user_from_db = select(User).where(User.id == user_details["sub"]).options(joinedload(User.profile))
        result = session.exec(user_from_db).first()
        
        if result == None:
            raise HTTPException(status_code=404, detail="No user found")
        
        token = jwt.encode({
            "sub": str(result.id),
            "email": result.email,
            "role": "user",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=3)
        }, secret, algorithm="HS256")
        
        refresh_token = jwt.encode({
            "sub": str(result.id),
            "exp": datetime.now(timezone.utc) + timedelta(days=1)
        }, secret, algorithm="HS256")
        
        
        user_session.refresh_token = refresh_token
        
        session.add(user_session)
        session.commit()
        session.refresh(user_session)
        
        return {
            "access_token": token,
            "refresh_token": refresh_token
        }
    
    except Exception as err:
        print(f"Error: {err}")
        raise HTTPException(status_code=403, detail="Invalid or expired token")
    

def update_user_service(user, id, session):
    initial_value = session.get(User, id)
    
    if not initial_value:
        raise HTTPException(status_code=404, detail="No user found")
    
    v = update(User).where(User.id == id).values(**user.model_dump())
    session.exec(v)
    session.commit()
    
    return session.get(User, id)

