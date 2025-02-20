from pydantic import BaseModel,EmailStr
from app.models.cache_data import CacheData
from datetime import datetime

class User(BaseModel):
    email:EmailStr
    password:str|None=None
    encrypt_api_key:str|None=None
    hashed_api_key:str|None=None
    api_key_enable:bool=False
    location_Id:str|None=None
    location_updatedAt:datetime|None=None
    weather_updatedAt:datetime|None=None
    inverter_Id:str|None=None
    solarModule_Id:str|None=None
    system_Id:str|None=None
    cached:CacheData|None=CacheData()
    

    def __init__(self,**kwarg):
        super().__init__(**kwarg)
    
    