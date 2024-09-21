
from fastapi import FastAPI
from abc import ABC,abstractmethod
from security import JWTHandler, APIKeyHandler

class BaseHandler(ABC):
    def __init__(self,tag:str,route:str,app:FastAPI,apikey_handler:APIKeyHandler,oauth_handler:JWTHandler):
        self.tag=tag
        self.route=route
        self.app=app
        self.apikey_handler=apikey_handler
        self.oauth_handler=oauth_handler

    @abstractmethod
    def register_routes(self):
        pass