from pydantic import BaseModel
from app.api_adaptor.aggregate_data import Weather_Data
class CacheData(BaseModel):
    weather:Weather_Data|None=None