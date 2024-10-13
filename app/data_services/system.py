from pymongo.database import Database
from app.data_services.base import BaseService
from app.models.system import PVSystemModel,SolarArray

class PVSystemService(BaseService[PVSystemModel]):
    def __init__(self, collection_name: str, db: Database, default_pv_system: PVSystemModel):
        super().__init__(collection_name, db)
        self.__default = default_pv_system

    def get_pv_system(self, system_Id: str) -> PVSystemModel:
        result = self.read_by_Id(system_Id)
        if result is not None:
            return PVSystemModel(**result)
        return self.__default
    
    def update_system(self,systemId:str,name:str|None,num_of_array:int,arrayConfig:SolarArray|None):
        field_to_update={}
        if name is not None:
            field_to_update.update({"name":name})

        if num_of_array >1:
            field_to_update.update({"num_of_array":num_of_array})
        
        if arrayConfig is not None:
            field_to_update.update({'array_config':arrayConfig})
        
        return self.update_ById(systemId,field_to_change=field_to_update)
    
    def create_system(self,name:str|None,num_of_arrays:int,arrayConfig:SolarArray|None):
        system=PVSystemModel()
        if name is not None:
            system.name=name
        if num_of_arrays > 1:
            system.num_of_array=num_of_arrays
        if arrayConfig is not None:
            system.array_config=arrayConfig
        return self.create(system)
    
        


    
    def run_pvsystem():
        pass


