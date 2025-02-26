import pandas as pd
import pvlib
import pytz
from pvlib.pvsystem import PVSystem
from pvlib.location import Location
from pvlib.modelchain import ModelChain
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
from solcast import live
from datetime import datetime, timezone

from app.models.result import ModelResult

def Barlow_pvlib_script(solcast_apikey:str) -> ModelResult:
    temperature_model_parameters = TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

    #sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')
    cec_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')

    #sandia_module = sandia_modules['Canadian_Solar_CS5P_220M___2009_']
    cec_modules = pvlib.pvsystem.retrieve_sam('CECMod')
    cec_module=cec_modules['Canadian_Solar_Inc__CS3W_405P']
    cec_inverter = cec_inverters['ABB__MICRO_0_25_I_OUTD_US_208__208V_']
    df = pvlib.pvsystem.retrieve_sam(name='CECInverter')


    #Module parameters
    #df=cec_modules['Canadian_Solar_Inc__CS3W_405P']
    #print(df)
    cec_module.Technology='Mono-c-Si'
    cec_module.Bifacial=1
    cec_module.STC=540.849
    cec_module.PTC=504.4
    cec_module.A_c=2.58
    cec_module.Length=2.256
    cec_module.Width=1.133
    cec_module.N_s=72
    cec_module.I_sc_ref=13.85
    cec_module.V_oc_ref=49.7
    cec_module.I_mp_ref=12.97
    cec_module.V_mp_ref=41.7
    cec_module.alpha_sc=0.0054015
    cec_module.beta_oc=-0.128723
    cec_module.T_NOCT=46
    cec_module.a_ref=1.81475
    cec_module.I_L_ref=13.8675
    cec_module.I_o_ref=0.0000000000172538
    cec_module.R_s=0.177359
    cec_module.R_sh_ref=140.584
    cec_module.Adjust=6.85992
    cec_module.gamma_r=-0.331
    cec_module.BIPV	='N'
    cec_module.name='VSUN540-144BMH-DG'
    cec_module.Version='SAM 2024.01.01'
    # #print(cec_module)
    # print("Inverter Parameters before update")
    # print(cec_inverter)
    cec_inverter.Paco=3606980
    cec_inverter.Pdco=3708310
    cec_inverter.Pso=7573.76
    cec_inverter.Vac='630'
    cec_inverter.Vdco=1100
    cec_inverter.C0=-0.00000000473641
    cec_inverter.C1=0.00000304621
    cec_inverter.C2=0.000146486
    cec_inverter.C3=-0.0000950682
    cec_inverter.Pnt=264.05
    cec_inverter.Vdcmax=1300
    cec_inverter.Idcmax=3371.19
    cec_inverter.Mppt_low=915
    cec_inverter.Mppt_high=1300
    cec_inverter.name='Sungrow SG3600UD'
    #print("The Inverter Parameters after update")
    #print(cec_inverter)

    lat=50.954694
    lon=-113.986028
    location = Location(latitude=lat, longitude=lon)

    #New Code
    #Inverter 0
    system = PVSystem(
        surface_tilt=25,
        surface_azimuth=180,
        module_parameters=cec_module,
        inverter_parameters=cec_inverter,
        temperature_model_parameters=temperature_model_parameters,
        modules_per_string=25, strings_per_inverter=308, losses_parameters={'age': 0.5,'soiling' : 1, 'shading' :1, 'mismatch' : 0.25, 'wiring': 1, 'connections' : 0.25, 'lid':0.5, 'nameplate_rating' : 0, 'availability':0}

    )
    #Inverter 1
    system1 = PVSystem(
        surface_tilt=25,
        surface_azimuth=180,
        module_parameters=cec_module,
        inverter_parameters=cec_inverter,
        temperature_model_parameters=temperature_model_parameters,
        modules_per_string=25, strings_per_inverter=302, losses_parameters={'age': 0.5,'soiling' : 1, 'shading' :1, 'mismatch' : 0.25, 'wiring': 1, 'connections' : 0.25, 'lid':0.5, 'nameplate_rating' : 0, 'availability':0}

    )
    #Inverter 2
    system2 = PVSystem(
        surface_tilt=25,
        surface_azimuth=180,
        module_parameters=cec_module,
        inverter_parameters=cec_inverter,
        temperature_model_parameters=temperature_model_parameters,
        modules_per_string=25, strings_per_inverter=313, losses_parameters={'age': 0.5,'soiling' : 1, 'shading' :1, 'mismatch' : 0.25, 'wiring': 1, 'connections' : 0.25, 'lid':0.5, 'nameplate_rating' : 0, 'availability':0}

    )
    #Inverter 3
    system3 = PVSystem(
        surface_tilt=25,
        surface_azimuth=180,
        module_parameters=cec_module,
        inverter_parameters=cec_inverter,
        temperature_model_parameters=temperature_model_parameters,
        modules_per_string=25, strings_per_inverter=306, losses_parameters={'age': 0.5,'soiling' : 1, 'shading' :1, 'mismatch' : 0.25, 'wiring': 1, 'connections' : 0.25, 'lid':0.5, 'nameplate_rating' : 0, 'availability':0}

    )
    #Inverter 4
    system4 = PVSystem(
        surface_tilt=25,
        surface_azimuth=180,
        module_parameters=cec_module,
        inverter_parameters=cec_inverter,
        temperature_model_parameters=temperature_model_parameters,
        modules_per_string=25, strings_per_inverter=320, losses_parameters={'age': 0.5,'soiling' : 1, 'shading' :1, 'mismatch' : 0.25, 'wiring': 1, 'connections' : 0.25, 'lid':0.5, 'nameplate_rating' : 0, 'availability':0}

    )
    #Inverter 5
    system5 = PVSystem(
        surface_tilt=25,
        surface_azimuth=180,
        module_parameters=cec_module,
        inverter_parameters=cec_inverter,
        temperature_model_parameters=temperature_model_parameters,
        modules_per_string=25, strings_per_inverter=299, losses_parameters={'age': 0.5,'soiling' : 1, 'shading' :1, 'mismatch' : 0.25, 'wiring': 1, 'connections' : 0.25, 'lid':0.5, 'nameplate_rating' : 0, 'availability':0}

    )
    #Inverter 6
    system6 = PVSystem(
        surface_tilt=25,
        surface_azimuth=180,
        module_parameters=cec_module,
        inverter_parameters=cec_inverter,
        temperature_model_parameters=temperature_model_parameters,
        modules_per_string=25, strings_per_inverter=317 , losses_parameters={'age': 0.5,'soiling' : 1, 'shading' :1, 'mismatch' : 0.25, 'wiring': 1, 'connections' : 0.25, 'lid':0.5, 'nameplate_rating' : 0, 'availability':0}

    )
    #Inverter 7
    system7 = PVSystem(
        surface_tilt=25,
        surface_azimuth=180,
        module_parameters=cec_module,
        inverter_parameters=cec_inverter,
        temperature_model_parameters=temperature_model_parameters,
        modules_per_string=25, strings_per_inverter=301, losses_parameters={'age': 0.5,'soiling' : 1, 'shading' :1, 'mismatch' : 0.25, 'wiring': 1, 'connections' : 0.25, 'lid':0.5, 'nameplate_rating' : 0, 'availability':0}

    )
    #Inverter 8
    system8 = PVSystem(
        surface_tilt=25,
        surface_azimuth=180,
        module_parameters=cec_module,
        inverter_parameters=cec_inverter,
        temperature_model_parameters=temperature_model_parameters,
        modules_per_string=25, strings_per_inverter=300, losses_parameters={'age': 0.5,'soiling' : 1, 'shading' :1, 'mismatch' : 0.25, 'wiring': 1, 'connections' : 0.25, 'lid':0.5, 'nameplate_rating' : 0, 'availability':0}

    )
    #Inverter 9
    #Maxing out Inverter Clipping
    system9 = PVSystem(
        surface_tilt=25,
        surface_azimuth=180,
        module_parameters=cec_module,
        inverter_parameters=cec_inverter,
        temperature_model_parameters=temperature_model_parameters,
        modules_per_string=25, strings_per_inverter=308, losses_parameters={'age': 0.5,'soiling' : 1, 'shading' :1, 'mismatch' : 0.25, 'wiring': 1, 'connections' : 0.25, 'lid':0.5, 'nameplate_rating' : 0, 'availability':0}

    )
    #Inverter 0
    mc = ModelChain(system, location, aoi_model="physical",spectral_model="no_loss", losses_model="pvwatts")
    #Inverter 1
    mc1 = ModelChain(system1, location, aoi_model="physical",spectral_model="no_loss", losses_model="pvwatts")
    #Inverter 2
    mc2 = ModelChain(system2, location, aoi_model="physical",spectral_model="no_loss", losses_model="pvwatts")
    #Inverter 3
    mc3 = ModelChain(system3, location, aoi_model="physical",spectral_model="no_loss", losses_model="pvwatts")
    #Inverter 4
    mc4 = ModelChain(system4, location, aoi_model="physical",spectral_model="no_loss", losses_model="pvwatts")
    #Inverter 5
    mc5 = ModelChain(system5, location, aoi_model="physical",spectral_model="no_loss", losses_model="pvwatts")
    #Inverter 6
    mc6 = ModelChain(system6, location, aoi_model="physical",spectral_model="no_loss", losses_model="pvwatts")
    #Inverter 7
    mc7 = ModelChain(system7, location, aoi_model="physical",spectral_model="no_loss", losses_model="pvwatts")
    #Inverter 8
    mc8 = ModelChain(system8, location, aoi_model="physical",spectral_model="no_loss", losses_model="pvwatts")
    #Inverter 9
    mc9 = ModelChain(system9, location, aoi_model="physical",spectral_model="no_loss",losses_model="pvwatts")


    solcast_resp = live.radiation_and_weather(
        latitude=lat,
        longitude=lon,
        output_parameters=['ghi', 'dni', 'dhi', 'air_temp', 'wind_speed_10m'],
        period='PT15M',
        hours=18, #Duration
        api_key=solcast_apikey
    )

    solcast_weather = solcast_resp.to_pandas()
    # Solcast API data is "period end" while PVLib expects instantaneous
    # To account for this, relabel the Solcast data to "period middle"
    solcast_weather.index = solcast_weather.index - pd.Timedelta(minutes=7.5)
    # timeseries in local time for readability
    #solcast_weather.index = solcast_weather.index.tz_convert('Europe/Rome')
    #Adjusting for Alberta
    # solcast_weather.index = solcast_weather.index.tz_convert('Canada/Mountain')

    #Inverter 0
    mc.run_model(solcast_weather)
    #Inverter 1
    mc1.run_model(solcast_weather)
    #Inverter 2
    mc2.run_model(solcast_weather)
    #Inverter 3
    mc3.run_model(solcast_weather)
    #Inverter 4
    mc4.run_model(solcast_weather)
    #Inverter 5
    mc5.run_model(solcast_weather)
    #Inverter 6
    mc6.run_model(solcast_weather)
    #Inverter 7
    mc7.run_model(solcast_weather)
    #Inverter 8
    mc8.run_model(solcast_weather)
    #Inverter 9 Not Part of Barlow
    mc9.run_model(solcast_weather)

    system_ac_power:float=mc1.results.ac.iloc[-1] + mc2.results.ac.iloc[-1]+mc3.results.ac.iloc[-1]+ mc4.results.ac.iloc[-1]+ mc5.results.ac.iloc[-1]+ mc6.results.ac.iloc[-1]+ mc7.results.ac.iloc[-1]+ mc8.results.ac.iloc[-1]+mc9.results.ac.iloc[-1]
    result:ModelResult=ModelResult()
    result.system_ac_power=system_ac_power
    result.system_dc_power=0
    result.time_stamp=datetime.now(tz=timezone.utc)
    result.calendar_year=result.time_stamp.year
    result.month=result.time_stamp.month
    result.day_of_month= result.time_stamp.day
    return result