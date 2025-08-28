class JsonMixin(object):

    @staticmethod
    def add_json_options(
        parser,  # type: _ActionsContainer
        entity,  # type: str
        include_switch=True,  # type: bool
    ):
        if include_switch:
            parser.add_argument(
                '--%s-json' % entity,
                action='store_true',
                dest='json',
                help='Output %s as JSON' % entity,
            )
        parser.add_argument(
            '--json-indent',
            type=int,
            default=None,
            dest='json_indent',
            help='Indentation level for JSON output',
        )
        parser.add_argument(
            '--json-sort-keys',
            action='store_true',
            default=False,
            dest='json_sort_keys',
            help='Sort the JSON output keys',
        )

    @staticmethod
    def dump_json(
        options,  # type: Namespace
        data,  # type: Dict[str, Any]
        out,  # type: IO
        **json_dump_kwargs  # type: Any
    ):
        if getattr(options, 'json', True) is False:
            return False
        indent = getattr(options, 'json_indent', None)
        sort_keys = getattr(options, 'json_sort_keys', False)
        json_dump_kwargs.setdefault('indent', indent)
        json_dump_kwargs.setdefault('sort_keys', sort_keys)
        if 'separators' not in json_dump_kwargs and indent is None:
            json_dump_kwargs['separators'] = (',', ':')
        json.dump(data, out, **json_dump_kwargs)
        out.write('\n')
        return True