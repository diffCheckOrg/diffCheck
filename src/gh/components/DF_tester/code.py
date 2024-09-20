#! python3


from ghpythonlib.componentbase import executingcomponent as component

from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import diffCheck
import diffCheck.df_cvt_bindings
from diffCheck import diffcheck_bindings


from ghpythonlib.componentbase import executingcomponent as component
from System.Windows.Forms import ToolStripSeparator
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import math
import fractions

class DFTester(component):
    def __init__(self):
        super(DFTester,self).__init__()
        self.factor = 1
        self.checked1 = False
        self.checked2 = False
        self.checked3 = False

    def RunScript(self, decIn):
        if self.factor == 1: 
            ftIn = decIn
            self.Message = "Make a Choice"
        else: ftIn = self.feet_inches(decIn)
        return ftIn

    def feet_inches(self, decimal):
        tol = round(decimal * self.factor)
        b = math.modf(tol / self.factor)
        feet = int(b[1] // 12)
        inch = int(b[1] % 12)
        fract = fractions.Fraction(b[0])
        if fract == 0:
            fract = ""
        fi = str(feet)+"'- "+str(inch)+" "+str(fract)+'"'
        return fi

    def AppendAdditionalComponentMenuItems(self, items):
        try: #always everything inside try
            #context menu item 1
            component.AppendAdditionalMenuItems(self, items)
            image = None
            items.Items.Add(ToolStripSeparator())
            item = items.Items.Add("Round to 1/2", image, self.OnClicked1)
            item.ToolTipText = "Round 1/2"
            item.Name = "2"
            item.Checked = self.checked1
            #context menu item 2
            item = items.Items.Add("Round to 1/4", image, self.OnClicked2)
            item.ToolTipText = "Round 1/4 "
            item.Name = "4"
            item.Checked = self.checked2
            #context menu item 3
            item = items.Items.Add("Round to 1/8", image, self.OnClicked3)
            item.ToolTipText = "Round 1/8"
            item.Name = "8"
            item.Checked = self.checked3
        except Exception as ex:
            System.Windows.Forms.MessageBox.Show(str(ex))
            
    def OnClicked1(self, index, value):
        try: #always everything inside try
            self.checked1 = not self.checked1
            self.checked2 = False
            self.checked3 = False
            self.factor = int(index.Name)
            self.Message = (index.ToolTipText)
            self.ExpireSolution(True)
        except Exception as ex:
            System.Windows.Forms.MessageBox.Show(str(ex))
    
    def OnClicked2(self, index, value):
        try: #always everything inside try
            self.checked2 = not self.checked2
            self.checked1 = False
            self.checked3 = False
            self.factor = int(index.Name)
            self.Message = (index.ToolTipText)
            self.ExpireSolution(True)
        except Exception as ex:
            System.Windows.Forms.MessageBox.Show(str(ex))
            
    def OnClicked3(self, index, value):
        try: #always everything inside try
            self.checked3 = not self.checked3
            self.checked1 = False
            self.checked2 = False
            self.factor = int(index.Name)
            self.Message = (index.ToolTipText)
            self.ExpireSolution(True)
        except Exception as ex:
            System.Windows.Forms.MessageBox.Show(str(ex))
