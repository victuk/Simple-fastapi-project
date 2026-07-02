from fastapi import HTTPException
from bcrypt import gensalt, hashpw, checkpw
from model.users import User
from model.profiles import Profile
from sqlmodel import Session, select, update
from jose import jwt
from dotenv import load_dotenv
import os

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
    print("V value", v["email"])
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
    
    
    session.add(new_profile)
    session.commit()
    session.refresh(new_profile)
    return new_user


def login_user(user, session: Session):
    u = User(**user.model_dump())
    user_from_db = select(User).where(User.email == u.email)
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
        "role": "user"
    }, secret, algorithm="HS256")
    
    return {
        "message": "Logged in successfully",
        "token": token
    }
        
    

def update_user_service(user, id, session):
    initial_value = session.get(User, id)
    
    if not initial_value:
        raise HTTPException(status_code=404, detail="No user found")
    
    v = update(User).where(User.id == id).values(**user.model_dump())
    session.exec(v)
    session.commit()
    
    return session.get(User, id)

