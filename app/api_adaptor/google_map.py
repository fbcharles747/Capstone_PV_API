from pydantic import BaseModel
from googlemaps.elevation import elevation
from googlemaps.timezone import timezone
from googlemaps.exceptions import ApiError, HTTPError, Timeout, TransportError
from googlemaps.client import Client

class GoogleTimeZone(BaseModel):
    dstOffset: int | None
    rawOffset: int | None
    status: str
    timeZoneId: str | None
    timeZoneName: str | None
    def __init__(self, **kwarg):
        super().__init__(**kwarg)


class GoogleMap_Adaptor:
    def __init__(self, client: Client) -> None:
        self.__client = client
    
    def get_timezone(self, latitude: float, longitude: float) -> GoogleTimeZone|None:
        try:
            result = timezone(client=self.__client, location=(latitude, longitude))
            return GoogleTimeZone(**result)
        except (ApiError, HTTPError, Timeout, TransportError) as e:
            print(f"Error fetching timezone: {str(e)}")
            return None
    
    def get_altitude(self, latitude: float, longitude: float) -> float | None:
        try:
            result = elevation(client=self.__client, locations=(latitude, longitude))
            return result[0]['elevation']
        except (ApiError, HTTPError, Timeout, TransportError) as e:
            print(f"Error fetching altitude: {str(e)}")
            return None
        except (IndexError, KeyError) as e:
            print(f"Error processing altitude data: {str(e)}")
            return None