import pvlib
from pvlib.location import Location
from pvlib.pvsystem import PVSystem,FixedMount, SingleAxisTrackerMount
from pvlib.modelchain import ModelChain

import pandas as pd
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
from pydantic import BaseModel


from app.models.inverter import InverterModel
from app.models.location import LocationModel
from app.models.solar_module import SolarModuleModel
from app.models.system import PVSystemModel
from app.models.result import SingleArrayStatus

from app.api_adaptor.aggregate_data import Weather_Data


class Solargis_TMY_Irradiance(BaseModel):
    ghi:float
    dni:float
    dhi:float
    irradiance_time_stamp:datetime

    def __init__(self,**kwarg):
        super().__init__(**kwarg)
    
    def to_dict_irradiance(self)->dict:
        result={
            "ghi":self.ghi,
            "dni":self.dni,
            "dhi":self.dhi,
            "irradiance_time_stamp":self.irradiance_time_stamp
        }

        return result

def get_current_irradiance_tmy(latitude: float, longitude: float) -> Solargis_TMY_Irradiance|None:
    result, _, _, _ = pvlib.iotools.get_pvgis_tmy(latitude=latitude, longitude=longitude)
    result = result.reset_index(names=['irradiance_time_stamp'])
    result['day_of_year'] = result['irradiance_time_stamp'].dt.dayofyear
    now = datetime.now(ZoneInfo('UTC'))
    days = now.timetuple().tm_yday
    result = result.loc[result['day_of_year'] == days]
    
    if result.empty:
        print(f"No data available for day {days}")
        return None

    # Convert current time to seconds since midnight
    now_seconds = now.hour * 3600 + now.minute * 60 + now.second

    # Convert dataset times to seconds since midnight
    result['time_seconds'] = result['irradiance_time_stamp'].dt.hour * 3600 + result['irradiance_time_stamp'].dt.minute * 60

    # Calculate the difference in seconds
    result['diff_from_now'] = abs(result['time_seconds'] - now_seconds)

    # Find the row with the minimum time difference
    obj = result.loc[result['diff_from_now'].idxmin()]
    
    return Solargis_TMY_Irradiance(**obj.to_dict())

def run_model(location:LocationModel,weather:Weather_Data,module:SolarModuleModel,inverter:InverterModel,system:PVSystemModel)->SingleArrayStatus:
    pvlib_location=Location(
        latitude=location.latitude,
        longitude=location.longitude,
        tz=location.timezone,
        altitude=location.altitude,
        name=location.name
    )

    print(f'location: {pvlib_location}')

    pvlib_system=PVSystem(
        surface_tilt=system.array_config.fix_mount.surface_tilt,
        surface_azimuth=system.array_config.fix_mount.surface_azimuth,
        module_parameters=module.model_dump(),
        inverter_parameters=inverter.model_dump(),
        strings_per_inverter=system.array_config.strings,
        modules_per_string=system.array_config.modules_per_string,
        racking_model=system.array_config.fix_mount.racking_model,
        module_type=system.array_config.module_type
    )
    print(pvlib_system)
    print(f'inverter params: {pvlib_system.inverter_parameters}')
    print(f'module params: {pvlib_system.arrays[0].module_parameters}')

    weather_data={
        'ghi':weather.ghi,
        'dni':weather.dni,
        'dhi':weather.dhi,
        'temp_air':weather.temp,
        'wind_speed':weather.wind_speed,
        'humidity':weather.humidity
    }

    print(f'weather: {weather_data}')

    precipitable_water=pvlib.atmosphere.gueymard94_pw(weather_data['temp_air'],weather_data['humidity'])
    weather_data.update(precipitable_water=precipitable_water)
    weather_data.pop('humidity')

    print(f'weather: {weather_data}')

    pvlib_weather=pd.DataFrame([weather_data],index=[pd.Timestamp('2024-11-04T19:15:00Z')])

    model_chain=ModelChain(system=pvlib_system,location=pvlib_location,aoi_model='no_loss')
    model_chain.run_model(pvlib_weather)

    result=model_chain.results.dc.reset_index(names='time_stamp').loc[0].to_dict()


    return SingleArrayStatus(**result)