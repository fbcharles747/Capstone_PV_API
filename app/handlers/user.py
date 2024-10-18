from fastapi import FastAPI,Form,HTTPException,status,Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated,Optional
from app.handlers.base import BaseHandler
from app.handlers.security import APIKeyHandler,JWTHandler
from app.data_services.user import UserService
from app.models.user import User
from pydantic import EmailStr

class UserHandler(BaseHandler):
    def __init__(self,data_service:UserService,
                 apikey_handler:APIKeyHandler,
                 oauth_handler:JWTHandler,
                 app:FastAPI):
        super().__init__(tag="User",route="/users",app=app,apikey_handler=apikey_handler,oauth_handler=oauth_handler)
        self.user_data_service=data_service
        
    
    def register_routes(self):
       
        @self.app.post(self.route,tags=[self.tag])
        async def sign_up(email:Annotated[EmailStr,Form()],password:Annotated[str,Form()]):
            status=self.user_data_service.sign_up(email=email,password=password)
            if status.acknowledged:
                return "user created"
            else:
                raise HTTPException(status_code=status.status_code,
                                    detail=status.message)
        
        @self.app.get(self.route+"/me",tags=[self.tag])
        async def get_current_user(user:Annotated[User,Depends(self.oauth_handler.get_current_user)])->User:
            return user
        
        @self.app.get(self.route+"/me/apikey",tags=[self.tag])
        async def get_my_apikey(user:Annotated[User,Depends(self.oauth_handler.get_current_user)])->str:
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="user not found"
                )
            return self.user_data_service.decrypt_apikey(user.encrypt_api_key)
        
        @self.app.put(self.route+"/me/apikey",tags=[self.tag])
        async def toggle_my_apikey(enable:bool,user:Annotated[User,Depends(self.oauth_handler.get_current_user)]):
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="user not found"
                )
            updated=self.user_data_service.toggle_apikey(user.email,enable=enable)
            if not updated:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="update fail"
                )
            return f"user apikey status change"
        
            
        
