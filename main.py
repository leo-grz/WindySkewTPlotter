# from src.skewt_plot import create_skewt_plot
# from src.data_processing import extract_windy_temps
# from src.data_processing import load_json_data
from src import *
import sys

def main():

    config = load_json_data()
    skewt_config = config['skewt']

    windy_sounding_file = "data\\windy_sounding3.json"

    try:
        windy_sounding = load_json_data(windy_sounding_file)
        pres, temp, dew = extract_windy_temps(windy_sounding)
        create_skewt_plot(pres, temp, dew, skewt_config)
    except FileNotFoundError as e:
        print(e)  # Print or log the error message
        sys.exit(1)  # Exit with a non-zero status code to indicate an error
    except ValueError as e:
        print(e)
        sys.exit(1)

    
   
if __name__ == "__main__":
    main()

