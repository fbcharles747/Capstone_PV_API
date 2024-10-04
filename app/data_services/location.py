from app.data_services.base import BaseService
from app.api_adaptor.google_map import GoogleMap_Adaptor
from app.api_adaptor.open_weather_map import OpenWeather_Adaptor
from app.api_adaptor.solcast_api import Solcast_Adaptor
from app.models.location import LocationModel
from app.api_adaptor.aggregate_data import Weather_Data
from pymongo.database import Database


class LocationService(BaseService):
    def __init__(self ,collection_name: str, db: Database,
                 gmap_adaptor:GoogleMap_Adaptor,
                 open_weather_adaptor:OpenWeather_Adaptor,
                 solcast_adaptor:Solcast_Adaptor):
        super().__init__(collection_name, db)
        self.__gmap_adaptor=gmap_adaptor
        self.__opweather_adptor=open_weather_adaptor
        self.__solcast_adptor=solcast_adaptor

    def upsert_location(self,latitude:float,longitude:float, user_email:str)->bool:
        tz=self.__gmap_adaptor.get_timezone(latitude=latitude,longitude=longitude)
        altitude=self.__gmap_adaptor.get_altitude(latitude=latitude,longitude=longitude)
        location=LocationModel(latitude=latitude,longitude=longitude,altitude=altitude,timezone=tz.timeZoneId,user_email=user_email)
        result=self.upsert(filter={"user_email":user_email},update=location.__dict__)
        return result.acknowledged
    
    def get_location_by_UserEmail(self,email:str)->LocationModel|None:
        result=self.read({"user_email":email})
        if result is not None:
            return LocationModel(**result)
        return result
    
    def get_current_weather(self,latitude:float,longitude)->Weather_Data|None:
        general,wind=self.__opweather_adptor.get_currentWeather(latitude,longitude)
        irradiance=self.__solcast_adptor.get_current_irradiance(latitude,longitude)
        if irradiance is None:
            print(f"Not able to get irradiance data")
            return None
        if wind is None:
            print(f"not able to get wind data")
            return None
        if general is None:
            print(f"not able to get temperature data in general")
            return None
        
        
        return Weather_Data(**general.__dict__,**wind.to_dict(),**irradiance.__dict__)

