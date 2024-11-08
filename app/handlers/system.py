from fastapi import FastAPI,HTTPException,status,Depends,Query
from app.handlers.base import BaseHandler
from app.handlers.security import JWTHandler, APIKeyHandler
from app.data_services.system import PVSystemService
from app.data_services.user import UserService
from app.data_services.location import LocationService
from app.data_services.inverter import InverterService
from app.data_services.solar_module import SolarModuleService
from app.models.user import User
from app.models.system import PVSystemModel,SolarArray
from app.models.result import ModelResult
from app.util.handler_return import ResponseModifier,ResponseWithMsg
from typing import Annotated

class PVSystemHandler(BaseHandler):
    def __init__(self,
                data_service:PVSystemService,
                user_service:UserService,
                location_service:LocationService,
                inverter_service:InverterService,
                solarMod_service:SolarModuleService,
                 app: FastAPI, 
                 apikey_handler: APIKeyHandler, 
                 oauth_handler: JWTHandler):
        super().__init__(tag="PVSystem", route="/pv_systems", app=app, apikey_handler=apikey_handler, oauth_handler=oauth_handler)
        self.__user_service=user_service
        self.__system_service=data_service
        self.__location_service=location_service
        self.__inverter_service=inverter_service
        self.__solarmodule_service=solarMod_service
        self.__resp_modifier=ResponseModifier[ModelResult]()


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
        
        @self.app.get(f'{self.route}/run_model',tags=[self.tag])
        async def run_model(
            token: Annotated[str | None, Depends(self.oauth_handler.token_from_request)],
            apikey: Annotated[str | None, Depends(self.apikey_handler.apikey_from_request)]
        )->ResponseWithMsg[ModelResult]:
            user=get_user(token=token,apikey=apikey)
            location=self.__location_service.get_location_ById(user.location_Id)
            weather=self.__location_service.get_current_weather(latitude=location.latitude,longitude=location.longitude)
            if weather is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="not able to get current weather data"
                )
            inverter=self.__inverter_service.get_inverter_ById(user.inverter_Id)
            module=self.__solarmodule_service.get_solar_module(user.solarModule_Id)
            
            system=self.__system_service.get_pv_system(user.system_Id)

            result=self.__system_service.run_model(
                location=location,
                weather=weather,
                module=module,
                inverter=inverter,
                system=system
            )

            
            if user.system_Id is None:
                return self.__resp_modifier.craft_with_msg(msg="You have not configure the system yet. Configure the system to store modelling result",
                                                             document=result)
            
            created=self.__system_service.store_result(system_id=user.system_Id,result=result)
            if not created:
                return self.__resp_modifier.craft_with_msg(msg="fail to record the result",document=result)
            

            return self.__resp_modifier.craft_with_msg(msg="the result is recorded",inserted=True,document=result)






            


