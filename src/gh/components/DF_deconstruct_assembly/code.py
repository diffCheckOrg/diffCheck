#! python3



from ghpythonlib.componentbase import executingcomponent as component



class DFDeconstructAssembly(component):
    def RunScript(self,
            i_assembly):
        o_beams = i_assembly.beams
        return o_beams
