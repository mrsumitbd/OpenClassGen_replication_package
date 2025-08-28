class PrecipitationSimulation(object):

    @staticmethod
    def is_applicable(world):
        return hasattr(world, 'temperature') and hasattr(world, 'humidity') and hasattr(world, 'elevation')

    def execute(self, world, seed):
        precipitation = self._calculate(seed, world)
        world.precipitation = precipitation
        return world

    @staticmethod
    def _calculate(seed, world):
        '''Precipitation is a value in [-1,1]'''
        random.seed(seed)
        
        # Base precipitation from humidity
        base_precipitation = (world.humidity - 0.5) * 2
        
        # Temperature effect (moderate temperatures favor precipitation)
        temp_factor = 1 - abs(world.temperature - 0.5) * 2
        
        # Elevation effect (higher elevation can increase precipitation)
        elevation_factor = 1 + (world.elevation * 0.3)
        
        # Random variation
        noise = random.uniform(-0.2, 0.2)
        
        # Calculate final precipitation
        precipitation = base_precipitation * temp_factor * elevation_factor + noise
        
        # Clamp to [-1, 1]
        precipitation = max(-1, min(1, precipitation))
        
        return precipitation