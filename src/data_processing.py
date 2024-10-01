import json
from metpy.units import units
import numpy as np

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
        
def extract_data(data, fields, min_points=5):
    """
    Generic function to extract data from a windy.com JSON sounding.
    
    Args:
    data: dict : The JSON data to extract from.
    fields: list : List of fields to extract (e.g., ['pressure', 'temp', 'dewpoint']).
    min_points: int : Minimum number of points required for the data to be valid.
    pressure_filter: tuple : Range of acceptable pressure values (used for filtering pressure field).
    
    Returns:
    list : A list of lists where each list corresponds to a field's extracted data.
    
    Raises:
    ValueError : If data points are less than `min_points` or mismatched lengths.
    """
    # create empty list for every variable to extract
    extracted_data = [[] for _ in fields]

    # amount of data points in the json file
    data_len = len(data['features'])

    for x in range(data_len):
        properties = data['features'][x]['properties']

        current_values = []
        for field in fields:
            value = properties.get(field)
            current_values.append(value)


        # Check if all values are present
        if all(current_values):
            # Optional filtering by pressure
            if 'pressure' in fields:
                pressure_idx = fields.index('pressure')
                p = current_values[pressure_idx]
                if not (1000 > float(p) > 100):
                    continue  # Skip if pressure is outside the filter range

            for i, value in enumerate(current_values):
                extracted_data[i].append(float(value))

    # Ensure valid data length
    if any(len(data_list) < min_points for data_list in extracted_data) or \
       not all(len(data_list) == len(extracted_data[0]) for data_list in extracted_data):
        raise ValueError('Too few data points or mismatched lengths. Terminating program.')
    
    extracted_data_with_units = add_units(extracted_data, fields)

    return extracted_data_with_units

def add_units(extracted_data, fields):

    """
    """

    default_units = {
        'pressure': units.hPa,
        'temp': units.degK,
        'dewpoint': units.degK,
        'gpheight': units.m,
        'wind_u': units.knots,
        'wind_v': units.knots
    }

    extracted_data_with_units = []

    for i, name in enumerate(fields):
        if name in default_units.keys() and type(extracted_data[i]) == list:
            extracted_data_with_units.append(np.array(extracted_data[i]) * default_units[name])
    
    return extracted_data_with_units