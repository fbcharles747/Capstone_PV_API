from app.data_services.base import BaseService
from app.api_adaptor.google_map import GoogleMap_Adaptor
from app.api_adaptor.open_weather_map import OpenWeather_Adaptor
from app.api_adaptor.solcast_api import Solcast_Adaptor
from app.models.location import LocationModel
from app.models.user import User
from app.api_adaptor.aggregate_data import Weather_Data
from pymongo.database import Database


class LocationService(BaseService[LocationModel]):
    def __init__(self, default_location:LocationModel,collection_name: str, db: Database,
                 gmap_adaptor:GoogleMap_Adaptor,
                 open_weather_adaptor:OpenWeather_Adaptor,
                 solcast_adaptor:Solcast_Adaptor):
        super().__init__(collection_name, db)
        self.default=default_location
        self.__gmap_adaptor=gmap_adaptor
        self.__opweather_adptor=open_weather_adaptor
        self.__solcast_adaptor=solcast_adaptor
    
    def load_locationInfo(self,latitude:float,longitude:float)->LocationModel:
        tz=self.__gmap_adaptor.get_timezone(latitude=latitude,longitude=longitude)
        altitude=self.__gmap_adaptor.get_altitude(latitude=latitude,longitude=longitude)
        location=LocationModel(latitude=latitude,longitude=longitude,altitude=altitude,timezone=tz.timeZoneId)
        return location
    
    def create_location(self,latitude:float,longitude:float,name:str)->str|None:
        location=self.load_locationInfo(latitude=latitude,longitude=longitude)
        location.name=name
        locationID=self.create(location)
        return locationID

    
    def update_location(self,latitude:float,longitude:float,locationId:str,name:str)->bool:
        location=self.load_locationInfo(latitude=latitude,longitude=longitude)
        location.name=name
        result=self.update_ById(locationId,location.__dict__)
        return result
    
    
    def get_location_ById(self,id:str)->LocationModel:
        if id is None:
            return self.default
        result=self.read_by_Id(id=id)
        if result is not None:
            return LocationModel(**result)
        return self.default

    
    def get_current_weather(self,latitude:float,longitude)->Weather_Data|None:
        general,wind=self.__opweather_adptor.get_currentWeather(latitude,longitude)
        irradiance=self.__solcast_adaptor.get_current_irradiance(latitude=latitude,longitude=longitude)
        if irradiance is None:
            print(f"Not able to get irradiance data")
            return None
        if wind is None:
            print(f"not able to get wind data")
            return None
        if general is None:
            print(f"not able to get temperature data in general")
            return None
        
        return Weather_Data(**general.__dict__,**wind.to_dict(),**irradiance.to_dict_irradiance())

