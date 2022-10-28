"""
Program: Odin Digital
Version: 1.3
Author: Andrés González Méndez
Date: 28 Oct 2022
Main script
"""

# IMPORTS

from tkinter import messagebox, filedialog, IntVar
import tkinter as tk
from PIL import Image, ImageTk
import cv2

# CONSTANTS

PROGRAM_NAME = "Odin Digital"
VERSION_NUMBER = "1.3"
FONT = "Verdana"
WINDOW_BACKGROUND_COLOR = "light gray"
WELCOME_TEXT = f"""Welcome to {PROGRAM_NAME} v{VERSION_NUMBER}, a digital image processing tool
developed by your QA friend Andrés González.
\nPlease select an option:"""
FILES_ALLOWED = [("Image Files",
    [".bmp", ".dib", ".jpeg", ".jpg", ".jpe", ".jp2", ".png",
    ".pbm", ".pgm", ".ppm", ".sr", ".ras", ".tiff", ".tif"])]
EXIT_APP_LABEL = "See you soon!"
PADY_FRAMES = 30
PADX_LABELS = 50
PADY_LABELS = 5
PADX_BUTTONS = 20
PADY_BUTTONS = 20

# FUNCTIONS

def color_to_gray():
    """Script that turns an image from color to grayscale

    Returns:
        bool: True if convertion is done, False otherwise
    """

    color_image = open_image_dialog("img", "Select image")

    if is_grayscale(color_image):
        messagebox.showwarning(
            title = "Warning",
            message = "The image is grayscale already"
            )
        color_to_gray()
        return False

    display_image(color_image, "Color image")

    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    display_image(gray_image, "Gray image")

    return True

def compare_two_images():
    """Script to compares two images

    Returns:
        bool: True if images can be compared, False otherwise
    """
    image_a = open_image_dialog("img", "Select image number 1")
    image_b = open_image_dialog("img", "Select image number 2")

    if not compare_size_of_images(image_a, image_b):
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
        get_image_size(difference)[0]*get_image_size(difference)[1])

    # TO DO:
    # show the differences in white, instead of the difference color itself

    display_image(image_a, "Image n.1")
    display_image(image_b, "Image n.2")
    display_image(difference, "Difference")

    messagebox.showinfo(
        title = "Result",
        message = f"""There are differences between the two images!
        Difference: {percentage_different_pixels:.2f}%"""
        )
    return True

def compare_size_of_images(image1, image2):
    """Compares the size of two images

    Args:
        image1 (numpy.ndarray): OpenCV-compatible image
        image2 (numpy.ndarray): OpenCV-compatible image

    Returns:
        bool: True if sizes are equal, False otherwise
    """

    if get_image_size(image1) == get_image_size(image2):
        return True

    return False

def digit_validation(char):
    """Checks that only numbers are entered in the Entry box

    Args:
        char (str): entered character in the Entry box

    Returns:
        bool: True if the character is a digit, False otherwise
    """

    if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        return True

    return False

def display_image(image, label):
    """Displays an image in a new window

    Args:
        image (numpy.ndarray): OpenCV-compatible image
        label (str): Text label shown above the image
    """

    window = tk.Toplevel(bg = WINDOW_BACKGROUND_COLOR)
    window.title(f"Image - {PROGRAM_NAME} v{VERSION_NUMBER}")
    window.resizable(False, False)

    text_label = tk.Label(
        window,
        text = label,
        font = (FONT, 30),
        bg = WINDOW_BACKGROUND_COLOR
        )
    text_label.pack(pady = PADY_LABELS)

    image_tk = image_cv2_to_tk(image)

    image_label = tk.Label(
        window,
        bg = WINDOW_BACKGROUND_COLOR,
        image = image_tk
    )
    image_label.image = image_tk
    image_label.pack()

    window.protocol("WM_DELETE_WINDOW", lambda: save_image(
        window,
        image,
        "img",
        "Select path to save image:")
    )

def edge_detection():
    """Script that detects edges in an image"""

    image = open_image_dialog("img", "Select image")
    edges = cv2.Canny(image,100,200)

    display_image(image, "Original image")
    display_image(edges, "Edges of the image")

def exit_app():
    """Manages exit confirmation dialog"""

    if messagebox.askyesno(
        message = "Are you sure you want to exit the app?",
        default = messagebox.NO):
        root.destroy()

def get_image_size(image):
    """Gets the size of an image

    Args:
        image (numpy.ndarray): OpenCV-compatible image

    Returns:
        tuple (int, int, int): (height, width, channels) of the image
    """

    height = image.shape[0]
    width = image.shape[1]
    channels = image.shape[2]
    return (height, width, channels)

def image_cv2_to_tk(image_cv2):
    """Transforms a OpenCV-compatible image to a Tkinter-compatible image

    Args:
        image_cv2 (numpy.ndarray): OpenCV-compatible image

    Returns:
        PIL.ImageTk.PhotoImage: Tkinter-compatible image
    """

    image_rgb = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB)

    return ImageTk.PhotoImage(Image.fromarray(image_rgb))

def is_grayscale(image):
    """Detects if an image is grayscale or not

    Args:
        image (numpy.ndarray): OpenCV-compatible image

    Returns:
        bool: True if the image is grayscale, False otherwise
    """

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    for i in range(get_image_size(rgb_image)[0]):
        for j in range(get_image_size(rgb_image)[1]):
            (r_value, g_value, b_value) = rgb_image[i, j]
            if not r_value == g_value == b_value:
                return False

    return True

def match_template():
    """Script that finds if an image is contained within another image"""

    image = open_image_dialog("img", "Select the image")
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    display_image(image, "Original image")

    template = open_image_dialog("img", "Select the template")
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    display_image(template, "Template image")

    res = cv2.matchTemplate(image_gray, template_gray, cv2.TM_SQDIFF)
    _, _, min_loc, _ = cv2.minMaxLoc(res)

    x_1, y_1 = min_loc
    x_2, y_2 = min_loc[0] + template.shape[1], min_loc[1] + template.shape[0]

    cv2.rectangle(image, (x_1, y_1), (x_2, y_2), (0, 255, 0), 3)

    display_image(image, "Detection")

def open_image_dialog(initial_dir, dialog_title):
    """Asks the user to select an image and reads it

    Args:
        initial_dir (str): path of the initial directory
        dialog_title (str): title of the dialog

    Returns:
        numpy.ndarray: OpenCV-compatible image
    """

    filename = filedialog.askopenfilename(
        initialdir = initial_dir,
        title = dialog_title,
        filetypes = FILES_ALLOWED)

    return cv2.imread(filename)

def resize_image():
    """Script that resizes an image"""

    original_image = open_image_dialog("img", "Select image")
    display_image(original_image, "Original image")

    dialog = tk.Toplevel(bg = WINDOW_BACKGROUND_COLOR)
    dialog.title(f"Image resizing - {PROGRAM_NAME} v{VERSION_NUMBER}")
    dialog.resizable(False, False)

    blocks = []

    blocks.append(tk.Frame(
            dialog,
            bg = WINDOW_BACKGROUND_COLOR
        )
    )
    blocks[0].pack()

    frames = []

    frames.append(
        tk.Frame(
            blocks[0],
            bg = WINDOW_BACKGROUND_COLOR
        )
    )
    frames[0].grid(pady = PADY_BUTTONS, padx = PADX_BUTTONS, row = 0, column = 0)

    frames.append(
        tk.Frame(
            blocks[0],
            bg = WINDOW_BACKGROUND_COLOR
        )
    )
    frames[1].grid(pady = PADY_BUTTONS, padx = PADX_BUTTONS, row = 0, column = 1)

    label_original_size = tk.Label(
        frames[1],
        text = "Original image",
        font = (FONT, 15),
        bg = WINDOW_BACKGROUND_COLOR
    )
    label_original_size.pack()

    frames.append(
        tk.Frame(
            blocks[0],
            bg = WINDOW_BACKGROUND_COLOR
        )
    )
    frames[2].grid(pady = PADY_BUTTONS, padx = PADX_BUTTONS, row = 0, column = 2)

    label_new_size = tk.Label(
        frames[2],
        text = "New image",
        font = (FONT, 15),
        bg = WINDOW_BACKGROUND_COLOR
    )
    label_new_size.pack()

    frames.append(
        tk.Frame(
            blocks[0],
            bg = WINDOW_BACKGROUND_COLOR
        )
    )
    frames[3].grid(pady = PADY_BUTTONS, padx = PADX_BUTTONS, row = 1, column = 0)

    label_width = tk.Label(
        frames[3],
        text = "Width",
        font = (FONT, 15),
        bg = WINDOW_BACKGROUND_COLOR
    )
    label_width.pack()

    frames.append(
            tk.Frame(
            blocks[0],
            bg = WINDOW_BACKGROUND_COLOR
        )
    )
    frames[4].grid(pady = PADY_BUTTONS, padx = PADX_BUTTONS, row = 1, column = 1)

    original_width = tk.Label(
        frames[4],
        text = get_image_size(original_image)[1],
        font = (FONT, 15),
        bg = WINDOW_BACKGROUND_COLOR
    )
    original_width.pack()

    frames.append(
        tk.Frame(
            blocks[0],
            bg = WINDOW_BACKGROUND_COLOR
        )
    )
    frames[5].grid(pady = PADY_BUTTONS, padx = PADX_BUTTONS, row = 1, column = 2)

    new_width = tk.Entry(
        frames[5],
        validate = 'key',
        validatecommand = (frames[5].register(digit_validation), '%S')
    )
    new_width.pack()

    frames.append(
        tk.Frame(
            blocks[0],
            bg = WINDOW_BACKGROUND_COLOR
        )
    )
    frames[6].grid(pady = PADY_BUTTONS, padx = PADX_BUTTONS, row = 2, column = 0)

    label_width = tk.Label(
        frames[6],
        text = "Height",
        font = (FONT, 15),
        bg = WINDOW_BACKGROUND_COLOR
    )
    label_width.pack()

    frames.append(
        tk.Frame(
            blocks[0],
            bg = WINDOW_BACKGROUND_COLOR
        )
    )
    frames[7].grid(pady = PADY_BUTTONS, padx = PADX_BUTTONS, row = 2, column = 1)

    original_heigth = tk.Label(
        frames[7],
        text = get_image_size(original_image)[0],
        font = (FONT, 15),
        bg = WINDOW_BACKGROUND_COLOR
    )
    original_heigth.pack()

    frames.append(
        tk.Frame(
            blocks[0],
            bg = WINDOW_BACKGROUND_COLOR
        )
    )
    frames[8].grid(pady = PADY_BUTTONS, padx = PADX_BUTTONS, row = 2, column = 2)

    new_height = tk.Entry(
        frames[8],
        validate = 'key',
        validatecommand = (frames[8].register(digit_validation), '%S')
    )
    new_height.pack()

    blocks.append(
        tk.Frame(
            dialog,
            bg = WINDOW_BACKGROUND_COLOR
        )
    )
    blocks[1].pack()

    def resize():
        if (len(new_width.get()) == 0) or (len(new_height.get()) == 0):
            messagebox.showwarning(
                title = "Warning",
                message = "Please fill in all required fields"
            )
            return False

        resized_image = cv2.resize(original_image, (int(new_width.get()), int(new_height.get())))
        display_image(resized_image, "Resized image")
        return True

    buttons = []

    buttons.append(
        tk.Button(
            blocks[1],
            text = "Resize!",
            bg = WINDOW_BACKGROUND_COLOR,
            command = resize
        )
    )
    buttons[0].pack(pady = PADY_BUTTONS, padx = PADX_BUTTONS, side = tk.RIGHT)

    buttons.append(
        tk.Button(
            blocks[1],
            text = "Close",
            bg = WINDOW_BACKGROUND_COLOR,
            command = dialog.destroy
        )
    )
    buttons[1].pack(pady = PADY_BUTTONS, padx = PADX_BUTTONS, side = tk.LEFT)

def rotate_without_cropping(image, angle):
    """Rotates an image without cropping

    Source:
        https://stackoverflow.com/questions/43892506/opencv-python-rotate-image-without-cropping-sides

    Args:
        image (numpy.ndarray): OpenCV-compatible image
        angle (int): rotation angle in degrees

    Returns:
        numpy.ndarray: rotated OpenCV-compatible image
    """

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

def rotate_image():
    """Script that rotates an image"""

    original_image = open_image_dialog("img", "Select image")
    display_image(original_image, "Original image")

    dialog = tk.Toplevel(bg = WINDOW_BACKGROUND_COLOR)
    dialog.title(f"Image rotation - {PROGRAM_NAME} v{VERSION_NUMBER}")
    dialog.resizable(False, False)

    direction_frame = tk.Frame(
        dialog,
        bg = WINDOW_BACKGROUND_COLOR
    )
    direction_frame.pack()

    direction_text_label = tk.Label(
        direction_frame,
        text = """In which direction do you want to rotate the image?""",
        font = (FONT, 15),
        bg = WINDOW_BACKGROUND_COLOR
        )
    direction_text_label.pack(pady = PADY_LABELS, padx = PADX_LABELS)

    direction_checkboxes_frame = tk.Frame(
        direction_frame,
        bg = WINDOW_BACKGROUND_COLOR
    )
    direction_checkboxes_frame.pack(pady = PADY_LABELS)

    rot_direction = IntVar()
    rot_direction.set(0)

    clockwise_checkbox = tk.Radiobutton(
        direction_checkboxes_frame,
        bg = WINDOW_BACKGROUND_COLOR,
        text = "Clockwise",
        variable = rot_direction,
        value = 1
    )
    clockwise_checkbox.pack(pady = PADY_BUTTONS, padx = PADX_BUTTONS, side = tk.LEFT)

    counterclockwise_checkbox = tk.Radiobutton(
        direction_checkboxes_frame,
        bg = WINDOW_BACKGROUND_COLOR,
        text = "Counterclockwise",
        variable = rot_direction,
        value = 2
    )
    counterclockwise_checkbox.pack(pady = PADY_BUTTONS, padx = PADX_BUTTONS, side = tk.RIGHT)

    angle_frame = tk.Frame(
        dialog,
        bg = WINDOW_BACKGROUND_COLOR
    )
    angle_frame.pack()

    angle_text_label = tk.Label(
        angle_frame,
        text = """How many degrees?""",
        font = (FONT, 15),
        bg = WINDOW_BACKGROUND_COLOR
        )
    angle_text_label.pack(pady = PADY_LABELS)

    angle_entrybox = tk.Entry(
        angle_frame,
        validate = 'key',
        validatecommand = (angle_frame.register(digit_validation), '%S')
    )
    angle_entrybox.pack(pady = PADY_BUTTONS)

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

        rot_image = rotate_without_cropping(original_image, angle)
        display_image(rot_image, "Rotated image")
        return True

    buttons_frame = tk.Frame(
        dialog,
        bg = WINDOW_BACKGROUND_COLOR
    )
    buttons_frame.pack()

    go_button = tk.Button(
        buttons_frame,
        text = "Rotate!",
        bg = WINDOW_BACKGROUND_COLOR,
        command = rotate
    )
    go_button.pack(pady = PADY_BUTTONS, padx = PADX_BUTTONS, side = tk.RIGHT)

    close_button = tk.Button(
        buttons_frame,
        text = "Close",
        bg = WINDOW_BACKGROUND_COLOR,
        command = dialog.destroy
    )
    close_button.pack(pady = PADY_BUTTONS, padx = PADX_BUTTONS, side = tk.LEFT)

def save_image(window, image, initial_dir, dialog_title):
    """Shows a dialog to save an image

    Args:
        window (tkinter.Toplevel): tkinter window containing the image
        image (numpy.ndarray): OpenCV-compatible image
        initial_dir (str): path of the initial directory
        dialog_title (str): title of the dialog
    """

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
            lambda: save_image(window, image, "img", "Select path to save image:")
            )
    else:
        window.destroy()

# MAIN

root = tk.Tk()
root.title(f"{PROGRAM_NAME} v{VERSION_NUMBER}")
root.resizable(False, False)
root.configure(bg = WINDOW_BACKGROUND_COLOR)

## Welcome text

intro_text = tk.Label(
    root,
    text = WELCOME_TEXT,
    font = (FONT, 20),
    bg = WINDOW_BACKGROUND_COLOR
)
intro_text.pack(pady = PADY_FRAMES, padx = PADX_LABELS)

## Menu bar

menu_bar = tk.Menu()

file_menu = tk.Menu(
    menu_bar,
    tearoff = False
)

root.configure(menu = menu_bar)

### File

file_menu.add_command(
    label = "Exit",
    command = exit_app
    )

menu_bar.add_cascade(
    menu = file_menu,
    label = "File"
)

### Tools

tools_menu = tk.Menu(
    menu_bar,
    tearoff = False
)
tools_menu.add_command(
    label = "Color to grayscale",
    command = color_to_gray
    )
tools_menu.add_command(
    label = "Rotate",
    command = rotate_image
    )
tools_menu.add_command(
    label = "Resize",
    command = resize_image
    )
tools_menu.add_command(
    label = "Compare two images",
    command = compare_two_images
    )
tools_menu.add_command(
    label = "Detect edges",
    command = edge_detection
    )
tools_menu.add_command(
    label = "Match with template",
    command = match_template
    )

menu_bar.add_cascade(
    menu = tools_menu,
    label = "Tools"
)

## Buttons frame

main_buttons_frame = tk.Frame(
    root,
    bg = WINDOW_BACKGROUND_COLOR
)
main_buttons_frame.pack(pady = PADY_FRAMES)

### Color2gray button

color2gray_button = tk.Button(
    main_buttons_frame,
    text = "Color to grayscale",
    font = (FONT, 15),
    bg = WINDOW_BACKGROUND_COLOR,
    command = color_to_gray
    )
color2gray_button.grid(pady = PADY_BUTTONS, padx = PADX_BUTTONS, row = 0, column = 0)

### Rotate button

rotateimage_button = tk.Button(
    main_buttons_frame,
    text = "Rotate",
    font = (FONT, 15),
    bg = WINDOW_BACKGROUND_COLOR,
    command = rotate_image
    )
rotateimage_button.grid(pady = PADY_BUTTONS, padx = PADX_BUTTONS, row = 1, column = 0)

### Resize button

resizeimage_button = tk.Button(
    main_buttons_frame,
    text = "Resize",
    font = (FONT, 15),
    bg = WINDOW_BACKGROUND_COLOR,
    command = resize_image
    )
resizeimage_button.grid(pady = PADY_BUTTONS, padx = PADX_BUTTONS, row = 2, column = 0)

### Compareimages button

compareimages_button = tk.Button(
    main_buttons_frame,
    text = "Compare two images",
    font = (FONT, 15),
    bg = WINDOW_BACKGROUND_COLOR,
    command = compare_two_images
    )
compareimages_button.grid(pady = PADY_BUTTONS, padx = PADX_BUTTONS, row = 0, column = 1)

### Edges button

edges_button = tk.Button(
    main_buttons_frame,
    text = "Detect edges",
    font = (FONT, 15),
    bg = WINDOW_BACKGROUND_COLOR,
    command = edge_detection
    )
edges_button.grid(pady = PADY_BUTTONS, padx = PADX_BUTTONS, row = 1, column = 1)

### Match template button

matchtemplate_button = tk.Button(
    main_buttons_frame,
    text = "Match with template",
    font = (FONT, 15),
    bg = WINDOW_BACKGROUND_COLOR,
    command = match_template
    )
matchtemplate_button.grid(pady = PADY_BUTTONS, padx = PADX_BUTTONS, row = 2, column = 1)

## Exit frame

exit_frame = tk.Frame(
    root,
    bg = WINDOW_BACKGROUND_COLOR
)
exit_frame.pack(pady = PADY_FRAMES)

exit_label = tk.Label(
    exit_frame,
    text = EXIT_APP_LABEL,
    font = (FONT, 15),
    bg = WINDOW_BACKGROUND_COLOR
)
exit_label.pack(pady = PADY_LABELS)

exit_button = tk.Button(
    exit_frame,
    text = "Exit",
    font = (FONT, 15),
    command = exit_app
    )
exit_button.pack(pady = PADY_LABELS)

##

root.protocol("WM_DELETE_WINDOW", exit_app)
root.mainloop()
