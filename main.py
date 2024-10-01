from src import *
import sys
from time import perf_counter
import matplotlib.pyplot as plt

def main():

    start_time = perf_counter()

    config = load_json_data()
    config['sounding_file'] = "data\\windy_sounding1.json"
    config['skewt']['title'] = "Sounding Data for windy_sounding3.json: SkewT"
    config['hodograph']['title'] = "Sounding Data for windy_sounding3.json: Hodograph"

    try:
        windy_sounding = load_json_data(config['sounding_file'])

        pres, temp, dew = extract_windy_data(windy_sounding, ['pressure', 'temp', 'dewpoint'])
        create_skewt_plot(pres, temp, dew, config['skewt'])

        gpheight, wind_u, wind_v = extract_windy_data(windy_sounding, ['gpheight', 'wind_u', 'wind_v'])
        create_hodograph_plot(gpheight, wind_u, wind_v, config['hodograph'])

        print(f"Execution time: {perf_counter() - start_time:.4f} seconds")

        plt.tight_layout()
        plt.show()

    except FileNotFoundError as e: # if config- or data file are missing
        print(e) 
        sys.exit(1) 
    except ValueError as e: # if there exist less than 5 data points
        print(e)
        sys.exit(1)
   
if __name__ == "__main__":
    main()

