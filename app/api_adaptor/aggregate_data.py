from pydantic import BaseModel,Field
from typing import Annotated

class Weather_Data(BaseModel):
    # General weather data
    temp: float | None
    feels_like: float | None = None
    temp_min: float | None = None
    temp_max: float | None = None
    pressure: float | None = None
    humidity: float | None = None
    sea_level: float | None = None
    grnd_level: float | None = None

    # Wind data
    wind_speed: float | None
    wind_deg: float | None

    # Solar Irradiance Data
    ghi:float
    ebh:float
    dni:float
    dhi:float
    cloud_opacity:float

    def __init__(self,**kwarg):
        super().__init__(**kwarg)


