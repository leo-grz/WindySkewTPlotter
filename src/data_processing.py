import json

# without argument loads in config parameters
def load_json_data(filepath='src\\config.json'):

    '''This function reads out the contents of a JSON file and returns them in a variable. 
    When no parameter is given, it loads the config data stored in src/config.json'''
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError as e:
        if filepath == 'config.json':
            raise FileNotFoundError(f"The default configuration file ('src\\config.json') couldn't be found. Terminating program.") from e
        else:
            raise FileNotFoundError(f"File '{filepath}' not found. Terminating program.") from e

def extract_windy_temps(data):

    '''This function returns pressure, temperature and dewpoint extracted from the 
    JSON data of a sounding that can be downloaded from windy.com'''

    pres, temp, dew = [], [], []

    data_len = len(data['features'])

    for x in range(data_len):

        properties = data['features'][x]['properties']
        
        p = properties.get('pressure')
        d = properties.get('dewpoint')
        t = properties.get('temp')

        if d and t and (1000 > int(p) > 100):
            pres.append(float(p))
            temp.append(float(t))
            dew.append(float(d))
    
    if (len(temp) < 5) or not (len(pres) == len(temp) == len(dew)): # raise Value error if temperature data contains less than 5 data points
        raise ValueError('Too few data points. Terminating program.')
    

    return pres, temp, dew


