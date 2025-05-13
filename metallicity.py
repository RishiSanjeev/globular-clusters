#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# metallicity.py
# Author: Rishi Sanjeev
# Created: 5-6-2025
# Description: Calculates metallicity from spectrum data.

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import ascii
from astropy import units as u
from specutils import Spectrum1D
from specutils.analysis import equivalent_width

"""
spectrum.csv - example
first column: wavelength in Angstroms
second column: flux
"wavelength,flux" header necessary

wavelength,flux
5150.0,1.01
5151.0,0.99
...
5339.0,1.00
"""

# === Load spectrum ===
filename = "spectrum.csv"
data = ascii.read(filename)
wavelength = data['wavelength'] * u.AA
flux = data['flux'] * u.Unit("erg / (s cm^2 Angstrom)")
spectrum = Spectrum1D(spectral_axis=wavelength, flux=flux)

# === Normalize ===
continuum_region = (wavelength > 5150*u.AA) & (wavelength < 5190*u.AA)
continuum_flux = np.median(flux[continuum_region])
normalized_flux = flux / continuum_flux
spectrum = Spectrum1D(spectral_axis=wavelength, flux=normalized_flux)

# === Fe I lines for [Fe/H] estimation ===
fe_lines = [
    ("Fe I", 5270, 3),
    ("Fe I", 5335, 3),
]

ews = []
print("Fe I Line Equivalent Widths:")
for name, center, width in fe_lines:
    region = [(center - width) * u.AA, (center + width) * u.AA]
    try:
        ew = equivalent_width(spectrum, regions=region)
        ews.append(ew.value)  # Save in Å
        print(f"{name} {center} Å: {ew:.3f}")
    except Exception as e:
        print(f"{name} {center} Å: Error - {e}")

# === Estimate metallicity [Fe/H] ===
if len(ews) >= 1:
    avg_ew = np.mean(ews)
    print(f"\nAverage Fe I EW: {avg_ew:.3f} Å")

    # === Assumed stellar parameters ===
    Teff = 5800  # K (e.g. Sun-like)
    logg = 4.4   # cgs

    # === Empirical formula (simplified version) ===
    # Based on made-up coefficients for illustrative use
    # [Fe/H] = a * EW + b * logg + c * log(Teff) + d
    a, b, c, d = 2.0, -0.3, -5.0, 10.0
    logTeff = np.log10(Teff)
    feh = a * avg_ew + b * logg + c * logTeff + d

    print(f"\nEstimated [Fe/H] ≈ {feh:.2f}")
else:
    print("Not enough valid Fe I lines to estimate metallicity.")