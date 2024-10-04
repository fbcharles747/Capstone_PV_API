# open weather API adaptor
from pydantic import BaseModel
from enum import Enum
import requests
class OpenWeather_General(BaseModel):
    temp:float|None
    feels_like:float|None=None
    temp_min:float|None=None
    temp_max:float|None=None
    pressure:float|None=None
    humidity:float |None=None
    sea_level:float|None=None
    grnd_level:float|None=None
    
    def __init__(self,**kwarg):
        super().__init__(**kwarg)

class OpenWeather_Wind(BaseModel):
    speed:float|None
    deg:float|None=None
    gust:float|None=None
    def __init__(self,**kwarg):
        super().__init__(**kwarg)

    def to_dict(self)->dict:
        result={
            "wind_speed":self.speed,
            "wind_deg":self.deg,
        }
        return result



class OpenWeather_Unit(Enum):
    STANDARD='standard'
    METRIC='metric'
    IMPERIAL='imperial'

class OpenWeather_Adaptor:

    def __init__(self,apikey:str):
        self.__apikey=apikey
    
    def get_currentWeather(self, latitude: float, longitude: float) -> tuple[OpenWeather_General, OpenWeather_Wind]:
        try:
            res = requests.get("https://api.openweathermap.org/data/2.5/weather", params={
                "lat": latitude,
                "lon": longitude,
                "appid": self.__apikey,
                "units": OpenWeather_Unit.METRIC.value
            })
            res.raise_for_status()  # Raise an exception for bad status codes
            result = res.json()
            general_data = OpenWeather_General(**result['main'])
            wind_data = OpenWeather_Wind(**result["wind"])
            return general_data, wind_data
        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None, None
        except KeyError as e:
            print(f"Error parsing weather data: {e}")
            return None, None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None, None
