from pymongo.database import Database
from app.data_services.base import BaseService
from app.models.inverter import InverterModel

class InverterService(BaseService[InverterModel]):
    def __init__(self, collection_name: str, db: Database,default_inverter:InverterModel):
        super().__init__(collection_name, db)
        self.__default=default_inverter

    
    
    def get_inverter_ById(self, inverter_Id:str)->InverterModel:
        result=self.read_by_Id(inverter_Id)
        if result is not None:
            return InverterModel(**result)
        return self.__default
    

    
