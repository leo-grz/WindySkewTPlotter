from metpy.plots import SkewT
from metpy.plots import Hodograph
from metpy.units import units
import matplotlib.pyplot as plt


def create_skewt_plot(pres, temp, dew, wind_u, wind_v, config, params, fig=None, ax=None):

    '''Takes pressure, temperature, dewpoint and the configuration contents 
    for the skew-t plot and returns a plt-object'''

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
        skew.plot(pres, params['temperatures']['\u03B8e'], c="pink",
                    lw=2, linestyle='solid', label="Equivalent Potential Temperature")

    if skewt_config['functionalities']['show_wb_temp']:
        skew.plot(pres, params['temperatures']['Tw'].to('degC'), c="lightblue",
                    lw=2, linestyle='solid', label="Wet-Bulb Temperature")

    if skewt_config['functionalities']['show_wb_pot_temp']:
        skew.plot(pres, params['temperatures']['\u03B8w'].to('degC'), c="lightblue",
                    lw=2, linestyle='dotted', label="Wet-Bulb Potential Temperature")

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




def create_hodograph_plot(gpheight, wind_u, wind_v, config, ax=None):

    """
    
    """

    hodograph_config = config['hodograph']
    
    if not ax:
        fig = plt.figure(figsize=tuple(hodograph_config['figsize']))
        ax = fig.add_subplot()

    hodo = Hodograph(ax, component_range=hodograph_config['component_range'])
    hodo.plot_colormapped(wind_u, wind_v, gpheight)
    hodo.add_grid(increment=hodograph_config['grid_increment'])

def display_parameters(config, params, fig):

    general = config['param_display']['general']
    x = general['abs_position'][0]
    y = general['abs_position'][1]
    
    def param_block(param_category, category_name):

        category = config['param_display']['categories'][category_name]

        """
        
        """
        cat_x = x + category['rel_position'][0]
        cat_y = y + category['rel_position'][1]

        headline = category['headline']
        unit = category['unit']

        headline_elevation = general['headline_elevation']
        indent = general['indent']
        line_spacing = general['line_spacing']
        key_val_spacing = general['key_val_spacing']

        fig.text(cat_x, cat_y + headline_elevation, headline, fontsize=11, ha='left', va='top')
        for i, (key, val) in enumerate(param_category.items()):
            i += 1
            try:
                key_val_spacing = category['key_val_spacing']
            except KeyError:
                pass


            # create string to display key as headline
            key_text = f"{key}:" 
            fig.text(cat_x + indent , cat_y - i*line_spacing, key_text, fontsize=9, ha='left', va='top')
            
            # create string to display value indented and below the headline, 
            # with corresponding abbreviated units from the config file (handed by display_config variable)
            if category_name == 'points':
                val_text = f"{round(val[1].to('degC'), 1).m}{unit[0]} | {round(val[0].m, 1)}{unit[1]}"
                fig.text(cat_x + indent + key_val_spacing , cat_y - i*line_spacing, val_text, fontsize=9, ha='left', va='top')
            elif category_name == 'temperatures':
                val_text = f"{round(val[0].m, 1)}{unit}"
                fig.text(cat_x + indent + key_val_spacing , cat_y - i*line_spacing, val_text, fontsize=9, ha='left', va='top')
            else:
                val_text = f"{round(float(val.m), 1)}{unit}"
                fig.text(cat_x + indent + key_val_spacing , cat_y - i*line_spacing, val_text, fontsize=9, ha='left', va='top')

    for key in params.keys():
        param_block(params[key], key)


