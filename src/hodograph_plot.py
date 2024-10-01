
from metpy.plots import Hodograph
from metpy.units import units
import metpy.calc as mpcalc
import matplotlib.pyplot as plt
import numpy as np

def create_hodograph_plot(gpheight, wind_u, wind_v, hodograph_config):

    gpheight = np.array(gpheight) * units.m
    wind_u = np.array(wind_u) * units.knots
    wind_v = np.array(wind_v) * units.knots
    
    fig = plt.figure(figsize=tuple(hodograph_config['figsize']))
    ax = fig.add_subplot()


    hodo = Hodograph(ax, component_range=hodograph_config['component_range'])
    
    hodo.plot_colormapped(wind_u, wind_v, gpheight)

    hodo.add_grid(increment=10)
    return ax

