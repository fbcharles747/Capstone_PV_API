from pymongo.database import Database
from datetime import datetime,timezone
from app.data_services.base import BaseService
from app.models.system import PVSystemModel,SolarArray
from app.models.inverter import InverterModel
from app.models.solar_module import SolarModuleModel
from app.models.location import LocationModel
from app.models.result import ModelResult
from app.api_adaptor.aggregate_data import Weather_Data
from app.api_adaptor.elastic_search import EsAdaptor
from elasticsearch import Elasticsearch



import app.api_adaptor.pvlib_util as pvlib_adaptor

class PVSystemService(BaseService[PVSystemModel]):
    def __init__(self, collection_name: str, db: Database, default_pv_system: PVSystemModel,es_client:Elasticsearch):
        super().__init__(collection_name, db)
        self.__default = default_pv_system
        self.__esAdaptor=EsAdaptor[ModelResult](client=es_client)

    def get_pv_system(self, system_Id: str) -> PVSystemModel:
        if system_Id is None:
            return self.__default
        
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
            field_to_update.update({'array_config':arrayConfig.model_dump()})
        
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
    
    
    def run_model(self,location:LocationModel,weather:Weather_Data,module:SolarModuleModel,inverter:InverterModel,system:PVSystemModel)->ModelResult:
        
        single_array_result=pvlib_adaptor.run_model(
            location=location,
            weather=weather,
            module=module,
            inverter=inverter,
            system=system
        )
        result=ModelResult(single_array_status=single_array_result)
        result.single_array_status=single_array_result
        result.system_dc_power=system.num_of_array * single_array_result.p_mp
        result.system_ac_power=result.system_dc_power * inverter.Efficiency
        result.time_stamp=datetime.now(tz=timezone.utc)
        result.calendar_year=result.time_stamp.year
        result.month=result.time_stamp.month
        result.day_of_month= result.time_stamp.day


        return result
    
    def store_result(self,system_id:str,result:ModelResult)->bool:
        return self.__esAdaptor.insert(index=system_id,document=result)
    


