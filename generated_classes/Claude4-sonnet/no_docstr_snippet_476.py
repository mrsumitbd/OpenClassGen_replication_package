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
                help=f'Output {entity} in JSON format'
            )
        parser.add_argument(
            '--json-indent',
            type=int,
            metavar='N',
            help='JSON output indentation level'
        )
        parser.add_argument(
            '--json-sort-keys',
            action='store_true',
            help='Sort JSON output keys'
        )

    @staticmethod
    def dump_json(
        options,  # type: Namespace
        data,  # type: Dict[str, Any]
        out,  # type: IO
        **json_dump_kwargs  # type: Any
    ):
        dump_kwargs = json_dump_kwargs.copy()
        
        if hasattr(options, 'json_indent') and options.json_indent is not None:
            dump_kwargs['indent'] = options.json_indent
        
        if hasattr(options, 'json_sort_keys') and options.json_sort_keys:
            dump_kwargs['sort_keys'] = True
        
        json.dump(data, out, **dump_kwargs)