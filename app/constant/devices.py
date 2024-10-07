DEFAULT_INVERTER = {
    'Vac': 277,  # Nominal AC voltage (V)
    'Pso': 28.358692,  # Power consumption during operation (W)
    'Paco': 2500.0,  # Maximum AC power output (W)
    'Pdco': 2592.4729,  # Maximum DC power output (W)
    'Vdco': 360.0,  # Nominal DC voltage (V)
    'C0': -0.000008,  # Curvature between AC power and DC power (1/W)
    'C1': -0.000045,  # Coefficient of `Pdco` variation with DC input voltage (1/V)
    'C2': 0.00041,  # Coefficient of inverter power consumption loss variation with DC input voltage (1/V)
    'C3': -0.002524,  # Coefficient of C0 variation with DC input voltage (1/V)
    'Pnt': 0.5,  # Inverter night time loss (kW)
    'Vdcmax': 416.0,  # Maximum DC voltage (V)
    'Idcmax': 7.201314,  # Maximum DC current (A)
    'Mppt_low': 100.0,  # Minimum MPPT DC voltage (V)
    'Mppt_high': 416.0,  # Maximum MPPT DC voltage (V)
    'CEC_Date': None,  # CEC date (if applicable, None indicates missing data)
    'CEC_Type': 'Utility Interactive',  # Type of CEC classification
    'Name': 'ABB__UNO_2_5_I_OUTD_S_US__277V_'  # Name of the inverter
}

DEFAULT_MODULE = {
    'Name': 'Sunpreme_Inc__SNPM_GxB_510',  # Name of the solar module
    'Technology': 'Thin Film',               # Type of technology used in the solar module
    'Bifacial': 'N',                         # Indicates if the module is bifacial (Y/N)
    'STC': 509.97,                          # Standard Test Conditions power output (W)
    'PTC': 479.6,                           # PTC (PVUSA Test Conditions) power output (W)
    'A_c': 2.591,                           # Area of the solar panel (m²)
    'Length': 1.981,                        # Length of the solar panel (m)
    'Width': 1.308,                         # Width of the solar panel (m)
    'N_s': 96,                              # Number of cells in series
    'I_sc_ref': 9.4,                        # Short circuit current (A) at STC
    'V_oc_ref': 74.7,                       # Open circuit voltage (V) at STC
    'I_mp_ref': 8.9,                        # Max Power Current (A) at STC
    'V_mp_ref': 57.3,                       # Max power voltage (V) at STC
    'alpha_sc': 0.00094,                    # Short circuit current change per degree Celsius (A/°C)
    'beta_oc': -0.19422,                    # Open circuit voltage change per degree Celsius (V/°C)
    'T_NOCT': 45.5,                         # Module NOCT (Nominal Operating Cell Temperature) rating (°C)
    'a_ref': 2.41017,                       # Ideality factor (V) from CEC module database
    'I_L_ref': 9.40894,                     # Reference light current (A)
    'I_o_ref': 0.0,                         # Reference diode saturation current (A)
    'R_s': 1.135045,                        # Reference series resistance (Ω)
    'R_sh_ref': 1193.327026,                # Reference shunt resistance (Ω)
    'Adjust': -20.561962,                   # Temperature coefficient adjustment factor
    'gamma_r': -0.3,                        # Gamma (%/°C) indicating performance degradation with temperature
    'Version': 'SAM 2018.11.11 r2',         # Version of the module or simulation software
    'Date': '1/3/2019'                      # Manufacture date of the module
}



