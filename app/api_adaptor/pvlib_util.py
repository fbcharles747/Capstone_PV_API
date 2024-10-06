import pvlib
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel


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