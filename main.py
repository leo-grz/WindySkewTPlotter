from src import *
import sys
from time import perf_counter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def main():

    start_time = perf_counter()

    config = load_json_data()
    config['sounding_file'] = 'data/windy_sounding4.json'

    # try:

    windy_sounding = load_json_data(config['sounding_file'])

    attributes = ['pressure', 'temp', 'dewpoint', 'gpheight', 'wind_u', 'wind_v']
    extracted_data = extract_data(windy_sounding, attributes)
    

    extracted_data = clean_extracted_data(extracted_data, config['default_ranges'])

    extracted_data = add_units(extracted_data)
        
    plot_extracted_data(extracted_data, config)

    
    params = calc_params(extracted_data)

    fig = plt.figure(figsize=tuple(config['figsize']))
    gs = gridspec.GridSpec(10, 15)
    
    gs_skewt = gs[:, 0:10]
    ax_hodograph = fig.add_subplot(gs[0:5, 10:15]) # hodograph ax

    create_skewt_plot(extracted_data, config, params, fig, gs_skewt)
    create_hodograph_plot(extracted_data, config, ax_hodograph)


    # for display_parameters function, 
    # to omit the 'others' category in params, since parcel trace shouldn't be displayed
    params.popitem() 
    display_parameters(config, params, fig)# there must be a better solution


    print(f'Execution time: {perf_counter() - start_time:.4f} seconds')

    plt.title(config['sounding_file'])
    plt.show()

    # except FileNotFoundError as e: # if config- or data file are missing
    #     print(e.with_traceback) 
    #     sys.exit(1) 
    # except ValueError as e: # if there exist less than 5 data points
    #     print(e.with_traceback)
    #     sys.exit(1)
   
if __name__ == '__main__':
    main()