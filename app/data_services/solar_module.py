from typing import Any, Dict
from pymongo.database import Database
from pymongo.results import UpdateResult
from app.data_services.base import BaseService
from app.models.solar_module import SolarModuleModel

class SolarModuleService(BaseService):
    def __init__(self, collection_name: str, db: Database, default_solar_module: SolarModuleModel):
        super().__init__(collection_name, db)
        self.__default = default_solar_module

    def upsert_solar_module(self, user_email: str, solar_module: SolarModuleModel) -> UpdateResult:
        solar_module.user_email = user_email
        return super().upsert({'user_email': user_email}, solar_module)

    def get_solar_module(self, user_email: str) -> SolarModuleModel:
        result = self.read({"user_email": user_email})
        if result is not None:
            return SolarModuleModel(**result)
        return self.__default
