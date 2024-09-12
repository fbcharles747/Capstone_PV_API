from fastapi import FastAPI
from app.handlers.base import BaseHandler
from app.data_services.user import UserService

class UserHandler(BaseHandler):
    def __init__(self,data_service:UserService,tag:str,route:str,app:FastAPI):
        super().__init__(tag=tag,route=route,app=app)
    
    def register_routes(self):
        @self.app.get(self.route,tags=[self.tag])
        async def get_users():
            return "get all the users"

