from typing import Any, Dict
from pymongo.database import Database
from pymongo.results import UpdateResult
from app.data_services.base import BaseService
from app.models.inverter import InverterModel

class InverterService(BaseService):
    def __init__(self, collection_name: str, db: Database,default_inverter:InverterModel):
        super().__init__(collection_name, db)
        self.__default=default_inverter

    def upsert_inverter(self, user_email:str, inverter:InverterModel) -> UpdateResult:
        inverter.user_email=user_email
        return super().upsert({'user_email':user_email}, inverter)
    
    def get_inverter(self, user_email:str)->InverterModel:
        result=self.read({"user_email":user_email})
        if result is not None:
            return InverterModel(**result)
        return self.__default
    

    
