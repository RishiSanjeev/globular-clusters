import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Hide Tkinter root window
Tk().withdraw()

# Prompt user to select a file (Excel or CSV)
filename = askopenfilename(
    title="Select your spreadsheet file",
    filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")]
)

if not filename:
    print("No file selected. Exiting...")
    exit()

# Load data
if filename.endswith(('.xlsx', '.xls')):
    df = pd.read_excel(filename)
else:
    df = pd.read_csv(filename)

# List of variables you want to plot (adjust as needed)
variables_to_plot = [
    'Globular cluster metallicity ([Fe/H])',
    'Globular cluster weight of mean metallicity',
    'Foreground reddening',
    'Visual magnitude of horizontal branch',
    'Apparent visual distance modulus',
    'Integrated cluster visual magnitude',
    'Absolute visual magnitude (cluster luminosity)',
    'Integrated color index of U-B (non-reddening corrected)',
    'Integrated color index of B-V (non-reddening corrected)',
    'Integrated color index of V-R (non-reddening corrected)',
    'Integrated color index of V-I (non-reddening corrected)',
    # 'Integrated cluster light spectral type', # Skipped (non-numeric)
    'Ellipticity (projected of isophotes, e = 1 - b/a)',
    'Heliocentric radial velocity (km/s)',
    'Observational internal uncertainty in radial velocity',
    'Solar neighborhood LSR radial velocity',
    'Central velocity dispersion (km/s)',
    'Observational internal uncertainty in velocity dispersion',
    'King concentration parameter (c)',
    'Core radius (arcmins)',
    'Half-light Radius (pc)',
    'Central surface brightness (visual magnitudes / arcsecond^2)',
    'Central luminosity density (log_10(L⊙/pc^3))',
    'Core relaxation time (log_10(years))',
    'Median relaxation time (log_10(years))',
    'Cluster density (stars/pc^3)',
    'Member star luminosity (watts)',
    'Rotation amplitude (best fit, km s^-1)'
]

# Ensure required columns exist
required_columns = ['Galactic longitude (°)', 'Galactic latitude (°)']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Required column '{col}' not found in your data.")

x = df['Galactic longitude (°)']
y = df['Galactic latitude (°)']

# Plot all variables at once
for var in variables_to_plot:
    if var not in df.columns:
        print(f"Warning: Column '{var}' not found in data. Skipping...")
        continue

    z = df[var]

    # Skip columns with all NaN or non-numeric values
    if z.isnull().all() or not pd.api.types.is_numeric_dtype(z):
        print(f"Skipping '{var}' (all NaN or non-numeric).")
        continue

    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(x, y, z, c=z, cmap='viridis', s=80)
    plt.colorbar(sc, label=var)

    ax.set_xlabel('Galactic Longitude (°)')
    ax.set_ylabel('Galactic Latitude (°)')
    ax.set_zlabel(var)
    ax.set_title(f'3D Plot of {var} vs Galactic Coordinates')

plt.show()

