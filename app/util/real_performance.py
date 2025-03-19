from app.models.result import ModelResult
from app.api_adaptor.aggregate_data import Weather_Data
from math import pow

def estimate_real_performance(result:ModelResult,weather:Weather_Data)->ModelResult:
    ac_regression: float = (
        (-0.0123379785) * weather.ghi +
        (0.000545750613) * weather.dni +
        (0.006399367634) * weather.dhi +
        (0.000001157367694) * result.system_ac_power
    )

    result.system_ac_power=ac_regression * pow(10,6) if ac_regression >= 0 else 0

    return result

                        

