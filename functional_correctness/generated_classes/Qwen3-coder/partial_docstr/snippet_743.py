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

        # Create the directory if it doesn't exist
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # Convert props to JSON string
        props_json = json.dumps(self.props)

        # Read the source file
        with open(self.src_file, 'r') as f:
            src_content = f.read()

        # Create the rendered content
        rendered_content = f'''
// Generated component file
{src_content}

// Render component
const props = {props_json};
const element = React.createElement({self.layout}, props);
ReactDOM.render(element, document.getElementById('{self.component_id}'));
'''

        # Write to the output file
        with open(path, 'w') as f:
            f.write(rendered_content)