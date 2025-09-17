class BundleOptionsMixin(object):
    def add_arguments(self, parser):
        parser.add_argument(
            '--bundle-dir',
            dest='bundle_dir',
            help='Directory to store bundle files'
        )
        parser.add_argument(
            '--bundle-format',
            dest='bundle_format',
            choices=['tar', 'zip', 'tar.gz', 'tar.bz2'],
            default='tar.gz',
            help='Bundle format (default: tar.gz)'
        )
        parser.add_argument(
            '--bundle-name',
            dest='bundle_name',
            help='Name of the bundle file'
        )
        parser.add_argument(
            '--include-dependencies',
            dest='include_dependencies',
            action='store_true',
            help='Include dependencies in bundle'
        )
        parser.add_argument(
            '--exclude-patterns',
            dest='exclude_patterns',
            nargs='*',
            help='Patterns to exclude from bundle'
        )

    def get_system_opts(self, options):
        system_opts = {}
        
        if hasattr(options, 'bundle_dir') and options.bundle_dir:
            system_opts['bundle_dir'] = options.bundle_dir
            
        if hasattr(options, 'bundle_format') and options.bundle_format:
            system_opts['bundle_format'] = options.bundle_format
            
        if hasattr(options, 'bundle_name') and options.bundle_name:
            system_opts['bundle_name'] = options.bundle_name
            
        if hasattr(options, 'include_dependencies'):
            system_opts['include_dependencies'] = options.include_dependencies
            
        if hasattr(options, 'exclude_patterns') and options.exclude_patterns:
            system_opts['exclude_patterns'] = options.exclude_patterns
            
        return system_opts