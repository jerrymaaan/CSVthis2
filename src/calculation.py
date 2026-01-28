from CoolProp.CoolProp import PropsSI

# -----------------------------
# functions how to calculate new columns in df
# -----------------------------
'''
ADD YOUR OWN FUNCTIONS HERE
(see examples below)
'''


def _test_addition(df):
    res = df['T1'] + df['T2']
    return res


def _test_power(df):
    res = df['I /A'] * df['E /V']
    return res


def _test_enthalpy(df):
    res = PropsSI('H',
                  'T', df['T1'].to_numpy() + 273.15,  # °C to K
                  'P', df['p_e'].to_numpy() * 1e5,  # bar to Pa
                  'Propane') / 1000  # J/kg to kJ/kg
    return res


# -----------------------------
# tells which column name is calculated with which function
# -----------------------------
'''
ADD YOUR COLUMN NAMES HERE
(see examples below)
'''
CALCULATED_COLUMNS = {
    'test_addition': _test_addition,
    'test_enthalpy': _test_enthalpy,
    'power /w': _test_power,
}


# -----------------------------
# for dropdown callback (DO NOT CHANGE)
# -----------------------------
def add_col(df):
    # adds all columns to df, no calculation needed at this point
    for col, func in CALCULATED_COLUMNS.items():
        df[col] = None

    return df


# -----------------------------
# for update_graph callback (DO NOT CHANGE)
# -----------------------------
def do_calc(df):
    # adds all columns and do calculation
    for col, func in CALCULATED_COLUMNS.items():
        df[col] = func(df)

    return df
