import pandas as pd
import glob
from read_data_func import get_resolution

file_path_pattern = 'C:/Users/Benjamin Bagi/Documents/Uni/PA Bagi/Files/Aufloesung_*.csv'
csv_files = glob.glob(file_path_pattern)

# Create an empty list to store DataFrames
df_list = []

# Loop through each CSV file and read it into a DataFrame
for csv_file in csv_files:
    df = pd.read_csv(csv_file, sep=';')
    df_list.append(df)

# Combine the DataFrames into a single DataFrame using pd.concat()
combined_df = pd.concat(df_list)

# Group the combined DataFrame by 'Point', 'X(um)', 'Y(um)', and calculate the mean for each group
mean_df = combined_df.groupby(['Point', 'X(um)', 'Y(um)','Distance(um)','Gray'], as_index=False).mean()

resolution = get_resolution(mean_df)

print(f'Resolution: {resolution} µm')
