from pydantic import BaseModel
from typing import Annotated
from fastapi import Body

class LocationModel(BaseModel):
    user_email:str
    latitude: Annotated[float, Body(description="Latitude in decimal degrees")]
    longitude: Annotated[float, Body(description="Longitude in decimal degrees")]
    altitude: Annotated[float, Body(description="Altitude in meters")]
    timezone: Annotated[str, Body(description="Timezone")]

    def __init__(self,**kwarg):
        super().__init__(**kwarg)