
#! python3

import os
import datetime
import shutil

def update_logo():
    # Get the current day of the year
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    print(day_of_year)

    # Get the list of images in the pool
    pool_folder = "assets/logo/dynamic_icon_dc/dynamic_logo_switcher/dynamic_logo_pool"
    img_files = sorted(os.listdir(pool_folder))

    # Select the image corresponding to the current day of the year
    img_file = img_files[day_of_year % len(img_files)]  # Use modulo to avoid out of range errors

    # Construct the paths
    old_path = os.path.join(pool_folder, img_file)
    new_path = "assets/logo/dynamic_icon_dc/dynamic_logo_switcher/current_dynamic_logo/logo.png"

    # Copy the file
    shutil.copyfile(old_path, new_path)

if __name__ == "__main__":
    update_logo()