class BundleOptionsMixin(object):

    def add_arguments(self, parser):
        parser.add_argument(
            '--system',
            action='store_true',
            help='Include system packages in the bundle'
        )
        parser.add_argument(
            '--no-system',
            action='store_true',
            help='Exclude system packages from the bundle'
        )
        parser.add_argument(
            '--compress',
            action='store_true',
            help='Compress the bundle'
        )
        parser.add_argument(
            '--format',
            choices=['tar', 'zip', 'dir'],
            default='tar',
            help='Bundle format (default: tar)'
        )

    def get_system_opts(self, options):
        if options.system and options.no_system:
            raise ValueError("Cannot specify both --system and --no-system")
        return {
            'include_system': options.system,
            'exclude_system': options.no_system,
            'compress': getattr(options, 'compress', False),
            'format': getattr(options, 'format', 'tar')
        }