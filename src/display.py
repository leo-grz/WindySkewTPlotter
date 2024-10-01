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

def display_parameters(params, fig):
    description = create_description(params)

    fig.text(0.65, 0.45, description, fontsize=10, ha='left', va='top')


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

