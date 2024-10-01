from src import *
import sys
from time import perf_counter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def main():

    start_time = perf_counter()

    config = load_json_data()
    config['sounding_file'] = "data\\windy_sounding3.json"

    try:

        fig = plt.figure(figsize=tuple(config['figsize']))
        gs = gridspec.GridSpec(10, 15)
        
        ax1 = fig.add_subplot(gs[:, 0:10]) # skewt ax
        ax2 = fig.add_subplot(gs[0:5, 10:15]) # hodograph ax

        windy_sounding = load_json_data(config['sounding_file'])

        pres, temp, dew, gpheight, wind_u, wind_v = extract_data(windy_sounding, 
                    ['pressure', 'temp', 'dewpoint', 'gpheight', 'wind_u', 'wind_v'])

        create_skewt_plot(pres, temp, dew, config, wind_u, wind_v, fig, ax1)
        create_hodograph_plot(gpheight, wind_u, wind_v, config, ax2)

        print(f"Execution time: {perf_counter() - start_time:.4f} seconds")

        plt.title(config['sounding_file'])
        #plt.tight_layout()
        plt.show()

    except FileNotFoundError as e: # if config- or data file are missing
        print(e) 
        sys.exit(1) 
    except ValueError as e: # if there exist less than 5 data points
        print(e)
        sys.exit(1)
   
if __name__ == "__main__":
    main()