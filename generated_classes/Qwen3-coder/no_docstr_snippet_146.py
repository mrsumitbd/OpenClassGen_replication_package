class VifPort(object):
    def __init__(self, port_name, ofport, vif_id, vif_mac, switch):
        self.port_name = port_name
        self.ofport = ofport
        self.vif_id = vif_id
        self.vif_mac = vif_mac
        self.switch = switch

    def __str__(self):
        return ("VifPort(port_name=%s, ofport=%s, vif_id=%s, vif_mac=%s, switch=%s)" % 
                (self.port_name, self.ofport, self.vif_id, self.vif_mac, self.switch))