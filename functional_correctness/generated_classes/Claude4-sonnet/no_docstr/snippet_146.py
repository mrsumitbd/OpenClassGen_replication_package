class VifPort(object):

    def __init__(self, port_name, ofport, vif_id, vif_mac, switch):
        self.port_name = port_name
        self.ofport = ofport
        self.vif_id = vif_id
        self.vif_mac = vif_mac
        self.switch = switch

    def __str__(self):
        return f"VifPort(port_name={self.port_name}, ofport={self.ofport}, vif_id={self.vif_id}, vif_mac={self.vif_mac}, switch={self.switch})"