#! python3

import System
import csv
import os
import typing

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper as gh

from diffCheck.df_error_estimation import DFInvalidData, DFVizResults


def add_bool_toggle(self,
    nickname: str,
    indx: int,
    X_param_coord: float,
    Y_param_coord: float,
    X_offset: int=87
    ) -> None:
    """
        Adds a boolean toggle to the component input

        :param nickname: the nickname of the value list
        :param indx: the index of the input parameter
        :param X_param_coord: the x coordinate of the input parameter
        :param Y_param_coord: the y coordinate of the input parameter
        :param X_offset: the offset of the value list from the input parameter
    """
    param = ghenv.Component.Params.Input[indx]  # noqa: F821
    if param.SourceCount == 0:
        toggle = gh.Kernel.Special.GH_BooleanToggle()
        toggle.NickName = nickname
        toggle.Description = "Toggle the value to use with DFVizSettings"
        toggle.CreateAttributes()
        toggle.Attributes.Pivot = System.Drawing.PointF(
            X_param_coord - (toggle.Attributes.Bounds.Width) - X_offset,
            Y_param_coord - (toggle.Attributes.Bounds.Height / 2 + 0.1)
            )
        toggle.Attributes.ExpireLayout()
        gh.Instances.ActiveCanvas.Document.AddObject(toggle, False)
        ghenv.Component.Params.Input[indx].AddSource(toggle)  # noqa: F821


class DFCsvExporter(component):
    def __init__(self):
        super(DFCsvExporter, self).__init__()
        self.prefix = ""
        self.counter = 0

        ghenv.Component.ExpireSolution(True)  # noqa: F821
        ghenv.Component.Attributes.PerformLayout()  # noqa: F821
        params = getattr(ghenv.Component.Params, "Input")  # noqa: F821
        for j in range(len(params)):
            Y_cord = params[j].Attributes.InputGrip.Y + 1
            X_cord = params[j].Attributes.Pivot.X + 10
            input_indx = j
            if "i_export_seperate_files" == params[j].NickName:
                add_bool_toggle(
                    ghenv.Component,  # noqa: F821
                    "export_asfiles",
                    input_indx, X_cord, Y_cord)
            if "i_export_distances" == params[j].NickName:
                add_bool_toggle(
                    ghenv.Component,  # noqa: F821
                    "export_dist",
                    input_indx, X_cord, Y_cord)

    def _get_id(self,
        idx: int,
        i_result: DFVizResults
        ) -> str:
        """ Get the ID of the element """
        counter = 0

        if self.prefix == "beam":
            return idx
        elif self.prefix == "joint":
            for idx_b, beam in enumerate(i_result.assembly.beams):
                for idx_j, joint in enumerate(beam.joints):
                    if counter == idx:
                        return f"{idx_b}--{idx_j}--{0}"
                    counter += 1
        elif self.prefix == "joint_face":
            for idx_b, beam in enumerate(i_result.assembly.beams):
                for idx_j, joint in enumerate(beam.joints):
                    for idx_f, face in enumerate(joint.faces):
                        if counter == idx:
                            return f"{idx_b}--{idx_j}--{idx_f}"
                        counter += 1

    def _prepare_row(self,
            idx: int,
            i_result: DFVizResults
        ) -> typing.Dict:
        """
            Convert the results contained in the DFVizResults object to a dict to be written in the CSV file

            :param idx: Index of the element
            :param i_result: DFVizResults object containing all the values

            :return: Dict of values containng as keys the header and as items the values to be written in the CSV file
        """
        if i_result.sanity_check[idx].value != DFInvalidData.VALID.value:
            invalid_type = i_result.sanity_check[idx].name
            return [self._get_id(idx, i_result), invalid_type, invalid_type, invalid_type, invalid_type, invalid_type, invalid_type]

        distances = [round(value, 4) for value in i_result.distances[idx]]
        min_dev = round(i_result.distances_min_deviation[idx], 4)
        max_dev = round(i_result.distances_max_deviation[idx], 4)
        std_dev = round(i_result.distances_sd_deviation[idx], 4)
        rmse = round(i_result.distances_rmse[idx], 4)
        mean = round(i_result.distances_mean[idx], 4)

        row: typing.Dict = {
            f"{self.prefix} id": self._get_id(idx, i_result),
            "distances": distances,
            "min_deviation": min_dev,
            "max_deviation": max_dev,
            "std_deviation": std_dev,
            "rmse": rmse,
            "mean": mean
        }
        return row

    def _write_csv(self,
        csv_path: str,
        rows: typing.List[typing.Dict],
        is_writing_only_distances: bool = False
        ) -> None:
        """
            Write the CSV file

            :param csv_path: Path of the CSV file
            :param rows: Dict of values to be written in the CSV file
            :param is_writing_only_distances: Flag to check if to write ONLY distances or the whole analysis

            :return: None
        """
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
            if is_writing_only_distances:
                writer.writerow(list(rows[0].keys())[:2])  # header
                element_id = [row[f"{self.prefix} id"] for row in rows]
                dist_rows = [row["distances"] for row in rows]
                for idx, dist_row in enumerate(dist_rows):
                    for dist in dist_row:
                        writer.writerow([element_id[idx], dist])
            else:
                rows = [{k: v for k, v in row.items() if k != "distances"} for row in rows]  # no distances
                writer.writerow(list(rows[0].keys()))  # header
                writer.writerows([list(row.values()) for row in rows])

    def RunScript(self,
            i_dump: bool,
            i_export_dir: str,
            i_file_name: str,
            i_export_seperate_files: bool,
            i_export_distances: bool,
            i_result):

        csv_analysis_path: str = None
        csv_distances_path: str = None

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
                    element_id = self._get_id(idx, i_result)
                    csv_analysis_path = os.path.join(i_export_dir, f"{i_file_name}_{self.prefix}_{element_id}.csv")
                    rows = [self._prepare_row(idx, i_result)]
                    self._write_csv(csv_analysis_path, rows)
                    if i_export_distances:
                        csv_distances_path = os.path.join(i_export_dir, f"{i_file_name}_{self.prefix}_{element_id}_distances.csv")
                        self._write_csv(csv_distances_path, rows, is_writing_only_distances=True)
            else:
                csv_analysis_path = os.path.join(i_export_dir, f"{i_file_name}.csv")
                merged_rows = [self._prepare_row(idx, i_result) for idx in range(len(i_result.source))]
                self._write_csv(csv_analysis_path, merged_rows)
                if i_export_distances:
                    csv_distances_path = os.path.join(i_export_dir, f"{i_file_name}_distances.csv")
                    self._write_csv(csv_distances_path, merged_rows, is_writing_only_distances=True)
