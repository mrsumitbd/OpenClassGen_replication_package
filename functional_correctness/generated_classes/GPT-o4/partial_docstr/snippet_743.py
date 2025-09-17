class SimpleComponent(object):
    '''Simple class for rendering a single component.

    Rather than requiring a collection of filters and charts, this
    function will render a single React component with props
    passed as a dictionary.

    Args:
        layout (str): Name of the React component to render.
        src_file (str): JavaScript module path containing the component.
        component_id (str): HTML element id to mount the component into.
        props (dict): Props for the component.
    '''

    def __init__(self, layout, src_file, component_id, props):
        if not isinstance(layout, str):
            raise TypeError("layout must be a string")
        if not isinstance(src_file, str):
            raise TypeError("src_file must be a string")
        if not isinstance(component_id, str):
            raise TypeError("component_id must be a string")
        if not isinstance(props, dict):
            raise TypeError("props must be a dictionary")

        self.layout = layout
        self.src_file = src_file
        self.component_id = component_id
        self.props = props

    def render(self, path):
        '''Render the component to a JavaScript file.'''
        props_json = json.dumps(self.props, indent=2)
        content = f"""import React from 'react';
import ReactDOM from 'react-dom';
import {{ {self.layout} }} from '{self.src_file}';

const props = {props_json};

ReactDOM.render(
  React.createElement({self.layout}, props),
  document.getElementById('{self.component_id}')
);
"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)