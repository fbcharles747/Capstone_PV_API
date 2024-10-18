from enum import Enum

class Collections(str,Enum):
    USER_COLLECTION='users'
    LOCATION_COLLECTION='locations'
    INVERTER_COLLECTION='inverters'
    SOLARMOD_COLLECTION='modules'
    PVSYSTEM_COLLECTION='pvsystem'

    