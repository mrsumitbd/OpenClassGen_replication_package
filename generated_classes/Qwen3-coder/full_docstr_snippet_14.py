class TemplateRenderer(object):
    '''Foundation Interface Template Renderer for jinja2'''

    def __init__(self, output_root_dir):
        '''Setup the jinja2 environment

        :param str output_root_dir: Root directory in which to write the Foundation interface.
        '''
        self.output_root_dir = output_root_dir
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader('.'),
            keep_trailing_newline=True
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
        if template_data is None:
            template_data = {}

        # Process template filename to create output path
        processed_filename = template_filename.replace('group', group).replace('entity', entity)
        path_parts = processed_filename.split('.')
        
        # Separate template name from path parts
        template_name = path_parts[-1]
        path_parts = path_parts[:-1]
        
        # Create output directory
        output_dir = os.path.join(self.output_root_dir, *path_parts)
        os.makedirs(output_dir, exist_ok=True)
        
        # Create output file path
        output_file = os.path.join(output_dir, template_name)
        
        # Render template
        template = self.env.get_template(template_filename)
        rendered_content = template.render(**template_data)
        
        # Write rendered content to file
        with open(output_file, 'w') as f:
            f.write(rendered_content)