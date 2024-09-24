#! python3


from ghpythonlib.componentbase import executingcomponent as component

from diffCheck.df_error_estimation import DFVizResults
import csv
import os


def get_id(prefix, idx, i_result):

    counter = 0

    if prefix == "beam":
        return idx
    elif prefix == "joint":
        for idx_b, beam in enumerate(i_result.assembly.beams):
            for idx_j, joint in enumerate(beam.joints):
                if counter == idx:
                    return f"{idx_b}--{idx_b}--{idx_j}"
                counter += 1
    elif prefix == "joint_face":
        for idx_b, beam in enumerate(i_result.assembly.beams):
            for idx_j, joint in enumerate(beam.joints):
                for idx_f, face in enumerate(joint.faces):
                    if counter == idx:
                        return f"{idx_b}--{idx_j}--{idx_f}"
                    counter += 1


class DFCsvExporter(component):
    def RunScript(self,
                  i_dump: bool,
                  i_export_dir: str,
                  i_file_name: str,
                  i_export_seperate_files: bool,
                  i_result: DFVizResults):

        if i_dump:
            # Ensure the export directory exists
            os.makedirs(i_export_dir, exist_ok=True)

            # Determine the prefix based on the type of data
            if len(i_result.assembly.beams) == len(i_result.source):
                prefix = "beam"
            elif len(i_result.assembly.all_joints) == len(i_result.source):
                prefix = "joint"
            elif len(i_result.assembly.all_joint_faces) == len(i_result.source):
                prefix = "joint_face"

            # Export each element in separate files if the flag is True
            if i_export_seperate_files:
                # Loop through the sources and export each element into its own file
                for idx, source in enumerate(i_result.source):
                    element_id = get_id(prefix, idx, i_result)
                    file_path = os.path.join(i_export_dir, f"{i_file_name}_{prefix}_{element_id}.csv")

                    with open(file_path, mode='w', newline='') as file:
                        writer = csv.writer(file)

                        # Write the header with the six columns
                        writer.writerow([f"{prefix} id", "distances", "min_deviation", "max_deviation", "std_deviation", "rmse"])

                        # Retrieve and round data
                        distances = [round(value, 4) for value in i_result.distances[idx]]  # Round distances to 4 decimals
                        min_dev = round(i_result.distances_min_deviation[idx], 4)
                        max_dev = round(i_result.distances_max_deviation[idx], 4)
                        std_dev = round(i_result.distances_sd_deviation[idx], 4)
                        rmse = round(i_result.distances_rmse[idx], 4)
                        distances_str = ";".join(map(str, distances))

                        # Create the row with the data and write it to the CSV
                        row = [get_id(prefix, idx, i_result), distances_str, min_dev, max_dev, std_dev, rmse]
                        writer.writerow(row)

            else:
                # Export all elements into a single file
                file_path = os.path.join(i_export_dir, f"{i_file_name}.csv")

                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)

                    # Write the header with the six columns
                    writer.writerow([f"{prefix} id", "distances", "min_deviation", "max_deviation", "std_deviation", "rmse"])

                    # Write the data for all elements
                    for idx, source in enumerate(i_result.source):
                        distances = [round(value, 4) for value in i_result.distances[idx]]  # Round distances to 4 decimals
                        min_dev = round(i_result.distances_min_deviation[idx], 4)
                        max_dev = round(i_result.distances_max_deviation[idx], 4)
                        std_dev = round(i_result.distances_sd_deviation[idx], 4)
                        rmse = round(i_result.distances_rmse[idx], 4)

                        distances_str = ";".join(map(str, distances))

                        # Create the row with the data and write it to the CSV
                        row = [get_id(prefix, idx, i_result), distances_str, min_dev, max_dev, std_dev, rmse]
                        writer.writerow(row)
