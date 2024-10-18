from fastapi import FastAPI,HTTPException,status,Depends,Query
from app.handlers.base import BaseHandler
from app.handlers.security import JWTHandler, APIKeyHandler
from app.data_services.system import PVSystemService
from app.data_services.user import UserService
from app.models.user import User
from app.models.system import PVSystemModel,SolarArray
from typing import Annotated

class PVSystemHandler(BaseHandler):
    def __init__(self,
                data_service:PVSystemService,
                user_service:UserService,
                 app: FastAPI, 
                 apikey_handler: APIKeyHandler, 
                 oauth_handler: JWTHandler):
        super().__init__(tag="PVSystem", route="/pv_systems", app=app, apikey_handler=apikey_handler, oauth_handler=oauth_handler)
        self.__user_service=user_service
        self.__system_service=data_service


    def register_routes(self):
        def get_user(token: str, apikey: str) -> User:
            user = None
            if token is not None and self.oauth_handler.verify_token(token):
                user = self.oauth_handler.get_current_user(token)
            elif apikey is not None and self.apikey_handler.verify_api_key(apikey):
                user = self.apikey_handler.get_current_user(apikey)
            
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token and API key"
                )
            return user
        

        # Define your routes for PVSystem here
        @self.app.get(f"{self.route}",tags=[self.tag])
        async def get_pv_systems(
            token: Annotated[str | None, Depends(self.oauth_handler.token_from_request)],
            apikey: Annotated[str | None, Depends(self.apikey_handler.apikey_from_request)]
        )->PVSystemModel:
            user=get_user(token=token,apikey=apikey)
            return self.__system_service.get_pv_system(user.system_Id)

        @self.app.post(f"{self.route}",tags=[self.tag])
        async def upsert_pv_system(
            user:Annotated[User,Depends(self.oauth_handler.get_current_user)],
            array_config:SolarArray=None,
            name:str=Query(None,min_length=4),
            num_of_arrays:int=Query(1,gt=0)
        ):
            
            if user.system_Id is None:
                
                createdID=self.__system_service.create_system(name=name,
                                                              num_of_arrays=num_of_arrays,
                                                              arrayConfig=array_config)
                if createdID is None:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="user system creation fail"
                    )
                self.__user_service.update_systemId(user_email=user.email,systemId=createdID)
                return "user PV system is created"
                
            
            updated=self.__system_service.update_system(systemId=user.system_Id,
                                                name=name,
                                                num_of_array=num_of_arrays,
                                                arrayConfig=array_config)
            if not updated:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail='user system update fail'
                )
            
            return "user system is updated"

            


