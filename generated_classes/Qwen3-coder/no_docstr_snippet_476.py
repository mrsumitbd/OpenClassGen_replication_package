class JsonMixin(object):

    @staticmethod
    def add_json_options(
        parser,  # type: _ActionsContainer
        entity,  # type: str
        include_switch=True,  # type: bool
    ):
        if include_switch:
            parser.add_argument(
                '--json',
                action='store_true',
                help=f'Output {entity} information in JSON format'
            )
        parser.add_argument(
            '--indent',
            type=int,
            default=2,
            help='JSON indentation level (default: 2)'
        )
        parser.add_argument(
            '--compact',
            action='store_true',
            help='Output compact JSON without extra whitespace'
        )

    @staticmethod
    def dump_json(
        options,  # type: Namespace
        data,  # type: Dict[str, Any]
        out,  # type: IO
        **json_dump_kwargs  # type: Any
    ):
        if hasattr(options, 'compact') and options.compact:
            json_dump_kwargs.setdefault('separators', (',', ':'))
            json_dump_kwargs.setdefault('indent', None)
        elif hasattr(options, 'indent'):
            json_dump_kwargs.setdefault('indent', options.indent)
        
        json.dump(data, out, **json_dump_kwargs)
        out.write('\n')