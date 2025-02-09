from pydantic import BaseModel
from typing import Annotated
from datetime import datetime
from fastapi import Body

class Weather_Data(BaseModel):
    # General weather data
    temp: Annotated[float, Body(description="Temperature in Celsius (°C)")]
    feels_like: Annotated[float | None, Body(description="Feels like temperature in Celsius (°C)")] = None
    temp_min: Annotated[float | None, Body(description="Minimum temperature in Celsius (°C)")] = None
    temp_max: Annotated[float | None, Body(description="Maximum temperature in Celsius (°C)")] = None
    pressure: Annotated[float | None, Body(description="Atmospheric pressure in hPa")] = None
    humidity: Annotated[float | None, Body(description="Humidity percentage (%)")] = None
    sea_level: Annotated[float | None, Body(description="Sea level pressure in hPa")] = None
    grnd_level: Annotated[float | None, Body(description="Ground level pressure in hPa")] = None

    # Wind data
    wind_speed: Annotated[float , Body(description="Wind speed in meters per second (m/s)")]
    wind_deg: Annotated[float | None, Body(description="Wind direction in degrees (°)")] = None

    # Solar Irradiance Data
    ghi: Annotated[float, Body(description="Global horizontal irradiance in W/m²")]
    dni: Annotated[float, Body(description="Direct normal irradiance in W/m²")]
    dhi: Annotated[float, Body(description="Diffuse horizontal irradiance in W/m²")]
    gti: Annotated[float, Body(description="Global tilted irradiance in W/m²")]
    irradiance_timestamp: Annotated[datetime, Body(description="UTC timestamp of the irradiance data")]

    def __init__(self,**kwarg):
        super().__init__(**kwarg)



