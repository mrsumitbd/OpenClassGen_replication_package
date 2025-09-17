class Aggregate(object):
    def __init__(self):
        self.groups = []
        self._finalized = False
        self._query = None

    def add_group(self, key, field, type="terms", opts=None):
        if opts is None:
            opts = {}
        self.groups.append({
            'key': key,
            'field': field,
            'type': type,
            'opts': opts
        })
        return self

    def finalize(self):
        self._finalized = True
        self._query = self.json()
        return self._query

    def json(self):
        def build(idx):
            g = self.groups[idx]
            agg_body = {'field': g['field']}
            agg_body.update(g['opts'])
            node = {g['key']: {g['type']: agg_body}}
            if idx + 1 < len(self.groups):
                node[g['key']]['aggs'] = build(idx + 1)
            return node

        if not self.groups:
            return {}
        return {'aggs': build(0)}

    def parse(self, result):
        aggs = result.get('aggregations', result)
        if not self.groups:
            return []

        rows = []
        keys = [g['key'] for g in self.groups]

        def recurse(level, buckets, path):
            key = keys[level]
            for b in buckets:
                p = path.copy()
                p[key] = b.get('key')
                if level == len(keys) - 1:
                    p['doc_count'] = b.get('doc_count')
                    rows.append(p)
                else:
                    nxt = b.get(keys[level + 1], {})
                    recurse(level + 1, nxt.get('buckets', []), p)

        first = keys[0]
        recurse(0, aggs.get(first, {}).get('buckets', []), {})
        return rows