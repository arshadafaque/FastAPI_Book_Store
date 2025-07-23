from pydantic import BaseModel,Field
import uuid
from datetime import datetime

class SignUp(BaseModel):
    username:str=Field(max_length=50)
    email:str=Field(max_length=50)
    first_name:str=Field(max_length=25)
    last_name:str=Field(max_length=25)
    password:str=Field(min_length=8,max_length=20)

class SignUpResponse(BaseModel):
    id:uuid.UUID
    username:str
    email:str
    first_name:str
    last_name:str
    is_verified:bool=False
    created_at:datetime
    updated_at:datetime

    class Config:
        from_attributes = True
        

class LoginData(BaseModel):
    email:str
    password:str