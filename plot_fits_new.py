import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
import os

# Define file paths for the FITS files
file_paths = {
    'Stokes I': r"C:\Users\anagha rajesh\Downloads\3C75_final_large.pbcor_cropped.fits",
    'Stokes Q': r"C:\Users\anagha rajesh\Downloads\3C75_final.Q_02_cropped.fits",
    'Stokes U': r"C:\Users\anagha rajesh\Downloads\3C75_final.U_02_cropped.fits",
    'Stokes V': r"C:\Users\anagha rajesh\Downloads\3C75_final.V_02_cropped.fits"
}

# Output folder to save images
output_folder = r"C:\Users\anagha rajesh\Desktop\RMtoolsTest\fits data images"
os.makedirs(output_folder, exist_ok=True)

# Load data and WCS from FITS files
fits_data = {}
fits_wcs = {}
for stokes, path in file_paths.items():
    with fits.open(path) as hdul:
        data = hdul[0].data[0, 0, :, :]
        header = hdul[0].header
        # Fix WCS to only use spatial dimensions (ignore frequency and stokes axes)
        wcs = WCS(header, naxis=2)
        fits_data[stokes] = data
        fits_wcs[stokes] = wcs

# Plot and save individual Stokes images with RA and Dec axes
for stokes in ['Stokes I', 'Stokes Q', 'Stokes U', 'Stokes V']:
    data = fits_data[stokes]
    wcs = fits_wcs[stokes]

    plt.figure(figsize=(8, 6))
    ax = plt.subplot(projection=wcs)
    im = ax.imshow(data, origin='lower', cmap='inferno')
    ax.set_xlabel('RA (J2000)')
    ax.set_ylabel('Dec (J2000)')
    plt.colorbar(im, label='Surface Brightness (Jy/beam)')
    plt.title(stokes)
    plt.savefig(os.path.join(output_folder, f"{stokes.replace(' ', '_')}_RA_Dec.png"))
    plt.close()

# Calculate Polarized Intensity (P) and Polarization Angle
Q = fits_data['Stokes Q']
U = fits_data['Stokes U']
P = np.sqrt(Q**2 + U**2)
pol_angle = 0.5 * np.arctan2(U, Q) * (180 / np.pi)

# Use WCS from one of the Stokes files (e.g., Stokes Q)
wcs = fits_wcs['Stokes Q']

# Plot and save Polarized Intensity with RA and Dec axes
plt.figure(figsize=(8, 6))
ax = plt.subplot(projection=wcs)
im = ax.imshow(P, origin='lower', cmap='viridis')
ax.set_xlabel('RA (J2000)')
ax.set_ylabel('Dec (J2000)')
plt.colorbar(im, label='Polarized Intensity (Jy/beam)')
plt.title('Polarized Intensity (P)')
plt.savefig(os.path.join(output_folder, "Polarized_Intensity_RA_Dec.png"))
plt.close()

# Plot and save Polarization Angle with RA and Dec axes
plt.figure(figsize=(8, 6))
ax = plt.subplot(projection=wcs)
im = ax.imshow(pol_angle, origin='lower', cmap='twilight')
ax.set_xlabel('RA (J2000)')
ax.set_ylabel('Dec (J2000)')
plt.colorbar(im, label='Polarization Angle (deg)')
plt.title('Polarization Angle (degrees)')
plt.savefig(os.path.join(output_folder, "Polarization_Angle_RA_Dec.png"))
plt.close()

print("All images with RA and Dec axes have been saved to:", output_folder)
