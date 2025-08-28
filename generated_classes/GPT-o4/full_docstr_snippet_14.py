class TemplateRenderer(object):
    '''Foundation Interface Template Renderer for jinja2'''

    def __init__(self, output_root_dir):
        '''Setup the jinja2 environment

        :param str output_root_dir: Root directory in which to write the Foundation interface.
        '''
        self.output_root_dir = os.path.abspath(output_root_dir)
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            undefined=StrictUndefined,
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True
        )

    def render_template(self, template_filename, group="group", entity="entity", template_data=None):
        '''Render one or more jinja2 templates.

        The output filename is relative to the `output_root_dir` defined in the class instance but is also defined by
        the `template_filename`. The `template_filename` should be interspersed with `.` to indicate subdirectories.

        Two place holders are also supported in the template filename:
        - `group`: which will be replaced by the `group` parameter
        - `entity`: which will be replaced by the `entity` parameter

        :param str template_filename: name of template to render, this also defines the output path and filename.
        :param str group: This should be supplied when the template filename contains `group` .
        :param str entity: This should be supplied when the template filename contains `entity`.
        :param dict template_data: Data to pass to the template.
        '''
        # replace placeholders
        fname = template_filename.replace('group', group).replace('entity', entity)
        # split off extension
        parts = fname.split('.')
        if len(parts) > 1:
            ext = parts[-1]
            path_parts = parts[:-1]
            rel_path = os.path.join(*path_parts) + '.' + ext
        else:
            rel_path = fname
        # load and render
        tpl = self.env.get_template(rel_path)
        data = template_data or {}
        rendered = tpl.render(**data)
        # write output
        out_path = os.path.join(self.output_root_dir, rel_path)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(rendered)