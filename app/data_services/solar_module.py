from pymongo.database import Database
from app.data_services.base import BaseService
from app.models.solar_module import SolarModuleModel

class SolarModuleService(BaseService[SolarModuleModel]):
    def __init__(self, collection_name: str, db: Database, default_solar_module: SolarModuleModel):
        super().__init__(collection_name, db)
        self.__default = default_solar_module
        

    def get_solar_module(self, module_Id: str) -> SolarModuleModel:
        if module_Id is None:
            return self.__default
        result = self.read_by_Id(module_Id)
        if result is not None:
            return SolarModuleModel(**result)
        return self.__default
