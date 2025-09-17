class Pop3ContentLengthHandler(object):
    def __init__(self):
        self.max_capacity = 4  # Can encode up to 9999 in 4 digits

    def capacity(self):
        return self.max_capacity

    def encode(self, marionette_state, template, to_embed):
        if len(to_embed) > 9999:
            raise ValueError("Data too large to embed in POP3 content length")
        
        # Convert data length to 4-digit string
        length_str = str(len(to_embed)).zfill(4)
        
        # Find content-length header in template and replace
        lines = template.split('\n')
        for i, line in enumerate(lines):
            if line.lower().startswith('content-length:'):
                lines[i] = f'Content-Length: {length_str}'
                break
        else:
            # Add content-length header if not found
            header_end = template.find('\r\n\r\n')
            if header_end == -1:
                header_end = template.find('\n\n')
                if header_end == -1:
                    lines.append(f'Content-Length: {length_str}')
                else:
                    lines.insert(-1, f'Content-Length: {length_str}')
            else:
                lines.insert(-1, f'Content-Length: {length_str}')
        
        return '\n'.join(lines)

    def decode(self, marionette_state, ctxt):
        lines = ctxt.split('\n')
        for line in lines:
            if line.lower().startswith('content-length:'):
                length_str = line.split(':', 1)[1].strip()
                try:
                    length = int(length_str)
                    return str(length).encode()
                except ValueError:
                    continue
        return b''