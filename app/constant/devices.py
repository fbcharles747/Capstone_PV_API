DEFAULT_INVERTER = {
    'Vac': 630,  # Nominal AC voltage (V)
    'Pso': 7573.76,  # Power consumption during operation (W)
    'Paco': 3606980,  # Maximum AC power output (W)
    'Pdco': 3708310,  # Maximum DC power output (W)
    'Vdco': 1100,  # Nominal DC voltage (V)
    'C0': -0.00000000473641,  # Curvature between AC power and DC power (1/W)
    'C1': 0.00000304621,  # Coefficient of `Pdco` variation with DC input voltage (1/V)
    'C2': 0.000146486,  # Coefficient of inverter power consumption loss variation with DC input voltage (1/V)
    'C3': -0.0000950682,  # Coefficient of C0 variation with DC input voltage (1/V)
    'Pnt': 264.05,  # Inverter night time loss (kW)
    'Vdcmax': 1300,  # Maximum DC voltage (V)
    'Idcmax': 3371.19,  # Maximum DC current (A)
    'Mppt_low': 915,  # Minimum MPPT DC voltage (V)
    'Mppt_high': 1300,  # Maximum MPPT DC voltage (V)
    'CEC_Date': None,  # CEC date (if applicable, None indicates missing data)
    'CEC_Type': 'Utility Interactive',  # Type of CEC classification
    'Name': 'Sungrow Power Supply Co - Ltd : SG3600UD [630V]',  # Name of the inverter
    'Efficiency': 0.97717  # Efficiency of the inverter
}

DEFAULT_MODULE = {
  "Technology": "Mono-c-Si",
  "Bifacial": 1,
  "STC": 540.849,
  "PTC": 504.4,
  "A_c": 2.6,
  "Length": 2.256,
  "Width": 1.133,
  "N_s": 72,
  "I_sc_ref": 13.85,
  "V_oc_ref": 49.7,
  "I_mp_ref": 12.97,
  "V_mp_ref": 41.7,
  "alpha_sc": 0.0054015,
  "beta_oc": -0.128723,
  "T_NOCT": 46,
  "a_ref": 1.81475,
  "I_L_ref": 13.8675,
  "I_o_ref": 1.72538e-11,
  "R_s": 0.177359,
  "R_sh_ref": 140.584,
  "Adjust": 6.85992,
  "gamma_r": -0.331,
  "BIPV": "N",
  "Version": "2023.10.31",
  "Date": "11/16/2022",
  "Name": "VSUN540-144BMH-DG",
  "Efficiency": 0.2267
}



