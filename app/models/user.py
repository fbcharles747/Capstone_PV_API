from pydantic import BaseModel,EmailStr

class User(BaseModel):
    email:EmailStr
    password:str|None=None
    encrypt_api_key:str|None=None
    hashed_api_key:str|None=None
    api_key_enable:bool=False

    def __init__(self,**kwarg):
        super().__init__(**kwarg)
    
    