from app.data_services.base import BaseService
from app.api_adaptor.google_map import GoogleMap_Adaptor
from app.models.location import LocationModel
from pymongo.database import Database


class LocationService(BaseService):
    def __init__(self ,collection_name: str, db: Database,gmap_adaptor:GoogleMap_Adaptor):
        super().__init__(collection_name, db)
        self.__gmap_adaptor=gmap_adaptor

    def upsert_location(self,latitude:float,longitude:float, user_email:str)->bool:
        tz=self.__gmap_adaptor.get_timezone(latitude=latitude,longitude=longitude)
        altitude=self.__gmap_adaptor.get_altitude(latitude=latitude,longitude=longitude)
        location=LocationModel(latitude=latitude,longitude=longitude,altitude=altitude,timezone=tz.timeZoneId,user_email=user_email)
        result=self.upsert(filter={"user_email":user_email},update=location.__dict__)
        return result.acknowledged

