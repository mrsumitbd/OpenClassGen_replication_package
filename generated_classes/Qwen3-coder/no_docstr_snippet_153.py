class Pop3ContentLengthHandler(object):

    def capacity(self):
        return 0

    def encode(self, marionette_state, template, to_embed):
        if not to_embed:
            return template
            
        # Find the content length line in the POP3 response
        lines = template.split('\n')
        new_lines = []
        
        for line in lines:
            if line.startswith('Content-Length:'):
                # Extract current content length
                try:
                    current_length = int(line.split(':')[1].strip())
                    # Add the length of data to embed
                    new_length = current_length + len(to_embed)
                    new_lines.append('Content-Length: ' + str(new_length))
                except (ValueError, IndexError):
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        # Join the lines back together
        result = '\n'.join(new_lines)
        
        # Append the data to embed at the end
        if not result.endswith('\n'):
            result += '\n'
        result += to_embed
        
        return result

    def decode(self, marionette_state, ctxt):
        # Find the content length line in the context
        lines = ctxt.split('\n')
        content_length = 0
        
        for line in lines:
            if line.startswith('Content-Length:'):
                try:
                    content_length = int(line.split(':')[1].strip())
                    break
                except (ValueError, IndexError):
                    continue
        
        if content_length > 0:
            # Extract the last 'content_length' characters as the embedded data
            # This assumes the embedded data is appended at the end
            embedded_data = ctxt[-content_length:] if len(ctxt) >= content_length else ctxt
            return embedded_data
        
        return ''