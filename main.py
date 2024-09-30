from src import *
import sys
from time import perf_counter

def main():

    start_time = perf_counter()

    config = load_json_data()
    config['sounding_file'] = "data\\windy_sounding3.json"
    config['skewt']['title'] = "Sounding Data for windy_sounding3.json "

    try:
        windy_sounding = load_json_data(config['sounding_file'])
        pres, temp, dew = extract_windy_temps(windy_sounding)

        plot = create_skewt_plot(pres, temp, dew, config['skewt'])
        print(f"Execution time: {perf_counter() - start_time:.4f} seconds")

        plot.show()

    except FileNotFoundError as e: # if config- or data file are missing
        print(e) 
        sys.exit(1) 
    except ValueError as e: # if there exist less than 5 data points
        print(e)
        sys.exit(1)

    
   
if __name__ == "__main__":
    main()

