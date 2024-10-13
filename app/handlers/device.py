from app.handlers.base import BaseHandler
from app.data_services.inverter import InverterService
from app.data_services.solar_module import SolarModuleService
from app.data_services.user import UserService
from app.handlers.security import APIKeyHandler, JWTHandler
from app.models.user import User
from app.models.inverter import InverterModel
from app.models.solar_module import SolarModuleModel
from fastapi import FastAPI, HTTPException, status, Depends
from typing import Annotated
from app.api_adaptor.aggregate_data import Weather_Data  # If needed

class DeviceHandler(BaseHandler):
    def __init__(self, 
                 inverter_service:InverterService,
                 module_service:SolarModuleService,
                 user_service: UserService,
                 apikey_handler: APIKeyHandler,
                 oauth_handler: JWTHandler,
                 app: FastAPI):
        super().__init__(tag="Device", route='/devices', app=app, apikey_handler=apikey_handler, oauth_handler=oauth_handler)
        self.__inverter_service=inverter_service
        self.__module_service=module_service
        self.__user_service = user_service

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
        
        @self.app.post(f"{self.route}/inverters", tags=[self.tag])
        async def upsert_inverter(inverter: InverterModel,  
                                 user: Annotated[User, Depends(self.oauth_handler.get_current_user)]):
            if user.inverter_Id is None:
                deviceId = self.__inverter_service.create(inverter)
                if deviceId is not None:
                    self.__user_service.update_inverterId(user_email=user.email,inverterId=deviceId)
                    return "User inverter is created"
                else:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Inverter creation failed"
                    )

            updated = self.__inverter_service.update_ById(id=user.inverter_Id,field_to_change=inverter.__dict__)
            
            if not updated:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="inverter update failed"
                )
            return "User inverter is updated"
        
            

        @self.app.get(f'{self.route}/configured-inverter', tags=[self.tag])
        async def get_configured_inverter(
            token: Annotated[str | None, Depends(self.oauth_handler.token_from_request)],
            apikey: Annotated[str | None, Depends(self.apikey_handler.apikey_from_request)]
        ) -> InverterModel:
            
            user = get_user(token=token, apikey=apikey)

            device = self.__inverter_service.get_inverter_ById(user.inverter_Id)
            if device is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Inverter not found"
                )
            return device
        
        @self.app.delete(f'{self.route}/configured-inverter',tags=[self.tag])
        async def delete_configured_inverter(
            user: Annotated[User, Depends(self.oauth_handler.get_current_user)]
        ):
            if user.inverter_Id is not None:  
                self.__user_service.update_inverterId(user_email=user.email,inverterId=None)  
                deleted=self.__inverter_service.delete_byId(user.inverter_Id)
                if not deleted:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="inverter deletion failed"
                    )
                return "inverter is deleted"
            return "user have no configured inverter"
        
        @self.app.post(f"{self.route}/solar_modules", tags=[self.tag])
        async def upsert_solar_module(module: SolarModuleModel,  
                                 user: Annotated[User, Depends(self.oauth_handler.get_current_user)]):
            if user.solarModule_Id is None:
                deviceId = self.__module_service.create(module)
                if deviceId is not None:
                    self.__user_service.update_moduleId(user_email=user.email,moduleId=deviceId)
                    return "module is created"
                else:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="module creation failed"
                    )

            updated = self.__module_service.update_ById(user.solarModule_Id,module.__dict__)
            
            if not updated:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="module update failed"
                )
            return "User module is updated"
        
        @self.app.get(f'{self.route}/configured-solar_modules', tags=[self.tag])
        async def get_configured_inverter(
            token: Annotated[str | None, Depends(self.oauth_handler.token_from_request)],
            apikey: Annotated[str | None, Depends(self.apikey_handler.apikey_from_request)]
        ) -> SolarModuleModel:
            
            user = get_user(token=token, apikey=apikey)

            device = self.__module_service.get_solar_module(user.solarModule_Id)
            if device is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="module not found"
                )
            return device
        
        @self.app.delete(f'{self.route}/configured-solar_modules',tags=[self.tag])
        async def delete_module(
            user: Annotated[User, Depends(self.oauth_handler.get_current_user)]
        ):
            if user.solarModule_Id is not None:
                self.__user_service.update_moduleId(user_email=user.email,moduleId=None)
                deleted=self.__module_service.delete_byId(user.solarModule_Id)
                if not deleted:
                        raise HTTPException(
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="inverter deletion failed"
                        )
                
                return "user module is deleted"
            return "user has no configured module"

        
