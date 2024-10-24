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
    'Technology': 'Mono-c-Si',
    'Bifacial': 1,
    'STC': 550.62,
    'PTC': 516.4,
    'A_c': 2.52,
    'Length': None,  # NaN is represented as None in Python
    'Width': None,   # NaN is represented as None in Python
    'N_s': 72,
    'I_sc_ref': 14,
    'V_oc_ref': 49.9,
    'I_mp_ref': 13.11,
    'V_mp_ref': 42,
    'alpha_sc': 0.00546,
    'beta_oc': -0.13024,
    'T_NOCT': 44.8,
    'a_ref': 1.82357,
    'I_L_ref': 14.0167,
    'I_o_ref': 1.78e-11,
    'R_s': 0.164846,
    'R_sh_ref': 138.077,
    'Adjust': 6.23131,
    'gamma_r': -0.33,
    'BIPV': 'N',
    'Version': '2023.10.31',
    'Date': '11/16/2022',
    'Name': 'JA Solar JAM72D30-550/MB'
}



