class PrecipitationSimulation(object):

    @staticmethod
    def is_applicable(world):
        return hasattr(world, 'width') and hasattr(world, 'height') and world.width > 0 and world.height > 0

    def execute(self, world, seed):
        world.precipitation = self._calculate(seed, world)

    @staticmethod
    def _calculate(seed, world):
        """Precipitation is a value in [-1,1]"""
        rng = random.Random(seed)
        precip = []
        for y in range(world.height):
            row = []
            for x in range(world.width):
                row.append(rng.uniform(-1.0, 1.0))
            precip.append(row)
        return precip