#! python3

"""
    Rename all the files in a folder with each day of the year like 0101, 0102, 0103, etc.
"""

import os
import datetime

# Set the path to the folder containing the images
img_folder = R"F:\diffCheck\assets\logo\dynamic_icon_dc\dynamic_logo_switcher\dynamic_logo_pool"

# Get the list of images in the folder
img_files = sorted(os.listdir(img_folder))

# rename from 1 to 365
for i, img_file in enumerate(img_files):
    day_of_year = i + 1
    new_name = f"{day_of_year:03d}.png"
    new_path = os.path.join(img_folder, new_name)
    os.rename(os.path.join(img_folder, img_file), new_path)
    print(f"Renamed {img_file} to {new_name}")