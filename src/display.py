from metpy.plots import SkewT
from metpy.plots import Hodograph
from metpy.units import units
import matplotlib.pyplot as plt


def create_skewt_plot(extracted_data, config, params, fig=None, ax=None):

    '''
    Creates a Skew-T plot using the provided pressure, temperature, dewpoint, 
    wind components, configuration, and additional parameters.

    Parameters
    ----------
    extracted_data :  dict(pint.Quantity) :  Dict with pint.Quantity values from sounding
    config : dict : Configuration dictionary containing plot settings and functionalities.
    params : dict : Additional parameters used for plotting and displaying (e.g., parcel profile, temperatures).
    fig : matplotlib.figure.Figure, optional: 
        A Matplotlib figure object to plot on. If None, a new figure is created.
    ax : matplotlib.axes.Axes, optional : 
        A Matplotlib axes object. If None, a new axis is created.

    Returns
    -------
    None
    
    Functionalities
    ---------------
    - Plots temperature, dewpoint, and parcel profile.
    - Plots dry adiabats, moist adiabats, and mixing lines.
    - Optionally adds equivalent potential temperature, wet-bulb temperature, 
      and wet-bulb potential temperature.
    - Shades CAPE and CIN areas if enabled.
    - Displays custom parameters as points with labels on the plot.
    '''

    pres = extracted_data.get('pressure', 1)
    temp = extracted_data.get('temp', 1)
    dew = extracted_data.get('dewpoint', 1)
    wind_u = extracted_data.get('wind_u', 1)
    wind_v = extracted_data.get('wind_v', 1)

    skewt_config = config['skewt']
    parcel_profile = params['other']['Parcel Profile'].to('degC')

    if not fig or not ax:
        fig = plt.figure(figsize=tuple(skewt_config['figsize']))
        skew = SkewT(fig, rotation=45)
    else:
        skew = SkewT(fig, rotation=45, subplot=ax)

    skew.plot(pres, temp, 'red', label='Temperature')
    skew.plot(pres, dew, 'blue', label='Dewpoint')
    skew.plot(pres, parcel_profile, 'k', linestyle='--', label='Parcel Trace')

    skew.plot_dry_adiabats(lw=1, linestyle='solid', colors='darkgreen', alpha=0.4)
    skew.plot_moist_adiabats(lw=1, linestyle='dashed', colors='darkgreen', alpha=0.4)
    skew.plot_mixing_lines(lw=1, linestyle='dashed', colors='darkblue', alpha=0.4)

    skew.plot_barbs(pres, wind_u, wind_v)
        
    # adding temperatures
    if skewt_config['functionalities']['show_equiv_pot_temp']:
        skew.plot(pres, params['temperatures']['\u03B8e'], c='pink',
                    lw=2, linestyle='solid', label='Equivalent Potential Temperature')

    if skewt_config['functionalities']['show_wb_temp']:
        skew.plot(pres, params['temperatures']['Tw'].to('degC'), c='lightblue',
                    lw=2, linestyle='solid', label='Wet-Bulb Temperature')

    if skewt_config['functionalities']['show_wb_pot_temp']:
        skew.plot(pres, params['temperatures']['\u03B8w'].to('degC'), c='lightblue',
                    lw=2, linestyle='dotted', label='Wet-Bulb Potential Temperature')

    # adding CAPE and CIN area to plot
    if skewt_config['functionalities']['show_cape_cin']:
        skew.shade_cape(pres, temp, parcel_profile)
        skew.shade_cin(pres, temp, parcel_profile)

    # show parameters as points in plot
    if skewt_config['functionalities']['show_params']:
        y = [l[0] for l in params['points'].values()]
        x = [l[1] for l in params['points'].values()]
        labels = list(params['points'].keys())

        # show params as points in plot
        skew.ax.scatter(x, y, marker='x', c='purple', s=50, zorder=5) 

        # Add labels to each point
        for i, label in enumerate(labels):        
            skew.ax.text(x[i] + 1 * units.degK, y[i], label, c='purple',fontsize=8, zorder=5)

    skew.ax.set_xlim(skewt_config['xlim'])
    skew.ax.set_ylim(skewt_config['ylim'])
    skew.ax.grid(skewt_config['grid'])
    skew.ax.set_title(skewt_config['title'])
    if skewt_config['legend']: skew.ax.legend()




def create_hodograph_plot(extracted_data, config, ax=None):

    '''
    Creates a Hodograph plot using the provided geopotential height, wind components,
    and configuration.

    Parameters
    ----------
    extracted_data :  dict(pint.Quantity) :  Dict with pint.Quantity values from sounding
    config : dict : Configuration dictionary containing plot settings and functionalities.
    ax : matplotlib.axes.Axes, optional : 
        A Matplotlib axes object. If None, a new axis is created.

    Returns
    -------
    None

    Functionalities
    ---------------
    - Plots a hodograph with colormapped wind vectors by height.
    - Adds a grid to the hodograph plot based on the configured grid increment.
    '''

    gpheight = extracted_data.get('gpheight', 1)
    wind_u = extracted_data.get('wind_u', 1)
    wind_v = extracted_data.get('wind_v', 1)

    hodograph_config = config['hodograph']
    
    if not ax:
        _, ax = plt.subplots(figsize=tuple(hodograph_config['figsize']))

    hodo = Hodograph(ax, component_range=hodograph_config['component_range'])
    hodo.plot_colormapped(wind_u, wind_v, gpheight)
    hodo.add_grid(increment=hodograph_config['grid_increment'])

def display_parameters(config, params, fig):

    '''
    Displays meteorological parameters on the given figure based on provided 
    configuration and parameters.

    Parameters
    ----------
    config : dict : Configuration dictionary containing parameter display settings.
    params : dict : Meteorological parameters to display (e.g., temperatures, points).
    fig : matplotlib.figure.Figure : The Matplotlib figure object where parameters are displayed.

    Returns
    -------
    None

    Functionalities
    ---------------
    - Displays categories of parameters with headlines, units, and values.
    - Custom positioning and formatting of parameter blocks according to config.
    '''
        
    general = config['param_display']['general']
    x, y = general['abs_position']
    headline_elevation = general['headline_elevation']
    indent = general['indent']
    line_spacing = general['line_spacing']
    
    def param_block(category_name, param_category):
        '''
        Helper function to display a block of parameters within a specific category 
        (e.g., points, temperatures) on the figure.

        Parameters
        ----------
        param_category : dict : The parameters to be displayed in the specific category.
        category_name : str : The name of the parameter category (e.g., 'points', 'temperatures').

        Returns
        -------
        None

        Functionalities
        ---------------
        - Displays each parameter with a key-value pair and corresponding units.
        - Custom formatting based on the category's configuration.
        '''

        category = config['param_display']['categories'][category_name]

        cat_x = x + category['rel_position'][0]
        cat_y = y + category['rel_position'][1]
        unit = category['unit']
        headline = category['headline']
        
        try:
            key_val_spacing = category['key_val_spacing']
        except KeyError:
            key_val_spacing = general['key_val_spacing']



        fig.text(cat_x, cat_y + headline_elevation, headline, fontsize=11, ha='left', va='top')
        for i, (key, val) in enumerate(param_category.items(), start=1):

            # create string to display key as headline
            key_text = f'{key}:' 
            fig.text(cat_x + indent , cat_y - i*line_spacing, key_text, fontsize=9, ha='left', va='top')
            
            # create string to display value indented and below the headline, 
            # with corresponding abbreviated units from the config file
            if category_name == 'points':
                val_text = f'{round(val[1].to('degC'), 1).m}{unit[0]} | {round(val[0].m, 1)}{unit[1]}'
            elif category_name == 'temperatures':
                val_text = f'{round(val[0].m, 1)}{unit}'
            else:
                val_text = f'{round(float(val.m), 1)}{unit}'

            fig.text(cat_x + indent + key_val_spacing , cat_y - i*line_spacing, val_text, fontsize=9, ha='left', va='top')

    for category_name, category_params in params.items():
        param_block(category_name, category_params)


