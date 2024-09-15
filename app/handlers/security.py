from fastapi.security import APIKeyHeader
from fastapi import Security,HTTPException,status
from app.data_services.user import UserService
class APIKeyHandler:
    api_key_header=APIKeyHeader(name="x-api-key")
    def __init__(self,user_data_service:UserService):
        self.__user_service=user_data_service

    def verify_api_key(self,api_key:str=Security(api_key_header))->None:
        user=self.__user_service.get_by_apikey(api_key)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )
        elif user.api_key_enable is False:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key authorization is not enable"
            )
