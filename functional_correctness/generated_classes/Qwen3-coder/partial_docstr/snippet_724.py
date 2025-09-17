class PrecipitationSimulation(object):

    @staticmethod
    def is_applicable(world):
        return hasattr(world, 'heightmap') and hasattr(world, 'precipitation')

    def execute(self, world, seed):
        if not self.is_applicable(world):
            return False
        
        precipitation_map = self._calculate(seed, world)
        world.precipitation = precipitation_map
        return True

    @staticmethod
    def _calculate(seed, world):
        '''Precipitation is a value in [-1,1]'''
        random.seed(seed)
        heightmap = world.heightmap
        rows, cols = len(heightmap), len(heightmap[0])
        precipitation = [[0.0 for _ in range(cols)] for _ in range(rows)]
        
        # Generate base precipitation with some noise
        for i in range(rows):
            for j in range(cols):
                # Base value with some randomness
                base_precip = random.uniform(-0.5, 0.5)
                
                # Modify based on height (higher elevations might get more/less precip)
                height_factor = heightmap[i][j]
                elevation_effect = -0.3 * height_factor  # Higher = drier
                
                # Add some spatial correlation
                if i > 0 and j > 0:
                    neighbor_influence = 0.2 * (precipitation[i-1][j] + precipitation[i][j-1]) / 2
                else:
                    neighbor_influence = 0
                
                precip_value = base_precip + elevation_effect + neighbor_influence
                
                # Clamp to [-1, 1]
                precipitation[i][j] = max(-1.0, min(1.0, precip_value))
        
        return precipitation