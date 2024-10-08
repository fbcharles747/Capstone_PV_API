# Solcast API adaptor
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel
import pandas as pd
import requests

class Solcast_Irradiance(BaseModel):
    ghi:float
    dni:float
    dhi:float
    period_end:datetime|None

    def __init__(self,**kwarg):
        super().__init__(**kwarg)
    
    def to_dict_irradiance(self)->dict:
        result={
            "ghi":self.ghi,
            "dni":self.dni,
            "dhi":self.dhi,
            "irradiance_timestamp":self.period_end
        }

        return result




class Solcast_Adaptor:
    def __init__(self,apikey:str):
        self.__apikey=apikey

    def get_estimated_actuals(self,latitude:float,longitude:float)->pd.DataFrame|None:
        try:
            response=requests.get(f"https://api.solcast.com.au/data/live/radiation_and_weather",
                                  params={
                                      "api_key":self.__apikey,
                                      "latitude": latitude,
                                      "longitude":longitude,
                                      "hours":1,
                                      "format":'json',
                                      "output_parameters":['dni','ghi','dhi'],
                                      "period":"PT15M"
                                  })
            response.raise_for_status()
            result=response.json()
            return pd.DataFrame(data=result["estimated_actuals"])
        except requests.RequestException as e:
            print(f"Error fetching the irradiance data: {e}")
            return None
        except KeyError as e:
            print(f"Error parsing the irradiance data: {e}")
            return None
        except Exception as e:
            print(f"unexpected exception in `get_estimated_actual`:{e}")
            return None
        
    def get_current_irradiance(self,latitude:float,longitude:float)->Solcast_Irradiance|None:
        irradiance_estimated=self.get_estimated_actuals(latitude=latitude,longitude=longitude)
        if irradiance_estimated is None:
            print(f"could not load irradiance data from `get_estimate_actuals`")
            return None
        irradiance_estimated['period_end']=pd.to_datetime(irradiance_estimated['period_end'])
        now=datetime.now(tz=ZoneInfo('UTC'))
        irradiance_estimated["diff_from_now"]=abs(irradiance_estimated['period_end'] - now)
        index_min=irradiance_estimated['diff_from_now'].idxmin()
        result_irradiance=irradiance_estimated.loc[index_min]
        parameters=result_irradiance.to_dict()
        result=Solcast_Irradiance(**parameters)
        return result