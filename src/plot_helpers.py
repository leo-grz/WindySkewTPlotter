import metpy.calc as mpcalc

def calc_params(pres, temp, dew, parcel_prof):

    '''Needs pressure, temperature, dewpoint and parcel trace to return a dictionary
    which contains LCL, LFC, EL, CCL, CAPE, CIN'''

    # points
    lcl = mpcalc.lcl(pres[0], temp[0], dew[0])
    lfc = mpcalc.lfc(pres, temp, dew)
    el = mpcalc.el(pres, temp, dew)
    ccl = mpcalc.ccl(pres, temp, dew)[:2]  # Extract only pressure and temperature
    
    # temperatures
    equiv_pot_temp = mpcalc.equivalent_potential_temperature(pres, temp, dew)
    wet_bulb_temp = mpcalc.wet_bulb_temperature(pres, temp, dew)
    wet_bulb_pot_temp = mpcalc.wet_bulb_potential_temperature(pres, temp, dew)
    

    # cape, cin
    cape, cin = mpcalc.cape_cin(pres, temp, dew, parcel_prof)

    # indices
    lifted_index = mpcalc.lifted_index(pres, temp, parcel_prof)
    k_index = mpcalc.k_index(pres, temp, dew)
    total_totals_index = mpcalc.total_totals_index(pres, temp, dew)
    showalter_index = mpcalc.showalter_index(pres, temp, dew)

    params = {
        # points on graph, x-value: °K, y-value: hPa, layout: (hPa, K)
        "points": {
            "LCL": lcl,
            "LFC": lfc,
            "EL": el,
            "CCL": ccl,
        },
        # cape and cin in j/kg
        "cape_cin": {
            "CAPE": cape,
            "CIN": cin
        },
        # temperatures
        "temperatures": {
            "\u03B8e": equiv_pot_temp,
            "Tw": wet_bulb_temp,
            "\u03B8w": wet_bulb_pot_temp
        },
        # indices generally don't have units!
        "indices": {
            "Lifted Index": lifted_index,
            "K Index": k_index,
            "Total Totals Index": total_totals_index,
            "Showalter Stability Index": showalter_index
        }
    }

    return params

def create_description(params):

    def hl(headline):
        return f"\n[ {headline} ]\n"

    description = hl('POINTS')

    for key, val in params['points'].items():
        description += f"{key}: {round(val[1].to('degC'), 1).m}°C | {round(val[0].m, 1)} hPa\n"

    description += hl('CAPE & CIN')

    for key, val in params['cape_cin'].items():
        description += f"{key}: {round(val.m, 1)} j/kg\n"

    description += hl('TEMPERATURES AT GROUND')

    for key, val in params['temperatures'].items():
        description += f"{key}: {round(val[0].m, 1)} °K\n"
    
    description += hl('INDICES')

    for key, val in params['indices'].items():
        description += f"{key}: {round(float(val.m), 1)}\n"

    return description


