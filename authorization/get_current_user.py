from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from dotenv import load_dotenv
import os
from typing import List
from model.users import User
from controller.user import RegistrationDetails

load_dotenv()

sec_scheme = HTTPBearer()

def get_current_user(value: HTTPAuthorizationCredentials = Depends(sec_scheme)):
    
    token = value.credentials
    scheme = value.scheme
    
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=400, detail="Invalid scheme")
    
    if token == None:
        raise HTTPException(status_code=404, detail="No token found")
    
    secret = os.getenv("AUTH_TOKEN")
    
    payload = jwt.decode(token, secret, algorithms="HS256")
    
    if secret == None or payload == None:
        raise HTTPException(status_code=500, detail="Invalid token or missing secret")
    
    return payload


class Role(RegistrationDetails):
    role: str

class CheckRole:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user: Role = Depends(get_current_user)):
        if current_user["role"] not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden")

        return current_user