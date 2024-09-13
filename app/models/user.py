from pydantic import BaseModel

class User(BaseModel):
    email:str
    password:str|None=None
    api_key:str|None=None
    