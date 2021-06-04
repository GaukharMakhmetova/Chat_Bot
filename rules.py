from collections import defaultdict

rulesDict = {
"MC":
    [
        "Rated Current", # error in original table: "Rated Currnet"
        "Coil rating",
        "Main contact",
        "Auxcontact",
        "Terminal"
    ],
'MMS':
    [
        "Rated current",
        "Breaking Capacity", # TODo объединил пока столбцы, чтобы как в word было
        "Frame size"
    ],
'MCB':
    [
        "Standard",
        "Rated current",
        "Nos. of pole",
        "Operating Voltage",
        "Trip curve"
    ],
'MCCB':
    [
        "Rated current",
        "Grade", #TODO список из нескольких столбцов мб, либо коммент текстом, грейды E N H L + опционально T
        "Trip unit", #TODO тут кодировки, надо как-то их перебивать
        "Pole",
        "Efficency", #TODO проверка есть ли T 80% или 100%  производительности. Пока тупо добавил колонку, но она скипается
        "Termination" #TODO  возможно потребуется расшифровка сокращений, или по первым буквам
    ],
'TOR':
    [
        "Rated current",
        "Heater type",
        "Terminal",
        "frame size"
    ],
'Contactor Relay':
    [
        "Coil rating",
        "# of contact",
        "Contact description"
    ],
'EMPR':
    [
        "Series Name (Class 2)",
        "Nominal Current",
        "Control Voltage",
        "Aux. Contact",
        "Wiring Method",
        "Option"
    ]
    # 'Accessories': TODO додумать, т.к. там невероятная солянка
    #     [
    #         "",
    #         "",
    #         "",
    #         "",
    #     ]
}

rulesComments = defaultdict(dict,
{
'MCCB':  {
    "Grade": """
        E 	50KA@120/240, 	50KA@240, 	25KA@480, 	14KA@600
        N	65KA@120/240, 	65KA@240, 	35KA@480, 	18KA@600
        H	100KA@120/240, 	100KA@240, 	65KA@480, 	35KA@600
        L	No Rating		150KA@240, 	100KA@480,	50KA@600	
        
        T   for 100% performance, default 80%
    """,
    "Trip unit": """
        FTU – Fixed Thermal and Fixed Magnetic 
        FMU – Adjustable Thermal and Fixed Magnetic
        ATU – Adjustable Thermal and Adjustable Magnetic 
        MCS – Molded Case Switch 
        MCP – Motor Circuit Protector
        ETS23 LSI  – Electronic Trip Unit Standard (Long Term, Short Term, Instantaneous)
        ETM33 – Electronic Trip Unit Multi-Function (Long Term, Short Term, Instantaneous, Ig – earth fault/ground fault)
        
        Above 800A – In large Breakers the trip unit remains three characters but each character has choices – Example: NGO – select from each letter position (OCR I, OCR II, and OCR III) 
        
        i.	OCR I
        
        N – Normal – no metering functions
        A – Ammeter – current meter 
        P – Power Meter – current, voltage and power meter
        S – Super Meter – current, voltage, power, power factor and harmonics meter
        MCP – Motor Circuit Protector
        MCS – Molded Case Switch
        
        ii.	OCR II
        G – Communications (X)
        E – Com.(X) + Outer CT(G/F)
        C – Communications (O)
        X – Com.(O) + Outer CT(G/F)
        
        iii.	OCR III
        
        0: Power(x), 60Hz
        1: Ac/Dc 100~250V, 60Hz
        2: Dc 24~60V, 60Hz
        5: Power(x), 50Hz
        6: Ac/Dc 100~250V, 50Hz
        7: Dc 24~60V, 50Hz
        
        Examples: AC7, FTU, ATU, ETM33
    """,
    "Termination": """
        LL: Line and Load side lugs
        L: Line side lugs only
        LO: Load side lugs only
        -: Bolt on
    """
},
'TOR': {
    "Heater type": """
        2H: Non-differential(2-heater)
        3H: Non-differential(3-heater)
        3K: Differential
        3D: Class 20
    """
},
'MCB': {
    'Trip curve' : """
        B – instantaneous trip at 3-5 times rated current
        C – instantaneous trip at 5-10 times rated current
        D – instantaneous trip at 10-20 times rated current
        
        Note: All mini circuit breakers are 80% rated breakers. 
    """
}
}
)

