class ARSCResTablePackage(object):

    def __init__(self, buff):
        # Read header: type (2), headerSize (2), size (4), id (4)
        header_data = buff.read(12)
        self.type, self.header_size, self.size, self.id = struct.unpack('<HHII', header_data)

        # Read package name: 128 UTF-16LE chars
        name_bytes = buff.read(128 * 2)
        self.name = name_bytes.decode('utf-16le').rstrip('\x00')

        # Read string pool offsets: typeStrings, lastPublicType, keyStrings, lastPublicKey
        rest = buff.read(16)
        self.type_strings, self.last_public_type, self.key_strings, self.last_public_key = struct.unpack('<IIII', rest)

    def get_name(self):
        return self.name