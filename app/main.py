from fastapi import FastAPI,Depends,HTTPException,status,Request
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer,APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from googlemaps.client import Client
from app.handlers.user import UserHandler
from app.handlers.location import LocationHandler
from app.handlers.security import APIKeyHandler,JWTHandler
from app.handlers.device import DeviceHandler
from app.handlers.system import PVSystemHandler
from app.data_services.user import UserService
from app.data_services.location import LocationService
from app.data_services.inverter import InverterService
from app.data_services.solar_module import SolarModuleService
from app.data_services.system import PVSystemService
from app.models.security import Token
from app.models.inverter import InverterModel
from app.models.solar_module import SolarModuleModel
from app.models.system import PVSystemModel,SolarArray
from app.constant.devices import DEFAULT_INVERTER,DEFAULT_MODULE
from typing import Annotated
import os
from app.api_adaptor.google_map import GoogleMap_Adaptor
from app.api_adaptor.open_weather_map import OpenWeather_Adaptor
from app.api_adaptor.solcast_api import Solcast_Adaptor
from app.constant.mongo_collection import Collections

# these are secret, need to be taken out in production
# secret='Gkq3b7z8J9k8L1k9J8k3L1k9J8k3L1k9J8k3L1k9J8k='
# gmap_apikey='AIzaSyBF2slAi7qpMnjPkcsqkQ0R59rYN9sOnNA'
# opweather_apikey='8bcf71b09bb730ee178c4d36c09206c1'
# db_uri="mongodb://user:pass@localhost:27017/"
oauth2Scheme=OAuth2PasswordBearer(tokenUrl="token")
# uncoment this line when running in container environment
db_uri=os.getenv("CONNECTION_STR")
gmap_apikey=os.getenv("GOOGLEMAP_APIKEY")
opweather_apikey=os.getenv("OPENWEATHER_APIKEY")
solcast_apikey=os.getenv("SOLCAST_APIKEY")
secret=os.getenv("SECRET_KEY")
# database connection

client=MongoClient(db_uri)
db=client.get_database("testDB")
gmap_client=Client(key=gmap_apikey)

# api adaptor
gmap_adaptor=GoogleMap_Adaptor(gmap_client)
opweather_adaptor=OpenWeather_Adaptor(apikey=opweather_apikey)
solcast_adaptor=Solcast_Adaptor(apikey=solcast_apikey)
# initialize data service
user_data_service=UserService(secret_key=secret,
                              collection_name=Collections.USER_COLLECTION.value,
                              db=db)
location_service=LocationService(collection_name=Collections.LOCATION_COLLECTION.value,db=db,
                                 gmap_adaptor=gmap_adaptor,
                                 open_weather_adaptor=opweather_adaptor,
                                 solcast_adaptor=solcast_adaptor)

inverter_service=InverterService(
    collection_name=Collections.INVERTER_COLLECTION.value,
    db=db,
    default_inverter=InverterModel(**DEFAULT_INVERTER)
)

module_service=SolarModuleService(
    collection_name=Collections.SOLARMOD_COLLECTION.value,
    db=db,
    default_solar_module=SolarModuleModel(**DEFAULT_MODULE)
)

default_system=PVSystemModel(
    name='default',
    num_of_array=4,
    array_config=SolarArray()
)

system_service=PVSystemService(
    collection_name=Collections.PVSYSTEM_COLLECTION,
    db=db,
    default_pv_system=default_system
)


# initialize security handler
apikey_handler=APIKeyHandler(user_data_service)
oauth_handler=JWTHandler(user_data_service=user_data_service,
                         secret=secret,
                         algorithm="HS256",
                         expiry_delta=15)

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize handler
user_handler=UserHandler(data_service=user_data_service,
                         apikey_handler=apikey_handler,
                         oauth_handler=oauth_handler,
                         app=app)

location_handler=LocationHandler(
    data_service=location_service,
    user_service=user_data_service,
    apikey_handler=apikey_handler,
    oauth_handler=oauth_handler,
    app=app
)

device_handler=DeviceHandler(
    inverter_service=inverter_service,
    module_service=module_service,
    user_service=user_data_service,
    apikey_handler=apikey_handler,
    oauth_handler=oauth_handler,
    app=app
)

system_handler=PVSystemHandler(
    data_service=system_service,
    user_service=user_data_service,
    app=app,
    apikey_handler=apikey_handler,
    oauth_handler=oauth_handler,
)


@app.get("/")
async def root():
    return "Hello there! go to `/docs` for documentation"

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = user_data_service.login( form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = oauth_handler.create_access_token({"sub": user.email})
    
    return Token(access_token=access_token, token_type="bearer")

@app.get("/test")
async def test_auth(authenticated:Annotated[bool,Depends(oauth_handler.verify_token)],
                    apikey_authenticated:Annotated[bool,Depends(apikey_handler.verify_api_key)]):
   
    return f"api key auth: {apikey_authenticated}   oauth auth:{authenticated}"


# register pathes of each handler
user_handler.register_routes()
location_handler.register_routes()
device_handler.register_routes()
system_handler.register_routes()




