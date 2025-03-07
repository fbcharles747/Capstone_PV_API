from app.models.result import ModelResult
from app.api_adaptor.aggregate_data import Weather_Data
from math import pow

def estimate_real_performance(result:ModelResult,weather:Weather_Data)->ModelResult:
    ac_regression:float=(-0.0722104769) * weather.ghi + (-0.00692898659) * weather.dni + (0.0120536989) * weather.dhi + (0.0000023656745)* result.system_ac_power
    result.system_ac_power=ac_regression * pow(10,6)

    return result

                        

