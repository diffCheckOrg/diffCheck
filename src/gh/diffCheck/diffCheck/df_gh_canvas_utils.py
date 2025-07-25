from Grasshopper import Instances
import Grasshopper as gh
import System.Drawing as sd
import System
import typing


def add_str_valuelist(comp,
    values_list: typing.List[str],
    nickname: str,
    indx: int,
    X_param_coord: float,
    Y_param_coord: float,
    X_offset: int = 87
    ) -> None:
    """
        Adds a value list of string values to the component input

        :param values_list: a list of string values to add to the value list
        :param nickname: the nickname of the value list
        :param indx: the index of the input parameter
        :param X_param_coord: the x coordinate of the input parameter
        :param Y_param_coord: the y coordinate of the input parameter
        :param X_offset: the offset of the value list from the input parameter
    """
    inp = comp.Params.Input[indx]  # noqa: F821
    if inp.SourceCount == 0:
        valuelist = gh.Kernel.Special.GH_ValueList()
        valuelist.NickName = nickname
        valuelist.Description = "Select the value to use with DFVizSettings"
        selected = valuelist.FirstSelectedItem
        valuelist.ListItems.Clear()
        for v in values_list:
            vli = gh.Kernel.Special.GH_ValueListItem(str(v), str('"' + v + '"'))
            valuelist.ListItems.Add(vli)
        if selected in values_list:
            valuelist.SelectItem(values_list.index(selected))
        valuelist.CreateAttributes()
        valuelist.Attributes.Pivot = System.Drawing.PointF(
            X_param_coord - (valuelist.Attributes.Bounds.Width) - X_offset,
            Y_param_coord - (valuelist.Attributes.Bounds.Height / 2 + 0.1)
            )
        valuelist.Attributes.ExpireLayout()
        gh.Instances.ActiveCanvas.Document.AddObject(valuelist, False)
        inp.AddSource(valuelist)  # noqa: F821


def add_slider(comp,
    nickname: str,
    indx: int,
    lower_bound: float,
    upper_bound: float,
    default_value: float,
    X_param_coord: float,
    Y_param_coord: float,
    X_offset: int = 100
    ) -> None:
    """
        Adds a slider to the component input

        :param nickname: the nickname of the slider
        :param indx: the index of the input parameter
        :param X_param_coord: the x coordinate of the input parameter
        :param Y_param_coord: the y coordinate of the input parameter
        :param X_offset: the offset of the slider from the input parameter
    """
    inp = comp.Params.Input[indx]  # noqa: F821
    if inp.SourceCount == 0:
        slider = gh.Kernel.Special.GH_NumberSlider()
        slider.NickName = nickname
        slider.Description = "Set the value for the threshold"
        slider.Slider.Minimum = System.Decimal(lower_bound)
        slider.Slider.Maximum = System.Decimal(upper_bound)
        slider.Slider.DecimalPlaces = 3
        slider.Slider.SmallChange = System.Decimal(0.001)
        slider.Slider.LargeChange = System.Decimal(0.01)
        slider.Slider.Value = System.Decimal(default_value)
        slider.CreateAttributes()
        slider.Attributes.Pivot = System.Drawing.PointF(
            X_param_coord - (slider.Attributes.Bounds.Width) - X_offset,
            Y_param_coord - (slider.Attributes.Bounds.Height / 2 - 0.1)
            )
        slider.Attributes.ExpireLayout()
        gh.Instances.ActiveCanvas.Document.AddObject(slider, False)
        inp.AddSource(slider)  # noqa: F821


def add_plane_object(comp,
                     nickname: str,
                     indx: int,
                     X_param_coord: float,
                     Y_param_coord: float,
                     X_offset: int = 75
                     ) -> None:
    """
        Adds a plane object to the component input

        :param nickname: the nickname of the plane object
        :param indx: the index of the input parameter
        :param X_param_coord: the x coordinate of the input parameter
        :param Y_param_coord: the y coordinate of the input parameter
        :param X_offset: the offset of the plane object from the input parameter
    """
    inp = comp.Params.Input[indx]  # noqa: F821
    if inp.SourceCount == 0:
        doc = Instances.ActiveCanvas.Document
        if doc:
            plane = gh.Kernel.Parameters.Param_Plane()
            plane.NickName = nickname
            plane.CreateAttributes()
            plane.Attributes.Pivot = System.Drawing.PointF(
                X_param_coord - (plane.Attributes.Bounds.Width) - X_offset,
                Y_param_coord
                )
            plane.Attributes.ExpireLayout()
            doc.AddObject(plane, False)
            inp.AddSource(plane)  # noqa: F821


def add_button(comp,
               nickname: str,
               indx: int,
               x_offset: int = 60
               ) -> None:
    """
    Adds a one-shot Boolean button to the left of a component input.

    :param comp: The Grasshopper component to which the button will be added.
    :param nickname: The display label of the button (e.g. "Start", "Load").
    :param indx: The index of the component input to wire the button into.
    :param x_offset: Horizontal distance (in pixels) to place the button to the left of the input.
    """

    inp = comp.Params.Input[indx]
    # only add if nothing already connected
    if inp.SourceCount == 0:
        # create the one-shot button
        btn = gh.Kernel.Special.GH_ButtonObject()
        btn.NickName = nickname
        btn.Value = False   # always starts False
        # build its UI attributes so we can measure size & position
        btn.CreateAttributes()

        # compute pivot: left of the input grip
        grip = inp.Attributes.InputGrip
        # X = input pivot X, Y = grip Y
        pivot_x = grip.X - btn.Attributes.Bounds.Width - x_offset
        pivot_y = grip.Y - btn.Attributes.Bounds.Height/2
        btn.Attributes.Pivot = sd.PointF(pivot_x, pivot_y)
        btn.Attributes.ExpireLayout()

        # drop it onto the canvas (non-grouped)
        Instances.ActiveCanvas.Document.AddObject(btn, False)
        # wire it into the component
        inp.AddSource(btn)


def add_panel(comp,
              nickname: str,
              text: str,
              indx: int,
              x_offset: int = 60,
              panel_height: int = 20
              ) -> None:
    """
    Adds a text panel to the left of a component input with a default string value.

    :param comp: The Grasshopper component to which the panel will be added.
    :param nickname: The label shown at the top of the panel (e.g. "Host", "Port").
    :param text: The default string to display inside the panel.
    :param indx: The index of the component input to connect the panel to.
    :param x_offset: Horizontal distance (in pixels) to place the panel left of the input.
    :param panel_height: Height of the panel in pixels (default is 20).

    :returns: None. The panel is created, positioned, and connected if no existing source is present.
    """

    inp = comp.Params.Input[indx]
    if inp.SourceCount == 0:
        panel = gh.Kernel.Special.GH_Panel()
        # Set the panel's displayed text
        panel.UserText = text
        panel.NickName = nickname
        panel.CreateAttributes()

        # adjust height while preserving width
        bounds = panel.Attributes.Bounds
        panel.Attributes.Bounds = System.Drawing.RectangleF(
            bounds.X,
            bounds.Y,
            bounds.Width,
            panel_height
        )

        # Position left of input grip
        grip = inp.Attributes.InputGrip
        px = grip.X - panel.Attributes.Bounds.Width - x_offset
        py = grip.Y - panel.Attributes.Bounds.Height / 2
        panel.Attributes.Pivot = sd.PointF(px, py)
        panel.Attributes.ExpireLayout()
        Instances.ActiveCanvas.Document.AddObject(panel, False)
        inp.AddSource(panel)
