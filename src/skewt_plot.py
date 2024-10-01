from .plot_helpers import *

from metpy.plots import SkewT
from metpy.units import units
import metpy.calc as mpcalc
import matplotlib.pyplot as plt
import numpy as np


def create_skewt_plot(pres, temp, dew, skewt_config):

    '''Takes pressure, temperature, dewpoint and the configuration contents 
    for the skew-t plot and returns a plt-object'''

    pres = np.array(pres) * units.hPa
    temp = np.array(temp) * units.degK
    dew = np.array(dew) * units.degK

    fig = plt.figure(figsize=tuple(skewt_config['figsize']))
    skew = SkewT(fig, rotation=45)

    skew.plot(pres, temp, 'red', label='Temperature')
    skew.plot(pres, dew, 'blue', label='Dewpoint')
    parcel_prof = mpcalc.parcel_profile(pres, temp[0], dew[0]).to('degC')
    skew.plot(pres, parcel_prof, 'k', linestyle='--', label='Parcel Trace')

    skew.plot_dry_adiabats(lw=1, linestyle='solid', colors='darkgreen', alpha=0.4)
    skew.plot_moist_adiabats(lw=1, linestyle='dashed', colors='darkgreen', alpha=0.4)
    skew.plot_mixing_lines(lw=1, linestyle='dashed', colors='darkblue', alpha=0.4)

    # Calculating parameters
    params = calc_params(pres, temp, dew, parcel_prof)

    # adding list of parameters to the side of plot
    if skewt_config['functionalities']['description']:
        description = create_description(params)
        skew.ax.text(1.02, 0.9, description, transform=skew.ax.transAxes, 
                     fontsize=10, color='black', va='top', ha='left')
        
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
        skew.ax.fill_betweenx(pres, temp, parcel_prof, 
                    where=parcel_prof > temp, 
                    facecolor='orange', alpha=0.5, label='CAPE')
        skew.ax.fill_betweenx(pres, temp, parcel_prof, 
                    where=parcel_prof < temp,
                    facecolor='blue', alpha=0.5, label='CIN')

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
