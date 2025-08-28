class _LazyTree(object):
    def __init__(self, path, treepath, tree, interpretation, flatten, awkwardlib, basketcache, keycache, executor):
        self._path = path
        self._treepath = treepath
        self._tree = tree
        self._interpretation = interpretation
        self._flatten = flatten
        self._awkwardlib = awkwardlib
        self._basketcache = basketcache
        self._keycache = keycache
        self._executor = executor
        self._initialized = False

    def _init(self):
        if not self._initialized:
            if self._tree is None:
                import uproot
                file = uproot.open(self._path)
                self._tree = file[self._treepath]
            self._initialized = True

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove unpicklable entries
        if '_tree' in state and hasattr(state['_tree'], '_file'):
            state['_tree'] = None
        state['_initialized'] = False
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._initialized = False

    def __call__(self, branch, entrystart, entrystop):
        self._init()
        return self._tree.array(
            branch,
            entrystart=entrystart,
            entrystop=entrystop,
            interpretation=self._interpretation,
            flatten=self._flatten,
            awkwardlib=self._awkwardlib,
            basketcache=self._basketcache,
            keycache=self._keycache,
            executor=self._executor
        )