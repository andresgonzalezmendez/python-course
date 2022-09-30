"""
Program: Odin Digital
Version: 1.0
Author: Andrés González Méndez
Date: 30 Sep 2022
Functions script
"""

from tkinter import filedialog
import cv2

def compareimages():
    """ Function to compare two images"""
    files_allowed = [("Image Files",
    [".bmp", ".dib", ".jpeg", ".jpg", ".jpe", ".jp2", ".png",
    ".pbm", ".pgm", ".ppm", ".sr", ".ras", ".tiff", ".tif"])]

    file_a = filedialog.askopenfilename(
        initialdir = "img",
        title = "Select image number 1",
        filetypes = files_allowed)
    file_b = filedialog.askopenfilename(
        initialdir = "img",
        title = "Select image number 2",
        filetypes = files_allowed)

    image_a = cv2.imread(file_a)
    image_b = cv2.imread(file_b)

    if (image_a.shape[0] != image_b.shape[0]) or (image_a.shape[1] != image_b.shape[1]):
        print("""ERROR:
        Both images must be the same size.""")
    else:
        difference = cv2.subtract(image_a, image_b)
        num_different_pixels = cv2.countNonZero(
            cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY))

        if num_different_pixels == 0:
            print ("""RESULT:
            Both images are exactly the same!""")

        else:
            percentage_different_pixels = 100 * num_different_pixels/(
                difference.shape[0]*difference.shape[1])
            print(f"""RESULT:
            There are differences between the two images!
            Percentage of different pixels: {percentage_different_pixels:.2f}%""")

            new_image_a = cv2.resize(
                image_a,
                (image_a.shape[1]//2, image_a.shape[0]//2)
                )
            new_image_b = cv2.resize(
                image_b,
                (image_b.shape[1]//2, image_b.shape[0]//2)
                )
            original_images = cv2.hconcat([new_image_a, new_image_b])

            cv2.imshow("Result", cv2.vconcat([original_images, difference]))

            cv2.waitKey(0)
            cv2.destroyAllWindows()
