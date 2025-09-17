class SimpleComponent(object):
    '''Simple class for rendering a single component.

        Rather than requiring a collection of filters and charts, this
        function will render a single react component with props
        passed as a dictionary.

        Args:
            layout (str): Type of react component to create.
            src_file (str): javascript file containing the component.
            component_id (str): html element id.
            props (dict): props for the component.
    '''

    def __init__(self, layout, src_file, component_id, props):
        self.layout = layout
        self.src_file = src_file
        self.component_id = component_id
        self.props = props

    def render(self, path):
        '''Render the component to a javascript file.'''
        import json
        import os
        
        props_json = json.dumps(self.props)
        
        js_content = f"""
import React from 'react';
import ReactDOM from 'react-dom';
import {self.layout} from './{self.src_file}';

const props = {props_json};

ReactDOM.render(
    React.createElement({self.layout}, props),
    document.getElementById('{self.component_id}')
);
"""
        
        with open(path, 'w') as f:
            f.write(js_content.strip())