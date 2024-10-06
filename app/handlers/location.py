from app.handlers.base import BaseHandler
from app.data_services.location import LocationService
from app.handlers.security import APIKeyHandler,JWTHandler
from app.models.user import User
from app.models.location import LocationModel
from fastapi import FastAPI,HTTPException,status,Depends
from typing import Annotated
from app.api_adaptor.aggregate_data import Weather_Data

class LocationHandler(BaseHandler):
    def __init__(self,data_service:LocationService,
                 apikey_handler:APIKeyHandler,
                 oauth_handler:JWTHandler,
                 tag:str,route:str,app:FastAPI):
        super().__init__(tag=tag,route=route,app=app,apikey_handler=apikey_handler,oauth_handler=oauth_handler)
        self.__location_service=data_service

    def register_routes(self):

        def get_user(token:str,apikey:str)->User:
            user=None
            if token is not None and self.oauth_handler.verify_token(token):
                user=self.oauth_handler.get_current_user(token)
            elif apikey is not None and self.apikey_handler.verify_api_key(apikey):
                user=self.apikey_handler.get_current_user(apikey)
            
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token and apikey"
                )
            return user
        
        @self.app.post(self.route,tags=[self.tag])
        async def upsert_location(latitude:float,longitude:float,user:Annotated[User,Depends(self.oauth_handler.get_current_user)]):
            
            updated=self.__location_service.upsert_location(latitude=latitude,longitude=longitude,user_email=user.email)
            
            if not updated:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="location update fail"
                )
            return "user location is updated"
        
        @self.app.get(f'/configured-location',tags=[self.tag])
        async def get_configured_location(
            token:Annotated[str|None,Depends(self.oauth_handler.token_from_request)],
            apikey:Annotated[str|None,Depends(self.apikey_handler.apikey_from_request)]
        )->LocationModel:
            
            user=get_user(token=token,apikey=apikey)

            location=self.__location_service.get_location_by_UserEmail(user.email)
            if location is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="location not found"
                )
            return location
        
        @self.app.get(f'/configured-location/weather',tags=[self.tag])
        async def get_current_weather(
            token:Annotated[str|None,Depends(self.oauth_handler.token_from_request)],
            apikey:Annotated[str|None,Depends(self.apikey_handler.apikey_from_request)]
        )->Weather_Data:
            
            user=get_user(token=token,apikey=apikey)
            
            location=self.__location_service.get_location_by_UserEmail(user.email)
            if location is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="location not found"
                )
            weather=self.__location_service.get_current_weather(latitude=location.latitude,longitude=location.longitude)
            if weather is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail='something wrong about weather data'
                )
            return weather
            
            
            
            
        
        
