"""
compareimages.py
Author: Andrés González Méndez
Date: 30 Sep 2022
v1.0
"""

# Import required modules

import cv2
import numpy as np

# Read the input images

image_a = cv2.imread("img/image_a.png")
image_b = cv2.imread("img/image_b.png")

(height_a, width_a, channels_a) = image_a.shape
(height_b, width_b, channels_b) = image_b.shape

# Check that images are valid

if (height_a != height_b) or (width_a != width_b) or (channels_a != channels_b):
    print("Both images must be the same size ")

# Calculate the difference image and percentage of different pixels

difference = cv2.subtract(image_a, image_b)
num_different_pixels  = cv2.countNonZero(cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY))
percentage_different_pixels = 100*num_different_pixels/(difference.shape[0]*difference.shape[1])
print("Percentage of different pixels: {:.2f}%".format(percentage_different_pixels))

# Print out the result

new_height_a = height_a//2
new_width_a = width_a//2
new_dim_a = (new_width_a, new_height_a)
new_height_b = height_b//2
new_width_b = width_b//2
new_dim_b = (new_width_b, new_height_b)
new_image_a = cv2.resize(image_a, new_dim_a)
new_image_b = cv2.resize(image_b, new_dim_b)
original_images = cv2.hconcat([new_image_a, new_image_b])

cv2.imshow("Result", cv2.vconcat([original_images, difference]))

cv2.waitKey(0)
cv2.destroyAllWindows()
