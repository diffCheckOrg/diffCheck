#! python3

"""
    This pthon component is used to create a dynamic logo for the DC project.
"""

import os
import Rhino
import Rhino.Geometry as rg

import colorsys

# global counter
# counter = 0
if i_reset:
    o_index = -1
# # sticky value
if "o_index" in globals():
    counter = o_index

if __name__ == "__main__":
    # take a screenshot of the Rhino viewport
    view = Rhino.RhinoDoc.ActiveDoc.Views.ActiveView

    # output path
    output_path = R"F:\diffCheck\assets\logo\dynamic_icon_dc\temp"
    name_rh_view = "Top_export"

    # clear the output_path files
    for file in os.listdir(output_path):
        os.remove(os.path.join(output_path, file))

    # list all the views in the Rhino document
    rh_view = None
    view_list = Rhino.RhinoDoc.ActiveDoc.Views.GetViewList(True, False)
    for view in view_list:
        print(view.MainViewport.Name)
        if view.MainViewport.Name == name_rh_view:
            rh_view = view
    if rh_view is None:
        raise Exception("View not found")


    # create a series from 0 to 359
    # series = range(10)  # 360

    # create a loop for 

    # wait 1 second
    # Rhino.RhinoApp.Wait()

    # call a command to take a screenshot of the Rhino viewport
    output_file_name = os.path.join(output_path, "logo_" + str(o_index) + ".png")
    Rhino.RhinoApp.RunScript("_-ViewCaptureToFile " + output_file_name + " _Enter", False)
    

    #recompute the solution
    # ghenv.Component.ExpireSolution(True)



    counter = counter + 1
    o_index = counter