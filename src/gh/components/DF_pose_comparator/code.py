#! python3



from ghpythonlib.componentbase import executingcomponent as component


class DFPoseComparator(component):
    def RunScript(self,
            i_scan,
            i_assembly):
        # dump the xml
        o_xml = None
        xml: str = i_assembly.to_xml()
        if i_dump:
            i_assembly.dump_xml(xml, i_export_dir)
        o_xml = xml

        return o_xml
