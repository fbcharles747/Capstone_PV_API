from pydantic import BaseModel,EmailStr

class User(BaseModel):
    email:EmailStr
    password:str|None=None
    api_key:str

    
    