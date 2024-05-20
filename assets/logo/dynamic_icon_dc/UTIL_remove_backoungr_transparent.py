#! python3

"""
    This is a script that reads all the images in a folder and remove the white background to 
    create a transparent .png images (do not use cv2)
"""

import os
import numpy as np

from PIL import Image
from PIL import Image, ImageFilter

def remove_background(img_path, save_path):
    img = Image.open(img_path)
    img = img.convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)


    original_size = img.size
    # Resize the image to a smaller size
    pixel_val = 30
    img = img.resize((pixel_val, pixel_val), Image.BOX)


    # Resize the image back to its original size
    img = img.resize(original_size, Image.BOX)



    img.save(save_path, "PNG")

# Set the path to the folder containing the images
img_folder = R"C:/Users/andre/Downloads/dynamiclogo_blue"

# Set the path to the folder where the transparent images will be saved
save_folder = R"C:/Users/andre/Downloads/transp"

# Create the folder if it does not exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Get the list of images in the folder
img_files = os.listdir(img_folder)

# Remove the white background from each image and save the transparent image
for img_file in img_files:
    img_path = os.path.join(img_folder, img_file)
    save_path = os.path.join(save_folder, img_file)
    remove_background(img_path, save_path)

# Print a message to indicate that the process is complete
print("White background removed from images.")
