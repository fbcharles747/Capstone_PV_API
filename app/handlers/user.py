from fastapi import FastAPI,Form,HTTPException,status
from typing import Annotated
from app.handlers.base import BaseHandler
from app.data_services.user import UserService
from app.models.user import User
from pydantic import EmailStr

class UserHandler(BaseHandler):
    def __init__(self,data_service:UserService,tag:str,route:str,app:FastAPI):
        super().__init__(tag=tag,route=route,app=app)
        self.user_data_service=data_service
    
    def register_routes(self):
        @self.app.get(self.route+"/{email}",tags=[self.tag])
        async def get_user(email:str):
            user=self.user_data_service.read({"email":email})
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"user with email ({email}) cannot be found")
            return user
        
        @self.app.post(self.route,tags=[self.tag])
        async def sign_up(email:Annotated[EmailStr,Form()],password:Annotated[str,Form()]):
            status=self.user_data_service.sign_up(email=email,password=password)
            if status.acknowledged:
                return "user created"
            else:
                raise HTTPException(status_code=status.status_code,
                                    detail=status.message)

