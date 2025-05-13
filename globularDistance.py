import cv2
import numpy as np
import matplotlib.pyplot as plt

# Constants
c = 3e5  # speed of light in km/s
H0 = 70  # Hubble's constant in km/s/Mpc
rest_wavelength = 656.3  # H-alpha rest wavelength in nm

def extract_spectrum(image_path):
    """Extract spectrum data (intensity vs. wavelength) from a spectrum image."""
    # Read the image (assuming the spectrum is a single channel image)
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Normalize image data (if needed)
    img = img.astype(np.float32)
    img /= img.max()  # Normalize intensity to a range [0, 1]

    # Sum along the rows to get the spectrum (summing intensity across the spectrum)
    spectrum = np.sum(img, axis=0)

    # Assume each column in the image corresponds to a wavelength step (this depends on your image scale)
    wavelength_step = 0.1  # This is an example; adjust based on your image scale
    wavelengths = np.arange(350, 1050, wavelength_step)  # Assuming wavelengths range from 350nm to 1050nm

    return wavelengths, spectrum

def calculate_redshift(wavelengths, spectrum, known_line_wavelength):
    """Calculate the redshift from the spectrum."""
    # Find the peak of the spectrum (or a known spectral line, e.g., H-alpha)
    peak_idx = np.argmax(spectrum)  # Find the index of the maximum intensity in the spectrum
    observed_wavelength = wavelengths[peak_idx]  # The wavelength where the peak occurs

    # Calculate redshift
    z = (observed_wavelength - known_line_wavelength) / known_line_wavelength
    return z, observed_wavelength

def calculate_velocity_from_redshift(z):
    """Calculate velocity using redshift."""
    return z * c

def calculate_distance_from_velocity(v):
    """Calculate distance using Hubble's Law."""
    return v / H0  # in megaparsecs (Mpc)

def plot_spectrum(wavelengths, spectrum, observed_wavelength, known_line_wavelength):
    """Plot the spectrum with annotations for known spectral lines."""
    plt.plot(wavelengths, spectrum)
    plt.axvline(observed_wavelength, color='r', linestyle='--', label=f'Observed: {observed_wavelength:.2f} nm')
    plt.axvline(known_line_wavelength, color='g', linestyle='--', label=f'Rest: {known_line_wavelength} nm')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity')
    plt.legend()
    plt.show()

def main(image_path):
    # Step 1: Extract spectrum from the image
    wavelengths, spectrum = extract_spectrum(image_path)

    # Step 2: Calculate redshift
    z, observed_wavelength = calculate_redshift(wavelengths, spectrum, rest_wavelength)
    print(f"Calculated redshift: {z:.5f}")
    print(f"Observed wavelength: {observed_wavelength:.2f} nm")

    # Step 3: Calculate velocity from redshift
    v = calculate_velocity_from_redshift(z)
    print(f"Calculated velocity: {v:.2f} km/s")

    # Step 4: Calculate distance from velocity using Hubble's Law
    distance = calculate_distance_from_velocity(v)
    print(f"Calculated distance: {distance:.2f} Mpc")

    # Step 5: Plot the spectrum and annotate the lines
    plot_spectrum(wavelengths, spectrum, observed_wavelength, rest_wavelength)

if __name__ == "__main__":
    # Path to the spectrum image
    image_path = 'path_to_your_spectrum_image.png'
    main(image_path)
