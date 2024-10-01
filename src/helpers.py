
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
