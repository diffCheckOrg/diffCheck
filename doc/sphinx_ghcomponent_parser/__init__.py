import os
import json

from docutils import nodes
from docutils.core import publish_parts

from docutils.parsers.rst import Directive
from sphinx.util.docutils import SphinxDirective
from docutils.statemachine import StringList

from . import metadata_parser

class GhComponentToRSTDirective(SphinxDirective):
    has_content = False
    required_arguments = 1

    def run(self):
        ghcomponent_dir = self.arguments[0]
        if not os.path.isabs(ghcomponent_dir):
            ghcomponent_dir = os.path.join(self.env.srcdir, ghcomponent_dir)
        if not os.path.exists(ghcomponent_dir):
            return [self.state_machine.reporter.warning(
                f'GHComponent directory not found: {ghcomponent_dir}', line=self.lineno)]
        metadata_json_file = os.path.join(ghcomponent_dir, 'metadata.json')
        pycode_file = os.path.join(ghcomponent_dir, 'code.py')
        icon_file = os.path.join(ghcomponent_dir, 'icon.png')
        
        metadata = metadata_parser.MetadataParser(metadata_json_file)

        ##########################################################################
        # RST content
        ##########################################################################
        # to be  used in toctree directive needs an unique id
        section = nodes.section(ids=["211c205b-cacd-486a-b321-d0d98bf1a6c7"])
        #-------------------------------------------------------------------------
        # general description
        section += nodes.Text(metadata.get_description())
        #-------------------------------------------------------------------------
        # input parameters
        subtitle_input = nodes.subtitle()
        subtitle_input_text = nodes.strong(text="Inputs:")
        subtitle_input += subtitle_input_text
        section += subtitle_input

        table = nodes.table()
        tgroup = nodes.tgroup(cols=2)
        table += tgroup
        tgroup += nodes.colspec(colwidth=1)
        tgroup += nodes.colspec(colwidth=1)
        
        tbody = nodes.tbody()
        tgroup += tbody
        if metadata.get_input_parameters():
            for param in metadata.get_input_parameters():
                row = nodes.row()
                entry = nodes.entry()
                entry += nodes.paragraph('', '', nodes.literal(text=f"{param['name']}"), nodes.Text(f" ({param['typeHintID']} ,{param['scriptParamAccess']})"))
                row += entry
                row += nodes.entry('', nodes.paragraph(text=param['description']))
                tbody += row
        section += table
        #-------------------------------------------------------------------------
        # output parameters
        subtitle_output = nodes.subtitle()
        subtitle_output_text = nodes.strong(text="Outputs:")
        subtitle_output += subtitle_output_text
        section += subtitle_output

        table = nodes.table()
        tgroup = nodes.tgroup(cols=2)
        table += tgroup
        tgroup += nodes.colspec(colwidth=1)
        tgroup += nodes.colspec(colwidth=1)
        
        tbody = nodes.tbody()
        tgroup += tbody
        if metadata.get_output_parameters():
            for param in metadata.get_output_parameters():
                row = nodes.row()
                row += nodes.entry('', nodes.literal(text=f"{param['name']}"))
                row += nodes.entry('', nodes.paragraph(text=param['description']))
                tbody += row
        section += table
        #-------------------------------------------------------------------------
        # code block
        subtitle_code = nodes.subtitle()
        subtitle_code_text = nodes.strong(text="Code:")
        subtitle_code += subtitle_code_text
        section += subtitle_code

        with open(pycode_file, 'r') as file:
            code_block_text = file.read()
        code_block = nodes.literal_block()
        code_block += nodes.Text(code_block_text)
        section += code_block
        #-------------------------------------------------------------------------
        return [section]


def setup(app):
    app.add_directive("ghcomponent_to_rst", GhComponentToRSTDirective)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }