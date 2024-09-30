#! python3


from ghpythonlib.componentbase import executingcomponent as component

from diffCheck.df_error_estimation import DFVizResults
import csv
import os


class DFCsvExporter(component):
    def _get_id(self, idx, i_result):
        """ Get the ID of the element """
        counter = 0

        if self.prefix == "beam":
            return idx
        elif self.prefix == "joint":
            for idx_b, beam in enumerate(i_result.assembly.beams):
                for idx_j, joint in enumerate(beam.joints):
                    if counter == idx:
                        return f"{idx_b}--{idx_b}--{idx_j}"
                    counter += 1
        elif self.prefix == "joint_face":
            for idx_b, beam in enumerate(i_result.assembly.beams):
                for idx_j, joint in enumerate(beam.joints):
                    for idx_f, face in enumerate(joint.faces):
                        if counter == idx:
                            return f"{idx_b}--{idx_j}--{idx_f}"
                        counter += 1

    def _write_csv(self, file_path, rows):
        """ Write the CSV file """
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f"{self.prefix} id", "distances", "min_deviation", "max_deviation", "std_deviation", "rmse", "mean"])
            writer.writerows(rows)

    def _prepare_row(self, idx, i_result):
        """ Prepare a row for the CSV file """
        distances = [round(value, 4) for value in i_result.distances[idx]]
        min_dev = round(i_result.distances_min_deviation[idx], 4)
        max_dev = round(i_result.distances_max_deviation[idx], 4)
        std_dev = round(i_result.distances_sd_deviation[idx], 4)
        rmse = round(i_result.distances_rmse[idx], 4)
        mean = round(i_result.distances_mean[idx], 4)
        distances_str = ";".join(map(str, distances))
        return [self._get_id(idx, i_result), distances_str, min_dev, max_dev, std_dev, rmse, mean]

    def RunScript(self,
                  i_dump: bool,
                  i_export_dir: str,
                  i_file_name: str,
                  i_export_seperate_files: bool,
                  i_result: DFVizResults):

        if i_dump:
            os.makedirs(i_export_dir, exist_ok=True)

            if len(i_result.assembly.beams) == len(i_result.source):
                self.prefix = "beam"
            elif len(i_result.assembly.all_joints) == len(i_result.source):
                self.prefix = "joint"
            elif len(i_result.assembly.all_joint_faces) == len(i_result.source):
                self.prefix = "joint_face"

            if i_export_seperate_files:
                for idx in range(len(i_result.source)):
                    element_id = self._get_id( idx, i_result)
                    file_path = os.path.join(i_export_dir, f"{i_file_name}_{self.prefix}_{element_id}.csv")
                    self._write_csv(file_path, [self._prepare_row(idx, i_result)])
            else:
                file_path = os.path.join(i_export_dir, f"{i_file_name}.csv")
                rows = [self._prepare_row(idx, i_result) for idx in range(len(i_result.source))]
                self._write_csv(file_path, rows)
