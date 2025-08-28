class Image:
    '''
    Packer image.

    :param str base_dir:
       Template base directory.
    :param str template_path:
       Template file path relative to ``base_dir``.
    '''

    def __init__(self, base_dir, template_path):
        self.base_dir = base_dir
        self.template_path = template_path

    def __repr__(self):
        return "Image(base_dir={!r}, template_path={!r})".format(
            self.base_dir, self.template_path)

    def available(self, context):
        '''
        Always return ``None``.

        :param resort.engine.execution.Context context:
           Current execution context.
        '''
        return None

    def insert(self, context):
        '''
        Build the image.

        :param resort.engine.execution.Context context:
           Current execution context.
        '''
        tpl = os.path.join(self.base_dir, self.template_path)

        # Validate the template
        subprocess.check_call(['packer', 'validate', tpl], cwd=self.base_dir)

        # Build and capture machine-readable output
        output = subprocess.check_output(
            ['packer', 'build', '-machine-readable', tpl],
            cwd=self.base_dir,
            universal_newlines=True
        )

        ami_id = None
        for line in output.splitlines():
            parts = line.split(',')
            # format: timestamp,artifact,0,id,ami-xxxxxx
            if len(parts) >= 5 and parts[1] == 'artifact' and parts[2] == '0' and parts[3] == 'id':
                ami_id = parts[4].strip()
                break

        if not ami_id:
            raise RuntimeError('Failed to parse AMI ID from packer output')

        return ami_id

    def delete(self, context):
        '''
        Does nothing.

        :param resort.engine.execution.Context context:
           Current execution context.
        '''
        pass