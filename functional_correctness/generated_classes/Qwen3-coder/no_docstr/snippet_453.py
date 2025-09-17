class ARSCResTablePackage(object):
    def __init__(self, buff):
        self.header = buff.read(272)
        self.header_size = int.from_bytes(self.header[:2], byteorder='little')
        self.type = int.from_bytes(self.header[2:4], byteorder='little')
        self.package_id = int.from_bytes(self.header[8:12], byteorder='little')
        self.name = self.header[12:268].decode('utf-16le').rstrip('\x00')

    def get_name(self):
        return self.name