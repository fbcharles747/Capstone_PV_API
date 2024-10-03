from app.handlers.base import BaseHandler
from app.data_services.location import LocationService
from app.handlers.security import APIKeyHandler,JWTHandler
from app.models.user import User
from fastapi import FastAPI,HTTPException,status,Depends
from typing import Annotated

class LocationHandler(BaseHandler):
    def __init__(self,data_service:LocationService,
                 apikey_handler:APIKeyHandler,
                 oauth_handler:JWTHandler,
                 tag:str,route:str,app:FastAPI):
        super().__init__(tag=tag,route=route,app=app,apikey_handler=apikey_handler,oauth_handler=oauth_handler)
        self.__location_service=data_service

    def register_routes(self):
        @self.app.post(self.route,tags=[self.tag])
        async def upsert_location(latitude:float,longitude:float,user:Annotated[User,Depends(self.oauth_handler.get_current_user)]):
            
            updated=self.__location_service.upsert_location(latitude=latitude,longitude=longitude,user_email=user.email)
            
            if not updated:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="location update fail"
                )
            return "user location is updated"
        
        
