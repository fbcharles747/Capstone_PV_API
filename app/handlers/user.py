from fastapi import FastAPI
from app.handlers.base import BaseHandler
from app.data_services.user import UserService
from app.models.user import User

class UserHandler(BaseHandler):
    def __init__(self,data_service:UserService,tag:str,route:str,app:FastAPI):
        super().__init__(tag=tag,route=route,app=app)
        self.user_data_service=data_service
    
    def register_routes(self):
        @self.app.get(self.route,tags=[self.tag])
        async def get_users():
            return "get all the users"
        
        @self.app.post(self.route,tags=[self.tag])
        async def sign_up():
            self.user_data_service.sign_up("example@ucalgary.ca","12345")
            return "sign up sucessful"

