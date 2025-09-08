from astropy.io import fits

# Path to your Stokes I FITS file
file_path = r"C:\Users\anagha rajesh\Downloads\3C75_final_large.pbcor_cropped.fits"

# Open the FITS file and read the header
with fits.open(file_path) as hdul:
    header = hdul[0].header

# Print the full header
for key, value in header.items():
    print(f"{key}: {value}")
