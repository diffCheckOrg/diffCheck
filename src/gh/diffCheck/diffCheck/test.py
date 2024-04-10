#! python3

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino

tol=sc.doc.ModelAbsoluteTolerance
breps = Rhino.Geometry.Brep.CreatePlanarBreps(i_crvs, tol)
o_brep = breps[0]