class Aggregate(object):
    def __init__(self):
        self.groups = {}
        self.aggregations = {}

    def add_group(self, key, field, type="terms", opts=None):
        if opts is None:
            opts = {}
        self.groups[key] = {
            "field": field,
            "type": type,
            "opts": opts
        }
        return self

    def finalize(self):
        aggregations = {}
        for key, group in self.groups.items():
            agg = {group["type"]: {"field": group["field"]}}
            if group["opts"]:
                agg[group["type"]].update(group["opts"])
            aggregations[key] = agg
        self.aggregations = aggregations
        return self

    def json(self):
        if not self.aggregations:
            self.finalize()
        return self.aggregations

    def parse(self, result):
        parsed = {}
        if "aggregations" in result:
            aggregations = result["aggregations"]
            for key, group in self.groups.items():
                if key in aggregations:
                    if group["type"] == "terms":
                        parsed[key] = [
                            {
                                "key": bucket.get("key"),
                                "doc_count": bucket.get("doc_count")
                            }
                            for bucket in aggregations[key].get("buckets", [])
                        ]
                    else:
                        parsed[key] = aggregations[key]
        return parsed