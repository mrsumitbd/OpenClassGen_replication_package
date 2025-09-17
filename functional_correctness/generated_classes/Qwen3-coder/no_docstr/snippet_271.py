class PanelMetricsHelper:
    def front_to_back(self, name):
        """Convert front panel name to back panel name"""
        if name.startswith('front_'):
            return name.replace('front_', 'back_', 1)
        return 'back_' + name

    def back_to_front(self, name):
        """Convert back panel name to front panel name"""
        if name.startswith('back_'):
            return name.replace('back_', 'front_', 1)
        return 'front_' + name

    def special_front_to_back(self, name):
        """Convert special front panel name to back panel name"""
        special_mappings = {
            'front_panel': 'back_panel',
            'front_door': 'back_door',
            'front_window': 'back_window',
            'front_wall': 'back_wall',
            'front_side': 'back_side'
        }
        return special_mappings.get(name, self.front_to_back(name))

    def special_back_to_front(self, name):
        """Convert special back panel name to front panel name"""
        special_mappings = {
            'back_panel': 'front_panel',
            'back_door': 'front_door',
            'back_window': 'front_window',
            'back_wall': 'front_wall',
            'back_side': 'front_side'
        }
        return special_mappings.get(name, self.back_to_front(name))