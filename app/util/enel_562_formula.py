from app.models.solar_module import SolarModuleModel
from app.models.system import PVSystemModel
from app.models.result import ModelResult
from app.models.inverter import InverterModel
from app.api_adaptor.aggregate_data import Weather_Data


def run_model(module:SolarModuleModel,inverter:InverterModel,system:PVSystemModel,weather:Weather_Data)->ModelResult:
    
    result:ModelResult=ModelResult()
    single_module_generation:float=module.A_c * weather.gti * module.Efficiency
    dc_power: float = (
        single_module_generation *
        system.array_config.modules_per_string *
        system.array_config.strings *
        system.num_of_array
    )
    ac_power:float=dc_power * (inverter.Efficiency - 0.02)
    result.system_ac_power=ac_power
    result.system_dc_power=dc_power
    
    return result
