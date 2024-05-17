#! python3


#values min, max of the domain of the parameters to vary
VAL_DICT = {
    "seem_start" : (0.0, 1.0),
    "scale_f" : (1.0, 1.3),
    "thickness" : (0.4, 1.8),
    "number_ctrl_pts" : (7, 20),
    "dist_from_centers" : (0.0, 4.0),
    "tightness" : (1.1, 2.1)
}

if __name__ == "__main__":
    print("Shuffler is running...")

    o_seem_start = 0.0
    o_scale_f = 1.0
    o_thickness = 0.4
    o_number_ctrl_pts = 7
    o_dist_from_centers = 0.0
    o_tightness = 1.1

    o_combinations = []

    import random
    
    # create a unique and random combinations for each day of the year and output a list of list of values (stay within the domain)
    seem_start_values = []
    for i in range(365):
        o_seem_start = random.uniform(VAL_DICT["seem_start"][0], VAL_DICT["seem_start"][1])
        o_scale_f = random.uniform(VAL_DICT["scale_f"][0], VAL_DICT["scale_f"][1])
        o_thickness = random.uniform(VAL_DICT["thickness"][0], VAL_DICT["thickness"][1])
        o_number_ctrl_pts = random.randint(VAL_DICT["number_ctrl_pts"][0], VAL_DICT["number_ctrl_pts"][1])
        o_dist_from_centers = random.uniform(VAL_DICT["dist_from_centers"][0], VAL_DICT["dist_from_centers"][1])
        o_tightness = random.uniform(VAL_DICT["tightness"][0], VAL_DICT["tightness"][1])

        o_combinations.append([o_seem_start, o_scale_f, o_thickness, o_number_ctrl_pts, o_dist_from_centers, o_tightness])

    

    print("Shuffler is done.")


