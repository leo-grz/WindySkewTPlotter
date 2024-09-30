from .data_processing import *

from metpy.plots import SkewT
from metpy.units import units
import metpy.calc as mpcalc
import matplotlib.pyplot as plt
import numpy as np


def create_skewt_plot(pres, temp, dew, skewt_config):

    '''Takes pressure, temperature, dewpoint and the configuration contents 
    for the skew-t plot and returns a plt-object'''

    temp = np.array(temp) * units.degK
    dew = np.array(dew) * units.degK
    pres = np.array(pres) * units.hPa

    if len(temp) < 5: # raise Value error if temperature data contains less than 5 data points
        raise ValueError('Too few data points. Terminating program.')
    
    fig = plt.figure(figsize=tuple(skewt_config['figsize']))
    skew = SkewT(fig, rotation=45)

    skew.plot(pres, temp, 'red', label='Temperature')
    skew.plot(pres, dew, 'blue', label='Dewpoint')
    parcel_prof = mpcalc.parcel_profile(pres, temp[0], dew[0]).to('degC')
    skew.plot(pres, parcel_prof, 'k', linestyle='--', label='Parcel Trace')

    skew.plot_dry_adiabats(lw=1, linestyle='solid', colors='darkgreen', alpha=0.4)
    skew.plot_moist_adiabats(lw=1, linestyle='dashed', colors='darkgreen', alpha=0.4)
    skew.plot_mixing_lines(lw=1, linestyle='dashed', colors='darkblue', alpha=0.4)

    skew.ax.set_xlim(skewt_config['xlim'])
    skew.ax.set_ylim(skewt_config['ylim'])
    skew.ax.grid(skewt_config['grid'])
    plt.title(skewt_config['title'])

    description = "" # description to be displayed at the right side of the plot


    # =====> FUNCTIONALITY: CAPE AND CIN
    cape, cin = mpcalc.cape_cin(pres, temp, dew, parcel_prof)
    description += f"CAPE: {round(cape, 2)}\n"
    description += f"CIN: {round(cin, 2)}\n"

    # Adding CAPE and CIN area to plot if specified in config.json
    if skewt_config['functionalities']['cape_cin']:
        skew.ax.fill_betweenx(pres, temp, parcel_prof, where=parcel_prof > temp,
                        facecolor='orange', alpha=0.5, label='CAPE')
        skew.ax.fill_betweenx(pres, temp, parcel_prof, where=parcel_prof < temp,
                        facecolor='blue', alpha=0.5, label='CIN')
        
    # =====> FUNCTIONALITY: LCL, LCF, EL
    x, y = [], []

    lcl_pres, lcl_temp = mpcalc.lcl(pres[0], temp[0], dew[0])
    lfc_pres, lfc_temp = mpcalc.lfc(pres, temp, dew)
    el_pres, el_temp = mpcalc.el(pres, temp, dew)
    ccl_pres, ccl_temp, ccl_convtemp = mpcalc.ccl(pres, temp, dew)
    x = [lcl_temp, lfc_temp, el_temp, ccl_temp]
    y = [lcl_pres, lfc_pres, el_pres, ccl_pres]
    skew.ax.scatter(x,y, marker='x', c='purple', s=50)

    description += f"LCL: {round(y[0], 2)}\n"
    description += f"LFC: {round(y[1], 2)}\n"
    description += f"EL: {round(y[2], 2)}\n"
    description += f"CCL: {round(y[3], 2)}\n"


    

    skew.ax.text(1.02, 0.9, description, transform=skew.ax.transAxes, fontsize=10, color='black', va='top', ha='left')

    return plt
