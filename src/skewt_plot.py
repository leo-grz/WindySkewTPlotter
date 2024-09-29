from .data_processing import load_json_data
from .data_processing import extract_windy_temps

from metpy.plots import SkewT
from metpy.units import units
import metpy.calc as mpcalc
import matplotlib.pyplot as plt
import numpy as np


def create_skewt_plot(pres, temp, dew, skewt_config):


    temp = np.array(temp) * units.degK
    dew = np.array(dew) * units.degK
    pres = np.array(pres) * units.hPa

    if len(temp) < 5:
        raise ValueError('Too few data points. Terminating program.')
    
    
    fig = plt.figure(figsize=tuple(skewt_config['figsize']))
    skew = SkewT(fig, rotation=45)

    skew.plot(pres, temp, 'red')
    skew.plot(pres, dew, 'blue')
    parcel_prof = mpcalc.parcel_profile(pres, temp[0], dew[0]).to('degC')
    skew.plot(pres, parcel_prof, 'k', linestyle='--')

    skew.plot_dry_adiabats(lw=1, linestyle='solid', colors='darkgreen')
    skew.plot_moist_adiabats(lw=1, linestyle='dashed', colors='darkgreen')
    skew.plot_mixing_lines(lw=1, linestyle='dashed', colors='darkblue')

    skew.ax.set_xlim(skewt_config['xlim'])
    skew.ax.set_ylim(skewt_config['ylim'])
    skew.ax.grid(skewt_config['grid'])
    plt.title(skewt_config['title'])
    plt.show()
