class _LazyTree(object):

    __slots__ = ("path", "treepath", "tree", "interpretation", "flatten",
                 "awkwardlib", "basketcache", "keycache", "executor", "_initialized")

    def __init__(self, path, treepath, tree, interpretation,
                 flatten, awkwardlib, basketcache, keycache, executor):
        self.path = path
        self.treepath = treepath
        self.tree = tree
        self.interpretation = interpretation
        self.flatten = flatten
        self.awkwardlib = awkwardlib
        self.basketcache = basketcache
        self.keycache = keycache
        self.executor = executor
        self._initialized = (tree is not None)

    def _init(self):
        if not self._initialized:
            import uproot
            f = uproot.open(self.path)
            self.tree = f[self.treepath]
            self._initialized = True

    def __getstate__(self):
        state = {
            "path":        self.path,
            "treepath":    self.treepath,
            "interpretation": self.interpretation,
            "flatten":     self.flatten,
            "awkwardlib":  self.awkwardlib,
            "basketcache": self.basketcache,
            "keycache":    self.keycache,
            "executor":    self.executor
        }
        return state

    def __setstate__(self, state):
        self.path = state["path"]
        self.treepath = state["treepath"]
        self.interpretation = state["interpretation"]
        self.flatten = state["flatten"]
        self.awkwardlib = state["awkwardlib"]
        self.basketcache = state["basketcache"]
        self.keycache = state["keycache"]
        self.executor = state["executor"]
        self.tree = None
        self._initialized = False

    def __call__(self, branch, entrystart, entrystop):
        self._init()
        arr = self.tree.array(
            branch,
            entry_start=entrystart,
            entry_stop=entrystop,
            library=self.awkwardlib,
            executor=self.executor,
            cache_baskets=self.basketcache,
            cache_keys=self.keycache
        )
        if self.flatten:
            return self.awkwardlib.flatten(arr)
        else:
            return self.interpretation(arr)