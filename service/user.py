from fastapi import HTTPException
from bcrypt import gensalt, hashpw, checkpw
from model.users import User
from sqlmodel import Session, select, update

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
    new_user = User(**user.model_dump())
    
    hashed_password = hash_passwords(new_user.password)
    
    new_user.password = hashed_password
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def login_user(user, session: Session):
    u = User(**user.model_dump())
    user_from_db = select(User).where(User.email == u.email)
    result = session.exec(user_from_db).first()
    print("user.password", user.password)
    print("result.password", result.password)
    passwords_match = compare_password(user.password, result.password)
    return passwords_match
        
    

def update_user_service(user, id, session):
    initial_value = session.get(User, id)
    
    if not initial_value:
        raise HTTPException(status_code=404, detail="No user found")
    
    v = update(User).where(User.id == id).values(**user.model_dump())
    session.exec(v)
    session.commit()
    
    return session.get(User, id)

