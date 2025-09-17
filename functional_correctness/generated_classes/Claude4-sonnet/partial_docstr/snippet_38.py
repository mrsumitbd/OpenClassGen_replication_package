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
        return f"Image(base_dir='{self.base_dir}', template_path='{self.template_path}')"

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
        template_full_path = os.path.join(self.base_dir, self.template_path)
        
        cmd = ['packer', 'build', template_full_path]
        
        env = os.environ.copy()
        if hasattr(context, 'variables'):
            for key, value in context.variables.items():
                env[f'PKR_VAR_{key}'] = str(value)
        
        subprocess.run(cmd, cwd=self.base_dir, env=env, check=True)

    def delete(self, context):
        '''
        Does nothing.

        :param resort.engine.execution.Context context:
           Current execution context.
        '''
        pass