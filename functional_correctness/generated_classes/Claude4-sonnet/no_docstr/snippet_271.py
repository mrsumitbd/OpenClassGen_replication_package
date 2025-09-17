class PanelMetricsHelper:
    def __init__(self):
        self.front_to_back_mapping = {
            'width': 'depth',
            'height': 'height',
            'depth': 'width',
            'x': 'z',
            'y': 'y',
            'z': 'x',
            'left': 'front',
            'right': 'back',
            'front': 'right',
            'back': 'left',
            'top': 'top',
            'bottom': 'bottom'
        }
        
        self.back_to_front_mapping = {v: k for k, v in self.front_to_back_mapping.items()}
        
        self.special_front_to_back_mapping = {
            'panel_width': 'panel_depth',
            'panel_height': 'panel_height',
            'panel_depth': 'panel_width',
            'offset_x': 'offset_z',
            'offset_y': 'offset_y',
            'offset_z': 'offset_x',
            'margin_left': 'margin_front',
            'margin_right': 'margin_back',
            'margin_front': 'margin_right',
            'margin_back': 'margin_left',
            'margin_top': 'margin_top',
            'margin_bottom': 'margin_bottom'
        }
        
        self.special_back_to_front_mapping = {v: k for k, v in self.special_front_to_back_mapping.items()}

    def front_to_back(self, name):
        return self.front_to_back_mapping.get(name, name)

    def back_to_front(self, name):
        return self.back_to_front_mapping.get(name, name)

    def special_front_to_back(self, name):
        return self.special_front_to_back_mapping.get(name, name)

    def special_back_to_front(self, name):
        return self.special_back_to_front_mapping.get(name, name)