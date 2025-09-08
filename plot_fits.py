import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import os

# Define file paths for the FITS files
file_paths = {
    'Stokes I': r"C:\Users\anagha rajesh\Downloads\3C75_final_large.pbcor_cropped.fits",
    'Stokes Q': r"C:\Users\anagha rajesh\Downloads\3C75_final.Q_02_cropped.fits",
    'Stokes U': r"C:\Users\anagha rajesh\Downloads\3C75_final.U_02_cropped.fits",
    'Stokes V': r"C:\Users\anagha rajesh\Downloads\3C75_final.V_02_cropped.fits"
}

# Folder to save images
output_folder = r"C:\Users\anagha rajesh\Desktop\RMtoolsTest\fits data images"
os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn't exist

# Load data from FITS files
fits_data = {}
for stokes, path in file_paths.items():
    with fits.open(path) as hdul:
        data = hdul[0].data
        fits_data[stokes] = data

# Plot and save individual Stokes images
for stokes, data in fits_data.items():
    plt.imshow(data[0, 0, :, :], origin='lower', cmap='inferno')
    plt.title(stokes)
    plt.colorbar(label='Surface Brightness')
    plt.savefig(os.path.join(output_folder, f"{stokes.replace(' ', '_')}.png"))
    plt.close()

# Calculate Polarized Intensity (P) and Polarization Angle
Q = fits_data['Stokes Q'][0, 0, :, :]
U = fits_data['Stokes U'][0, 0, :, :]
P = np.sqrt(Q**2 + U**2)
pol_angle = 0.5 * np.arctan2(U, Q) * (180 / np.pi)

# Plot and save Polarized Intensity
plt.imshow(P, origin='lower', cmap='viridis')
plt.title('Polarized Intensity (P)')
plt.colorbar(label='Polarized Intensity')
plt.savefig(os.path.join(output_folder, "Polarized_Intensity.png"))
plt.close()

# Plot and save Polarization Angle
plt.imshow(pol_angle, origin='lower', cmap='twilight')
plt.title('Polarization Angle (degrees)')
plt.colorbar(label='Angle (deg)')
plt.savefig(os.path.join(output_folder, "Polarization_Angle.png"))
plt.close()

print("All images have been saved to:", output_folder)
