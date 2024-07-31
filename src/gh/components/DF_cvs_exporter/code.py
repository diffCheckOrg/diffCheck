#! python3

import System
import typing

import Rhino
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML
from diffCheck.df_error_estimation import DFVizResults
import csv
import os


class CsvExporter(component):
    def RunScript(self,
        i_dump: bool,
        i_export_dir: str,
        i_file_name: str,
        i_export_seperate_files: bool,
        i_result: DFVizResults):
        """
            The csv-exporter component exports a list of values to a .csv file

            :param i_dump: A flag indicating whether to perform the export.
            :param i_export_dir: The directory where the CSV file will be saved.
            :param i_file_name: The name of the file
            :param i_export_seperate_files: whether to export a different file for each part
            :param i_values: A list of values to be exported.

            :return o_success: A string notifying the user for the successful export
        """
        if i_dump:
            # Ensure the export directory exists
            os.makedirs(i_export_dir, exist_ok=True)

            if i_export_seperate_files:
                # Export each list of values to a separate file
                for idx, list_of_values in enumerate(i_result.distances):
                    file_name = f"{i_file_name}_{idx + 1}.csv"
                    file_path = os.path.join(i_export_dir, file_name)
                    with open(file_path, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([list_of_values])
            else:
                # Export all values to a single file
                file_path = os.path.join(i_export_dir, f"{i_file_name}.csv")
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    for list_of_values in i_result.distances:
                        writer.writerow([list_of_values])

            o_success = "Successfully exported the values"

            return o_success


# if __name__ == "__main__":
#     com = CsvExporter()
#     o_cvs = com.RunScript(
#         i_dump,
#         i_export_dir,
#         i_file_name,
#         i_export_seperate_files,
#         i_results
#     )