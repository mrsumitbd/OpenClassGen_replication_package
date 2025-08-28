class Aggregate(object):
    def __init__(self):
        self.aggregations = {}
        self.finalized = False

    def add_group(self, key, field, type="terms", opts=None):
        if opts is None:
            opts = {}
        
        agg_config = {
            type: {
                "field": field,
                **opts
            }
        }
        
        self.aggregations[key] = agg_config
        return self

    def finalize(self):
        self.finalized = True
        return self

    def json(self):
        return {
            "aggs": self.aggregations
        }

    def parse(self, result):
        if "aggregations" not in result:
            return {}
        
        parsed = {}
        for key, agg_result in result["aggregations"].items():
            if "buckets" in agg_result:
                parsed[key] = []
                for bucket in agg_result["buckets"]:
                    bucket_data = {
                        "key": bucket["key"],
                        "doc_count": bucket["doc_count"]
                    }
                    parsed[key].append(bucket_data)
            else:
                parsed[key] = agg_result
        
        return parsed