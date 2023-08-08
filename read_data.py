import pandas as pd
import glob
from read_data_func import GetResolution, GetLineprofile
# load csv dictionary
file_path_pattern = 'C:/Users/Benjamin Bagi/Documents/Uni/PA Bagi/Files/Aufloesung_*.csv'

resolution = GetResolution(file_path_pattern)

file_path = 'C:/Users/Benjamin Bagi/Documents/Uni/PA Bagi/Files/linienprofil.csv'
GetLineprofile(file_path)