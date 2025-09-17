class RevlinkMultiplexer:
    def __init__(self, *revlinks):
        self.revlinks = revlinks

    def __call__(self, rev, repo):
        for revlink in self.revlinks:
            result = revlink(rev, repo)
            if result:
                return result
        return None