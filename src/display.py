from metpy.plots import SkewT
from metpy.plots import Hodograph
from metpy.units import units
import matplotlib.pyplot as plt
from matplotlib import gridspec
from .data_processing import extract_relevant_wind_data

wind_data = None


def create_skewt_plot(extracted_data, config, params, fig, gridspec):

    '''
    Creates a Skew-T plot using the provided pressure, temperature, dewpoint, 
    wind components, configuration, and additional parameters.

    Parameters
    ----------
    extracted_data :  dict(pint.Quantity) :  Dict with pint.Quantity values from sounding
    config : dict : Configuration dictionary containing plot settings and functionalities.
    params : dict : Additional parameters used for plotting and displaying (e.g., parcel profile, temperatures).
    fig : matplotlib.figure.Figure : A Matplotlib figure object to plot on.
    gridspec : matplotlib.gridspec.GridSpec, optional : Gridspec to set the position of skew-t in fig.

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

    pres, temp, dew = [extracted_data.get(key, 1) for key in ['pressure', 'temp', 'dewpoint']]

    skewt_config = config['skewt']
    parcel_profile = params['other']['Parcel Profile'].to('degC')

    skew = SkewT(fig, rotation=45, subplot=gridspec)

    skew.plot(pres, temp, 'red', label='Temperature')
    skew.plot(pres, dew, 'blue', label='Dewpoint')
    skew.plot(pres, parcel_profile, 'k', linestyle='--', label='Parcel Trace')

    skew.plot_dry_adiabats(lw=1, linestyle='solid', colors='darkgreen', alpha=0.4)
    skew.plot_moist_adiabats(lw=1, linestyle='dashed', colors='darkgreen', alpha=0.4)
    skew.plot_mixing_lines(lw=1, linestyle='dashed', colors='darkblue', alpha=0.4)

    wind_data = extract_relevant_wind_data(extracted_data, config)
    barb_pres, barb_wind_u, barb_wind_v = [wind_data.get(key, 1) for key in ['pressure', 'wind_u', 'wind_v']]
    skew.plot_barbs(barb_pres, barb_wind_u, barb_wind_v) # <=============== AMOUNT OF FLAGS
        
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
        y = [l[0] for l in params.get('points').values()]
        x = [l[1] for l in params.get('points').values()]
        labels = list(params.get('points').keys())

        # show params as points in plot
        skew.ax.scatter(x, y, marker='x', c='purple', s=50, zorder=5) 

        # Add labels to each point
        for i, label in enumerate(labels):        
            skew.ax.text(x[i] + 1 * units.degK, y[i], label, c='purple',fontsize=8, zorder=5)

    skew.ax.set_xlabel(f'temperature ({units.degC})')
    skew.ax.set_ylabel(f'pressure ({units.hPa})')

    skew.ax.set_xlim(skewt_config['xlim'])
    skew.ax.set_ylim(skewt_config['ylim'])
    skew.ax.grid(skewt_config['grid'])
    skew.ax.set_title(skewt_config['title'])
    if skewt_config['legend']: skew.ax.legend()




def create_hodograph_plot(extracted_data, config, ax):

    '''
    Creates a Hodograph plot using the provided geopotential height, wind components,
    and configuration.

    Parameters
    ----------
    extracted_data :  dict(pint.Quantity) :  Dict with pint.Quantity values from sounding
    config : dict : Configuration dictionary containing plot settings and functionalities.
    ax : matplotlib.axes.Axes : A Matplotlib axes object.

    Returns
    -------
    None

    Functionalities
    ---------------
    - Plots a hodograph with colormapped wind vectors by height.
    - Adds a grid to the hodograph plot based on the configured grid increment.
    - Reduces amount of displayed datapoints to the measurements at pressure levels derived from config.
    '''

    # hodograph becomes messy if too many measurements are drawn

    wind_data = extract_relevant_wind_data(extracted_data, config)
    pres, wind_u, wind_v = [wind_data.get(key, 1) for key in ['pressure', 'wind_u', 'wind_v']]
    hodograph_config = config['hodograph']

    hodo = Hodograph(ax, component_range=hodograph_config['component_range'])
    hodo.plot_colormapped(wind_u, wind_v, pres)
    hodo.add_grid(increment=hodograph_config['grid_increment'])

def display_parameters(config, params, fig, sounding_properties=None):

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
    # removing the 'other' category, since it shouldn't be displayed
    if 'other' in params.keys():
        params.popitem()
        
    general = config['text_display']['general']
    x, y = general['abs_position']
    
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
        def on_hover(event):

            for text, full_text, short_text in text_elements:
                if text.contains(event)[0]:  # Check if mouse is over the text
                    text.set_text(full_text)  # Set to full text on hover
                    fig.canvas.draw_idle()    # Redraw canvas
                else:
                    text.set_text(short_text)  # Revert to short text when not hovering
                    fig.canvas.draw_idle()
        text_elements = []

        category = config['text_display']['categories'][category_name]

        cat_x = x + category.get('rel_position', 0)[0]
        cat_y = y + category.get('rel_position', 0)[1]
                                   
        keys = ['headline_elevation', 'indent', 'line_spacing', 'unit', 'headline', 
                    'key_val_spacing', 'text_fontsize', 'hl_fontsize' ]
        headline_elevation, indent, line_spacing, unit, headline, key_val_spacing, \
                    text_fontsize, hl_fontsize = [category.get(key, general[key]) for key in keys]

        fig.text(cat_x, cat_y + headline_elevation, headline, fontsize=hl_fontsize, ha='left', va='top')
        for i, (key, val) in enumerate(param_category.items(), start=1):

            # create string to display key as headline
            key_text = f'{key}:' 
            fig.text(cat_x + indent , cat_y - i*line_spacing, key_text, fontsize=text_fontsize, ha='left', va='top')
            
            # create string to display value indented and below the headline, 
            # with corresponding abbreviated units from the config file
            if category_name == 'points':
                val_text = f'{round(val[1].to('degC'), 1).m}{unit[0]} | {round(val[0].m, 1)}{unit[1]}'
            elif category_name == 'temperatures':
                val_text = f'{round(val[0].m, 1)}{unit}'
            elif category_name == 'sounding_properties':

                if len(str(val)) >= 20:
                    # to extend text on hovering over it, if its so long that it would overlap with the skewt
                    short_text, full_text = str(val)[0:15] + '...', val
                    text = fig.text(cat_x + indent + key_val_spacing , cat_y - i*line_spacing, short_text, fontsize=text_fontsize, ha='left', va='top')
                    text_elements += [(text, full_text, short_text)]
                    continue

                val_text = f'{val}'
            else:
                val_text = f'{round(float(val.m), 1)}{unit}'

            fig.text(cat_x + indent + key_val_spacing , cat_y - i*line_spacing, val_text, fontsize=text_fontsize, ha='left', va='top')
        if category_name == 'sounding_properties':
            fig.canvas.mpl_connect("motion_notify_event", on_hover)

    for category_name, category_params in params.items():
        param_block(category_name, category_params)

    if sounding_properties:
        param_block('sounding_properties', sounding_properties)




def plot_extracted_data(extracted_data, config):
    default_ranges = config['default_ranges']

    '''
    documentation missing
    '''

    for key, val in extracted_data.items():
        print(f'{key}: [{min(val).m}, {max(val).m}], LENGTH: {len(val)} | should be in range: {default_ranges[key]}')

    def add_subplot(gs, attrib):
        ax = fig.add_subplot(gs)
        # add data plot
        ax.plot(range(1, len(extracted_data[attrib])+1),extracted_data[attrib], c='blue')
        # add minimum from range
        ax.plot(range(1, len(extracted_data[attrib])+1), [default_ranges[attrib][0]
                    for x in range(len(extracted_data[attrib]))], c='red')
        # add maximum from range
        ax.plot(range(1, len(extracted_data[attrib])+1), [default_ranges[attrib][1] 
                    for x in range(len(extracted_data[attrib]))], c='red')
        ax.set_xlabel('index')
        ax.set_ylabel(f'{attrib} ({extracted_data[attrib].units})')
        ax.grid(True)

    fig = plt.figure(figsize=(10, 8))
    gs = gridspec.GridSpec(3, 2, wspace=0.3, hspace=0.3)  # 3 rows, 2 columns

    add_subplot(gs[0, 0], 'pressure')
    add_subplot(gs[0, 1], 'gpheight')
    add_subplot(gs[1, 0], 'temp')
    add_subplot(gs[1, 1], 'dewpoint')
    add_subplot(gs[2, 0], 'wind_u')
    add_subplot(gs[2, 1], 'wind_v')

    # plt.show()
