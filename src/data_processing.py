from metpy.units import units
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
import numpy as np
import json
from matplotlib import gridspec

def load_json_data(filepath='src/config.json'):

    '''
    Generic function to load data from a JSON file

    Paramters
    ---------
    filepath : string : Path to the JSON file to load. 
        Per default the 'src/config.json' is loaded if no other filepath is given
    
    Returns
    -------
    dict : JSON contents of specified file.
    '''
    
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
        
    except FileNotFoundError as e:
        raise FileNotFoundError(f'File \'{filepath}\' not found. Terminating program.') from e
        
def extract_data(data, fields, min_points=5):
    
    '''
    Function to extract data from a windy.com JSON sounding.
    
    Paramters
    ---------
    data: dict : The JSON data to extract from.
    fields: list : List of fields to extract (e.g., ['pressure', 'temp', 'dewpoint']).
    min_points: int : Minimum number of points required for the data to be valid.
    pressure_filter: tuple : Range of acceptable pressure values (used for filtering pressure field).
    
    Returns
    -------
    dict : A dictionary of lists where each list corresponds to a field's extracted data.
    
    Raises
    ------
    ValueError : If data points are less than `min_points` or mismatched lengths.
    '''

    extracted_data = {field: [] for field in fields}  # Using a dictionary for clarity

    for feature in data['features']:
        properties = feature['properties']

        current_values = [properties.get(field) for field in fields]

        if all(current_values):
            if 'pressure' in fields and not (1000 > float(current_values[fields.index('pressure')]) > 100):
                continue  # Skip based on pressure filtering

            for i, field in enumerate(fields):
                extracted_data[field].append(float(current_values[i]))

    # Ensure data validity
    # check needed?
    if any(len(values) < min_points for values in extracted_data.values()) or \
       not all(len(values) == len(extracted_data[fields[0]]) for values in extracted_data.values()):
        raise ValueError('Too few data points or mismatched lengths.')
        
    return extracted_data

def clean_extracted_data(extracted_data, default_ranges):
    # indices_to_remove = {key: [] for key in extracted_data.keys()}

    # print(f'Indices to remove: {indices_to_remove}')

    return extracted_data # return cleaned data

def plot_extracted_data(extracted_data, default_ranges):

    '''
    documentation missing
    '''

    def add_subplot(gs, attrib):
        ax = fig.add_subplot(gs)
        ax.plot(range(1, len(extracted_data[attrib])+1),extracted_data[attrib])
        ax.plot(range(1, len(extracted_data[attrib])+1), [default_ranges[attrib][0] for x in range(len(extracted_data[attrib]))], c='red')
        ax.plot(range(1, len(extracted_data[attrib])+1), [default_ranges[attrib][1] for x in range(len(extracted_data[attrib]))], c='red')
        ax.set_xlabel('index')
        ax.set_ylabel(attrib)
        ax.grid(True)

    for key, val in extracted_data.items():
        print(f'{key}: [{min(val)}, {max(val)}], LENGTH: {len(val)} | should be in range: {default_ranges[key]}')

    fig = plt.figure(figsize=(10, 8))
    gs = gridspec.GridSpec(3, 2, wspace=0.3, hspace=0.3)  # 3 rows, 2 columns

    add_subplot(gs[0, 0], 'pressure')
    add_subplot(gs[0, 1], 'temp')
    add_subplot(gs[1, 0], 'dewpoint')
    add_subplot(gs[1, 1], 'gpheight')
    add_subplot(gs[2, 0], 'wind_u')
    add_subplot(gs[2, 1], 'wind_v')

    plt.show()


    for key, values in extracted_data.items():
        if key in default_ranges:
            min_val, max_val = default_ranges[key]
            for idx, value in enumerate(values):
                if not min_val <= value <= max_val:
                    indices_to_remove[key].append(idx)


        
    return extracted_data

def add_units(extracted_data):

    '''
    Function to add pint.Quantity (metpy.units) to a dataset retreived by the extract_data function.

    Parameters
    ----------
    extracted_data :  dict(list) :  Dict with pint.Quantity values from sounding

    Returns
    -------
    list : list of numpy arrays with corresponding units attatched
    '''

    default_units = {
        'pressure': units.hPa,
        'temp': units.degK,
        'dewpoint': units.degK,
        'gpheight': units.m,
        'wind_u': units.knots,
        'wind_v': units.knots
    }
    return {key: np.array(val) * default_units[key] for key, val in extracted_data.items()}


def calc_params(extracted_data):
    
    '''
    Function to calculate meteorological parameters like points (lcl, lfc...), 
    cape & cin, indices, temperatures and parcel profile
    for plotting, displaying and further analysis in the matplotlib fig.

    Parameters
    ----------
    extracted_data :  dict(pint.Quantity) :  Dict with pint.Quantity values from sounding

    Returns
    -------
    dict : Contains all calculated temperatures, indices, points and quantities
    '''

    pres = extracted_data.get('pressure', 1)
    temp = extracted_data.get('temp', 1)
    dew = extracted_data.get('dewpoint', 1)

    parcel_profile = mpcalc.parcel_profile(pres, temp[0], dew[0])
    cape, cin = mpcalc.cape_cin(pres, temp, dew, parcel_profile)

    params = {
        'points': {
            'LCL': mpcalc.lcl(pres[0], temp[0], dew[0]),
            'LFC': mpcalc.lfc(pres, temp, dew),
            'EL': mpcalc.el(pres, temp, dew),
            'CCL': mpcalc.ccl(pres, temp, dew)[:2]  # Extracted only necessary values
        },
        'cape_cin': {
            'CAPE': cape,
            'CIN': cin
        },
        'temperatures': {
            '\u03B8e': mpcalc.equivalent_potential_temperature(pres, temp, dew),
            'Tw': mpcalc.wet_bulb_temperature(pres, temp, dew),
            '\u03B8w': mpcalc.wet_bulb_potential_temperature(pres, temp, dew)
        },
        'indices': {
            'Lifted Index': mpcalc.lifted_index(pres, temp, parcel_profile),
            'K Index': mpcalc.k_index(pres, temp, dew),
            'Total Totals Index': mpcalc.total_totals_index(pres, temp, dew),
            'Showalter Index': mpcalc.showalter_index(pres, temp, dew)
        },
        'other': {
            'Parcel Profile': parcel_profile
        }
    }

    return params