#! python3

"""
    This component parse the metadata.json of the GHComponent and convert it to RST format.
"""

import json

class MetadataParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_json()

    def load_json(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def get_name(self):
        return self.data.get("name", "")

    def get_nickname(self):
        return self.data.get("nickname", "")

    def get_category(self):
        return self.data.get("category", "")

    def get_subcategory(self):
        return self.data.get("subcategory", "")

    def get_description(self):
        return self.data.get("description", "")

    def get_exposure(self):
        return self.data.get("exposure", 0)

    def get_instance_guid(self):
        return self.data.get("instanceGuid", "")

    def get_ghpython_settings(self):
        return self.data.get("ghpython", {})

    def get_input_parameters(self):
        ghpython = self.get_ghpython_settings()
        return ghpython.get("inputParameters", [])

    def get_output_parameters(self):
        ghpython = self.get_ghpython_settings()
        return ghpython.get("outputParameters", [])

    def return_rst_content(self):
        content = []
        # Uncomment these lines if you want to include additional metadata
        # content.append(f"{'`' * 2}{self.get_name()}{'`' * 2}")
        # content.append(f"{'#' * 2} {self.get_nickname()}")
        # content.append(f"{'#' * 2} {self.get_category()}")
        # content.append(f"{'#' * 2} {self.get_subcategory()}")
        # content.append(f"{'#' * 2} {self.get_description()}")
        # content.append(f"{'#' * 2} {self.get_exposure()}")
        # content.append(f"{'#' * 2} {self.get_instance_guid()}")
        # content.append(f"{'#' * 2} GHPython Settings:")
        # for key, value in self.get_ghpython_settings().items():
        #     content.append(f"{'#' * 3} {key}: {value}")

        

        params = self.get_input_parameters()
        # if params:  # Ensure params is not empty
        #     content.append("\n")
        #     content.append(".. list-table:: inputs\n    :header-rows: 1\n")
        #     content.append("    * - parameter")
        #     content.append("      - description")
        #     content.append("    * - test")
        #     content.append("      - test1")
        #     # for param in params:
        #     #     content.append(f"    * - {param['name']}")
        #     #     content.append(f"      - {param['description']}")

        content.append("prooooooooooooooooova1")
        content.append("\n")
        content.append("\n")
        content.append(".. list-table:: inputs\n    :header-rows: 1\n")
        content.append("    * - Package")
        content.append("      - Version")
        content.append("    * - vc")
        content.append("      - 14.3=hcf57466_18")
        content.append("    * - vc14_runtime")
        content.append("      - 14.16.27012=hf0eaf9b_1")
        content.append("\n")
        content.append("prooooooooooooooooova2")

        # convert merge into one string


        return content


            # content.append(f"{'#' * 3} Name: {param.get('name', '')}")
            # content.append(f"{'#' * 3} Nickname: {param.get('nickname', '')}")
            # content.append(f"{'#' * 3} Description: {param.get('description', '')}")
            # content.append(f"{'#' * 3} Optional: {param.get('optional', False)}")
            # content.append(f"{'#' * 3} Allow Tree Access: {param.get('allowTreeAccess', False)}")
            # content.append(f"{'#' * 3} Show Type Hints: {param.get('showTypeHints', False)}")
            # content.append(f"{'#' * 3} Script Param Access: {param.get('scriptParamAccess', '')}")
            # content.append(f"{'#' * 3} Wire Display: {param.get('wireDisplay', '')}")
            # content.append(f"{'#' * 3} Source Count: {param.get('sourceCount', 0)}")
            # content.append(f"{'#' * 3} Type Hint ID: {param.get('typeHintID', '')}")
        # return content