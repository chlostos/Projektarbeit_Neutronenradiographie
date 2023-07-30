import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def get_resolution(df):
    # Choose the column to represent the edge (e.g., "Gray" column for intensity values)
    x_data = df['Distance(um)'].values  # x-values (position along the edge)
    y_data = df['Gray'].values  # y-values (intensity values)

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
    plt.plot(x_data, y_data, marker='o', linestyle='', label='Measurement')
    plt.plot(x_data, esf_model(x_data, *popt), linestyle='--', label='Fit (ESF)')
    plt.xlabel('Pixels (25 µm)')
    plt.ylabel('Counts')
    plt.title('Distance - Intensity Curve with Fit')
    plt.legend()
    plt.grid(True)
    plt.show()

    return fwhm_resolution