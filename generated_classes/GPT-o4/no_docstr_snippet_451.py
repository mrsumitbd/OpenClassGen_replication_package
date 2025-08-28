class BundleOptionsMixin(object):

    def add_arguments(self, parser):
        parser.add_argument(
            '-o', '--output-dir',
            dest='output_dir',
            default=os.getcwd(),
            help='Directory in which to place the bundle'
        )
        parser.add_argument(
            '-f', '--format',
            dest='format',
            choices=['zip', 'tar', 'gztar', 'bztar', 'xztar'],
            default='gztar',
            help='Bundle archive format'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            dest='force',
            help='Overwrite existing bundles'
        )
        parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            dest='verbose',
            help='Enable verbose output'
        )

    def get_system_opts(self, options):
        return {
            'output_dir': options.output_dir,
            'format':     options.format,
            'force':      options.force,
            'verbose':    options.verbose,
        }