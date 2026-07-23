
from sqlmodel import SQLModel, Field

class VerifyEmail(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    user_id: str
    otp: str
    token: str