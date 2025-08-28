class ARSCResTablePackage(object):
    def __init__(self, buff):
        self.buff = buff
        self.header_size = int.from_bytes(buff[0:2], byteorder='little')
        self.type = int.from_bytes(buff[2:4], byteorder='little')
        self.size = int.from_bytes(buff[4:8], byteorder='little')
        self.id = int.from_bytes(buff[8:12], byteorder='little')
        self.name_offset = int.from_bytes(buff[12:16], byteorder='little')
        self.type_strings_offset = int.from_bytes(buff[16:20], byteorder='little')
        self.last_public_type = int.from_bytes(buff[20:24], byteorder='little')
        self.key_strings_offset = int.from_bytes(buff[24:28], byteorder='little')
        self.last_public_key = int.from_bytes(buff[28:32], byteorder='little')
        
    def get_name(self):
        if self.name_offset == 0:
            return ""
        
        name_start = self.name_offset
        name_length = int.from_bytes(self.buff[name_start:name_start+2], byteorder='little')
        
        if name_length == 0:
            return ""
            
        name_data = self.buff[name_start+2:name_start+2+(name_length*2)]
        return name_data.decode('utf-16le', errors='ignore').rstrip('\x00')