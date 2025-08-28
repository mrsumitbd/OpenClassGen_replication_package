class RouteCQC:
    def setup(self, qubits: int, depth: int, op_density: float, grid_device_size: int):
        self.qubits = qubits
        self.depth = depth
        self.op_density = op_density
        self.grid_device_size = grid_device_size
        self.results = []
        self.depth_ratios = []
        # Build grid coupling map
        size = grid_device_size
        edges = []
        for i in range(size):
            for j in range(size):
                idx = i * size + j
                if idx >= qubits:
                    continue
                if i + 1 < size:
                    idx2 = (i + 1) * size + j
                    if idx2 < qubits:
                        edges.append([idx, idx2])
                if j + 1 < size:
                    idx2 = i * size + (j + 1)
                    if idx2 < qubits:
                        edges.append([idx, idx2])
        self.coupling_map = CouplingMap(edges)

    def time_circuit_routing(self, *_):
        circ = random_circuit(self.qubits, self.depth, self.op_density, measure=False)
        orig_depth = circ.depth()
        start = time.perf_counter()
        routed = transpile(circ, coupling_map=self.coupling_map, optimization_level=1, routing_method='sabre')
        end = time.perf_counter()
        routed_depth = routed.depth()
        self.results.append(end - start)
        self.depth_ratios.append(routed_depth / orig_depth if orig_depth > 0 else 0.0)
        return end - start

    def track_routed_circuit_depth_ratio(self, *_) -> float:
        if not self.depth_ratios:
            return 0.0
        return sum(self.depth_ratios) / len(self.depth_ratios)

    def teardown(self, *_):
        for attr in ['qubits', 'depth', 'op_density', 'grid_device_size',
                     'results', 'depth_ratios', 'coupling_map']:
            if hasattr(self, attr):
                delattr(self, attr)