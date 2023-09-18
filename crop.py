import cv2
import numpy as np
import os

# Load the image
image = cv2.imread('D:/Kuliah/Semester 5/Pengolahan Citra Digital/Pertemuan 4/flask-digital-image-processing/static/img/img_normal.jpg')

# Define the number of rows and columns (n x n)
n = 5

# Get the dimensions of the image
height, width, _ = image.shape

# Calculate the size of each tile
tile_height = height // n
tile_width = width // n

# Define the output directory
output_directory = 'D:/Kuliah/Semester 5/Pengolahan Citra Digital/Pertemuan 4/flask-digital-image-processing/static/img/tiles/'

# Check if the directory exists, and if not, create it
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Initialize a list to store the tiles
tiles = []

# Iterate through the image and crop it into tiles
for i in range(n):
    for j in range(n):
        # Calculate the coordinates for cropping
        y1 = i * tile_height
        y2 = (i + 1) * tile_height
        x1 = j * tile_width
        x2 = (j + 1) * tile_width

        # Crop the tile from the image
        tile = image[y1:y2, x1:x2]

        # Save the tile
        tile_filename = os.path.join(output_directory, f'tile_{i * n + j + 1}.jpg')
        cv2.imwrite(tile_filename, tile)

        # Show the tile (optional)
        cv2.imshow(f'Tile {i * n + j + 1}', tile)

# Wait for a key press and close OpenCV windows
cv2.waitKey(0)
cv2.destroyAllWindows()
