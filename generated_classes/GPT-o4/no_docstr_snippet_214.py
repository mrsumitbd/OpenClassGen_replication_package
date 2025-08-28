class RevlinkMultiplexer:
    def __init__(self, *revlinks):
        self.revlinks = revlinks

    def __call__(self, rev, repo):
        outputs = []
        for rl in self.revlinks:
            result = rl(rev, repo)
            if result:
                outputs.append(result)
        if not outputs:
            return ''
        if len(outputs) == 1:
            return outputs[0]
        return '\n'.join(outputs)