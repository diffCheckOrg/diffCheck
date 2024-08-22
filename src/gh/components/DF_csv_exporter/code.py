#! python3


from ghpythonlib.componentbase import executingcomponent as component

from diffCheck.df_error_estimation import DFVizResults
import csv
import os


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
