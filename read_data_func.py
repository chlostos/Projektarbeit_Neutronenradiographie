import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from scipy.optimize import curve_fit

def get_Esf(df):
    # Choose the column to represent the edge (e.g., "Gray" column for intensity values)
    x_data = df['Distance(um)'].values  # x-values (position along the edge)
    y_data = df['Gray'].values  # y-values (intensity values)
    X_data = df['Point'].values
    # Function for Edge Spread Function (ESF)
    def esf_model(x, p1, p2, p3, λ):
        return p1 + p2 * np.arctan(λ * (x - p3))

    # Perform the curve fit using the ESF model
    popt, _ = curve_fit(esf_model, x_data, y_data, p0=[y_data.min(), y_data.max()-y_data.min(), x_data.mean(), 0.01])

    # Extract the value of λ from the curve fit
    λ_fit = popt[3]

    # Calculate the FWHM resolution using the equation: FWHM(x) ≡ (2/λ)
    fwhm_resolution = 2 / λ_fit

    # Plot the Distance - Intensity curve with the fit curve (without lines connecting data points)
    plt.plot(X_data, y_data, marker='o', linestyle='', label='Measurement')
    plt.plot(X_data, esf_model(x_data, *popt), linestyle='--', label='Fit (ESF)')

    # Set the X-Achse auf 2er Schritte
    x_locator = MultipleLocator(base=2)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_locator)

    plt.xlabel('Pixels (25 µm)')
    plt.ylabel('Counts')
    plt.legend()
    plt.grid(False)
    plt.show()

    return fwhm_resolution

def GetResolution(file_path_pattern):
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
    df_mean = combined_df.groupby(['Point', 'X(um)', 'Y(um)', 'Distance(um)', 'Gray'], as_index=False).mean()

    # Gruppieren nach der 'Point'-Spalte und Berechnung des Mittelwerts für andere Spalten
    mean_df = df_mean.groupby('Point', as_index=False).mean()

    resolution = get_Esf(mean_df)

    print(f'Resolution: {resolution} µm')

    return resolution

def get_lineprofile(df):
    # Choose the column to represent the edge (e.g., "Gray" column for intensity values)
    x_data = df['Distance(um)'].values  # x-values (position along the edge)
    y_data = df['Gray'].values  # y-values (intensity values)

    # Plot the Distance - Intensity curve with the fit curve for the selected range
    plt.plot(x_data, y_data, marker='o', linestyle='', label='Measurement')

    # Set the X-Achse auf 20tsd.-er Schritte
    x_locator = MultipleLocator(base=20000)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_locator)

    plt.xlabel('Distance(µm)')
    plt.ylabel('Counts')
    plt.ylim(30000, 60000)
    plt.legend()
    plt.grid(True)
    plt.show()

def GetLineprofile(file_path):

    csv_file = (file_path)
    # Create an empty list to store DataFrames
    df = pd.read_csv(csv_file, sep=';')

    get_lineprofile(df)


