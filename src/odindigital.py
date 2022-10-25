"""
Program: Odin Digital
Version: 1.3-beta
Author: Andrés González Méndez
Date: 25 Oct 2022
Main script
"""

# IMPORTS

from tkinter import messagebox, filedialog, IntVar
import tkinter as tk
from PIL import Image, ImageTk
import cv2

# CONSTANTS

PROGRAM_NAME = "Odin Digital"
VERSION_NUMBER = "1.3-beta"
FONT = "Verdana"
WINDOW_BACKGROUND_COLOR = "light gray"
WELCOME_TEXT = f"""Welcome to {PROGRAM_NAME} v{VERSION_NUMBER}, a digital image processing tool
developed by your QA friend Andrés González.
\nPlease select an option:"""
FILES_ALLOWED = [("Image Files",
    [".bmp", ".dib", ".jpeg", ".jpg", ".jpe", ".jp2", ".png",
    ".pbm", ".pgm", ".ppm", ".sr", ".ras", ".tiff", ".tif"])]
COLOR2GRAY_LABEL = "Select a color image to convert it to grayscale"
COMPAREIMAGES_LABEL = "Select two images to see how different they are"
ROTATEIMAGE_LABEL = "Rotate an image in any direction"
EDGES_LABEL = "Detect the edges of an image"
EXIT_APP = "See you soon!"
PADY_INTROTEXT = 20
PADY_FRAMES = 10
PADY_LABELSBUTTONS = 3

# FUNCTIONS

def openimagedialog(initial_dir, dialog_title):
    """Function to read an image from the computer"""

    filename = filedialog.askopenfilename(
        initialdir = initial_dir,
        title = dialog_title,
        filetypes = FILES_ALLOWED)

    return cv2.imread(filename)

def imagecv2totk(image_cv2):
    """Function to convert OpenCV images to Pillow"""

    image_rgb = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB)

    return ImageTk.PhotoImage(Image.fromarray(image_rgb))

def displayimage(image, label):
    """Function to display an image in new window"""

    window = tk.Toplevel(bg = WINDOW_BACKGROUND_COLOR)
    window.title(f"Image - {PROGRAM_NAME} v{VERSION_NUMBER}")
    window.resizable(False, False)

    text_label = tk.Label(
        window,
        text = label,
        font = (FONT, 30),
        bg = WINDOW_BACKGROUND_COLOR
        )
    text_label.pack(pady = PADY_LABELSBUTTONS)

    image_tk = imagecv2totk(image)

    image_label = tk.Label(
        window,
        bg = WINDOW_BACKGROUND_COLOR,
        image = image_tk
    )
    image_label.image = image_tk
    image_label.pack()

    window.protocol("WM_DELETE_WINDOW", lambda: saveimage(
        window,
        image,
        "img",
        "Select path to save image:")
    )

def exitapp():
    """Show confirmation dialog"""
    if messagebox.askyesno(
        message = "Are you sure you want to exit the app?",
        default = messagebox.NO):
        root.destroy()

def saveimage(window, image, initial_dir, dialog_title):
    """Dialog for saving images"""

    user_choice = messagebox.askyesnocancel(
        message = "Do you want to save the image before closing?"
        )

    if user_choice:
        filename = filedialog.asksaveasfilename(
            initialdir = initial_dir,
            title = dialog_title,
            filetypes = FILES_ALLOWED
        )
        cv2.imwrite(filename, image)
        window.destroy()
    elif user_choice is None:
        window.protocol(
            "WM_DELETE_WINDOW",
            lambda: saveimage(window, image, "img", "Select path to save image:")
            )
    else:
        window.destroy()

def getimagesize(image):
    """Get image size"""

    height = image.shape[0]
    width = image.shape[1]
    channels = image.shape[2]
    return (height, width, channels)

def compareimagesizes(image1, image2):
    """Compare image sizes"""

    if getimagesize(image1) == getimagesize(image2):
        return True

    return False

def compareimages():
    """ Function to compare two images"""

    image_a = openimagedialog("img", "Select image number 1")
    image_b = openimagedialog("img", "Select image number 2")

    if not compareimagesizes(image_a, image_b):
        messagebox.showwarning(
            title = "Warning",
            message = "Both images must be the same size"
            )
        return False

    difference = cv2.absdiff(image_a, image_b)

    num_different_pixels = cv2.countNonZero(
        cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY))

    if num_different_pixels == 0:
        messagebox.showinfo(
            title = "Result",
            message = "Both images are the same!"
            )
        return False

    percentage_different_pixels = 100 * num_different_pixels/(
        getimagesize(difference)[0]*getimagesize(difference)[1])

    # TO DO:
    # show the differences in white, instead of the difference color itself

    displayimage(image_a, "Image n.1")
    displayimage(image_b, "Image n.2")
    displayimage(difference, "Difference")

    messagebox.showinfo(
        title = "Result",
        message = f"""There are differences between the two images!
        Difference: {percentage_different_pixels:.2f}%"""
        )
    return True

def isgrayscale(image):
    """Detects if an image is grayscale or not"""

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    for i in range(getimagesize(rgb_image)[0]):
        for j in range(getimagesize(rgb_image)[1]):
            (r_value, g_value, b_value) = rgb_image[i, j]
            if not r_value == g_value == b_value:
                return False

    return True

def color2gray():
    """Function to turn an image from color to grayscale"""

    color_image = openimagedialog("img", "Select image")

    if isgrayscale(color_image):
        messagebox.showwarning(
            title = "Warning",
            message = "The image is grayscale already"
            )
        color2gray()
        return False

    # Color image
    displayimage(color_image, "Color image")

    # Gray image
    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    displayimage(gray_image, "Gray image")

    return True

def rotate_image(image, angle):
    """Rotates an image (angle in degrees) and expands image to avoid cropping"""

    # image shape has 3 dimensions
    height, width = image.shape[:2]
    # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape
    image_center = (width/2, height/2)

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0,0])
    abs_sin = abs(rotation_mat[0,1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo)
    # and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    rotated_mat = cv2.warpAffine(image, rotation_mat, (bound_w, bound_h))
    return rotated_mat

def digitvalidation(char):
    """Function to check that only numbers are entered in the Entry box"""
    if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        return True

    return False

def rotateimage():
    """Function to rotate an image"""

    original_image = openimagedialog("img", "Select image")
    displayimage(original_image, "Original image")

    dialog = tk.Toplevel(bg = WINDOW_BACKGROUND_COLOR)
    dialog.title(f"Image rotation - {PROGRAM_NAME} v{VERSION_NUMBER}")
    dialog.geometry("400x300")
    dialog.resizable(False, False)

    direction_frame = tk.Frame(
        dialog,
        bg = WINDOW_BACKGROUND_COLOR
    )
    direction_frame.pack(pady = PADY_FRAMES)

    direction_text_label = tk.Label(
        direction_frame,
        text = """In which direction do you want to rotate the image?""",
        font = (FONT, 15),
        bg = WINDOW_BACKGROUND_COLOR
        )
    direction_text_label.pack(pady = PADY_LABELSBUTTONS)

    direction_checkboxes_frame = tk.Frame(
        direction_frame,
        bg = WINDOW_BACKGROUND_COLOR
    )
    direction_checkboxes_frame.pack(pady = PADY_LABELSBUTTONS)

    rot_direction = IntVar()
    rot_direction.set(0)

    clockwise_checkbox = tk.Radiobutton(
        direction_checkboxes_frame,
        bg = WINDOW_BACKGROUND_COLOR,
        text = "Clockwise",
        variable = rot_direction,
        value = 1
    )
    clockwise_checkbox.pack(pady = PADY_LABELSBUTTONS, padx = 10, side = tk.LEFT)

    counterclockwise_checkbox = tk.Radiobutton(
        direction_checkboxes_frame,
        bg = WINDOW_BACKGROUND_COLOR,
        text = "Counterclockwise",
        variable = rot_direction,
        value = 2
    )
    counterclockwise_checkbox.pack(pady = PADY_LABELSBUTTONS, padx = 10, side = tk.RIGHT)

    angle_frame = tk.Frame(
        dialog,
        bg = WINDOW_BACKGROUND_COLOR
    )
    angle_frame.pack(pady = PADY_FRAMES)

    angle_text_label = tk.Label(
        angle_frame,
        text = """How many degrees?""",
        font = (FONT, 15),
        bg = WINDOW_BACKGROUND_COLOR
        )
    angle_text_label.pack(pady = PADY_LABELSBUTTONS)

    angle_entrybox = tk.Entry(
        angle_frame,
        validate = 'key',
        validatecommand = (angle_frame.register(digitvalidation), '%S')
    )
    angle_entrybox.pack(pady = PADY_LABELSBUTTONS)

    def rotate():
        if len(angle_entrybox.get()) == 0:
            messagebox.showwarning(
                title = "Warning",
                message = "Please fill in all required fields"
            )
            return False

        if rot_direction.get() == 1:
            angle = -int(angle_entrybox.get())
        elif rot_direction.get() == 2:
            angle = int(angle_entrybox.get())
        else:
            messagebox.showwarning(
                title = "Warning",
                message = "Please fill in all required fields"
            )
            return False

        rot_image = rotate_image(original_image, angle)
        displayimage(rot_image, "Rotated image")
        return True

    buttons_frame = tk.Frame(
        dialog,
        bg = WINDOW_BACKGROUND_COLOR
    )
    buttons_frame.pack(pady = PADY_FRAMES)

    go_button = tk.Button(
        buttons_frame,
        text = "Rotate!",
        bg = WINDOW_BACKGROUND_COLOR,
        command = rotate
    )
    go_button.pack(pady = PADY_LABELSBUTTONS, padx = 10, side = tk.RIGHT)

    close_button = tk.Button(
        buttons_frame,
        text = "Close",
        bg = WINDOW_BACKGROUND_COLOR,
        command = dialog.destroy
    )
    close_button.pack(pady = PADY_LABELSBUTTONS, padx = 10, side = tk.LEFT)

def edgedetection():
    """Funciton to detec edges"""

    image = openimagedialog("img", "Select image")
    edges = cv2.Canny(image,100,200)

    displayimage(image, "Original image")
    displayimage(edges, "Edges of the image")

# MAIN

root = tk.Tk()
root.title(f"{PROGRAM_NAME} v{VERSION_NUMBER}")
root.geometry("800x600")
root.resizable(False, False)
root.configure(bg = WINDOW_BACKGROUND_COLOR)

## Welcome text

intro_text = tk.Label(
    root,
    text = WELCOME_TEXT,
    font = (FONT, 20),
    bg = WINDOW_BACKGROUND_COLOR
)
intro_text.pack(pady = PADY_INTROTEXT)

## Menu bar

menu_bar = tk.Menu()

file_menu = tk.Menu(
    menu_bar,
    tearoff = False
)
file_menu.add_command(
    label = "Exit",
    command = exitapp
    )

menu_bar.add_cascade(
    menu = file_menu,
    label = "File"
)

tools_menu = tk.Menu(
    menu_bar,
    tearoff = False
)
tools_menu.add_command(
    label = "Color -> Gray",
    command = color2gray
    )
tools_menu.add_command(
    label = "Compare images",
    command = compareimages
    )
tools_menu.add_command(
    label = "Rotate image",
    command = rotateimage
    )
tools_menu.add_command(
    label = "Edge detection",
    command = edgedetection
    )

menu_bar.add_cascade(
    menu = tools_menu,
    label = "Tools"
)

root.configure(menu = menu_bar)

## Color2gray frame

color2gray_frame = tk.Frame(
    root,
    bg = WINDOW_BACKGROUND_COLOR
)
color2gray_frame.pack(pady = PADY_FRAMES)

color2gray_label = tk.Label(
    color2gray_frame,
    text = COLOR2GRAY_LABEL,
    font = (FONT, 15),
    bg = WINDOW_BACKGROUND_COLOR
)
color2gray_label.pack(pady = PADY_LABELSBUTTONS)

color2gray_button = tk.Button(
    color2gray_frame,
    text = "Color -> Gray",
    font = (FONT, 15),
    bg = WINDOW_BACKGROUND_COLOR,
    command = color2gray
    )
color2gray_button.pack(pady = PADY_LABELSBUTTONS)

## Compareimages frame

compareimages_frame = tk.Frame(
    root,
    bg = WINDOW_BACKGROUND_COLOR
)
compareimages_frame.pack(pady = PADY_FRAMES)

compareimages_label = tk.Label(
    compareimages_frame,
    text = COMPAREIMAGES_LABEL,
    font = (FONT, 15),
    bg = WINDOW_BACKGROUND_COLOR
)
compareimages_label.pack(pady = PADY_LABELSBUTTONS)

compareimages_button = tk.Button(
    compareimages_frame,
    text = "Compare images",
    font = (FONT, 15),
    bg = WINDOW_BACKGROUND_COLOR,
    command = compareimages
    )
compareimages_button.pack(pady = PADY_LABELSBUTTONS)

## Rotate frame

rotateimage_frame = tk.Frame(
    root,
    bg = WINDOW_BACKGROUND_COLOR
)
rotateimage_frame.pack(pady = PADY_FRAMES)

rotateimage_label = tk.Label(
    rotateimage_frame,
    text = ROTATEIMAGE_LABEL,
    font = (FONT, 15),
    bg = WINDOW_BACKGROUND_COLOR
)
rotateimage_label.pack(pady = PADY_LABELSBUTTONS)

rotateimage_button = tk.Button(
    rotateimage_frame,
    text = "Rotate image",
    font = (FONT, 15),
    bg = WINDOW_BACKGROUND_COLOR,
    command = rotateimage
    )
rotateimage_button.pack(pady = PADY_LABELSBUTTONS)

## Edges frame

edges_frame = tk.Frame(
    root,
    bg = WINDOW_BACKGROUND_COLOR
)
edges_frame.pack(pady = PADY_FRAMES)

edges_label = tk.Label(
    edges_frame,
    text = EDGES_LABEL,
    font = (FONT, 15),
    bg = WINDOW_BACKGROUND_COLOR
)
edges_label.pack(pady = PADY_LABELSBUTTONS)

edges_button = tk.Button(
    edges_frame,
    text = "Edge detection",
    font = (FONT, 15),
    bg = WINDOW_BACKGROUND_COLOR,
    command = edgedetection
    )
edges_button.pack(pady = PADY_LABELSBUTTONS)

## Exit frame

exit_frame = tk.Frame(
    root,
    bg = WINDOW_BACKGROUND_COLOR
)
exit_frame.pack(pady = PADY_FRAMES)

exit_label = tk.Label(
    exit_frame,
    text = EXIT_APP,
    font = (FONT, 15),
    bg = WINDOW_BACKGROUND_COLOR
)
exit_label.pack(pady = PADY_LABELSBUTTONS)

exit_button = tk.Button(
    exit_frame,
    text = "Exit",
    font = (FONT, 15),
    command = exitapp
    )
exit_button.pack(pady = PADY_LABELSBUTTONS)

##

root.protocol("WM_DELETE_WINDOW", exitapp)
root.mainloop()
