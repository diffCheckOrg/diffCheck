#! python3

import System
import typing

import Rhino
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import csv
import os


class CsvExporter(component):
    def RunScript(self,
        i_dump: bool,
        i_export_dir: str,
        i_results):
        """
            The csv-exporter component exports a list of values to a .csv file

            :param i_dump: A flag indicating whether to perform the export.
            :param i_export_dir: The directory where the CSV file will be saved.
            :param i_values: A list of values to be exported.
        """
        if i_dump:
            # Ensure the export directory exists
            os.makedirs(i_export_dir, exist_ok=True)

            # Define the CSV file path
            file_path = os.path.join(i_export_dir, 'exported_values.csv')

            # Write the values to the CSV file
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                for list_of_values in i_results.distances:
                    writer.writerow([list_of_values])


if __name__ == "__main__":
    com = CsvExporter()
    o_cvs = com.RunScript(
        i_dump,
        i_export_dir,
        i_results
    )