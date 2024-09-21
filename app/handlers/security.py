from fastapi.security import APIKeyHeader,OAuth2PasswordBearer,HTTPBearer
from datetime import datetime,timedelta,timezone
from fastapi import Security,Depends,HTTPException,status
import jwt
from jwt.exceptions import InvalidTokenError
from app.data_services.user import UserService
from app.models.security import Token,TokenData
from app.models.user import User
from typing import Optional,Annotated

class APIKeyHandler:
    api_key_header=APIKeyHeader(name="x-api-key",auto_error=False)
    def __init__(self,user_data_service:UserService):
        self.__user_service=user_data_service

    def apikey_from_request(self,api_key:Annotated[Optional[str],Depends(api_key_header)])->Optional[str]:
        return api_key
    
    def verify_api_key(self,api_key:Annotated[Optional[str],Depends(api_key_header)])->bool:
        if api_key is None:
            return False
        user=self.__user_service.get_by_apikey(api_key)
        if user is None :
            return False
        elif user.api_key_enable is False:
            return False
        return True
    
    def get_current_user(self,api_key:Annotated[Optional[str],Depends(api_key_header)])->Optional[User]:
        authorization_exception=HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
        authenticated=self.verify_api_key(api_key)
        if not authenticated:
            raise authorization_exception
        return self.__user_service.get_by_apikey(api_key)


class JWTHandler:
    oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token",auto_error=False)
    def __init__(self,user_data_service:UserService,secret:str,algorithm:str|None,expiry_delta:int) -> None:
        self.__secret_key=secret
        self.__algorithm=algorithm
        self.__expire_time=expiry_delta
        self.__user_data_service=user_data_service

    def token_from_request(self,access_token:Annotated[Optional[str],Depends(oauth2_scheme)])->Optional[str]:
        return access_token
    
    def create_access_token(self, data:dict)->str:
        to_encode=data.copy()
        expiry=datetime.now(timezone.utc) + timedelta(minutes=self.__expire_time)
        to_encode.update({"exp":expiry.timestamp()})
        encoded_jwt=jwt.encode(payload=to_encode,algorithm=self.__algorithm,key=self.__secret_key)
        return encoded_jwt
    
    def login_for_access_token(self, email:str,password:str)->Optional[Token]:
        user=self.__user_data_service.login(email,password)
        if user is not None:
            access_token=self.create_access_token({"sub":user.email})
            return Token(access_token=access_token,token_type="bearer")
        return None

    def decode_token(self,access_token:Annotated[str,Security(oauth2_scheme)])->Optional[TokenData]:
        try: 
            payload=jwt.decode(jwt=access_token,key=self.__secret_key,algorithms=[self.__algorithm])
            expiration:float=payload.get("exp")
            email:str=payload.get("sub")
            if (email is None) or (expiration is None):
                return None
            return TokenData(email=email,expiration_timestamp=expiration)
        except InvalidTokenError:
            return None
        
    def verify_token(self, access_token:Annotated[str,Security(oauth2_scheme)])->bool:
        token_data=self.decode_token(access_token)
        if token_data is None:
            return False    
        
        exp_datetime=datetime.fromtimestamp(timestamp=token_data.expiration_timestamp,tz=timezone.utc)
        if exp_datetime < datetime.now(timezone.utc) or token_data.email is None:
            return False
        
        return True
    # issue: don't depends this on `token_from_request` method
    def get_current_user(self,access_token:Annotated[str,Depends(oauth2_scheme)])->Optional[User]:
        invalidTokenException=HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token"
            )
        authenticated=self.verify_token(access_token=access_token)
        if not authenticated:
            raise invalidTokenException
        token_data=self.decode_token(access_token)
        if token_data is None:
            raise invalidTokenException
        return self.__user_data_service.get_by_email(token_data.email)
    
    
    
    