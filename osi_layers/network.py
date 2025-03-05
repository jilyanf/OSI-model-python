class NetworkLayer:
    def __init__(self):
        self.ip_address = "192.168.1.1"
        
    def create_packet(self, frame, dest_ip):
        """Create IP packet"""
        packet = {
            'source_ip': self.ip_address,
            'dest_ip': dest_ip,
            'ttl': 64,
            'payload': frame
        }
        return packet
        
    def route_packet(self, packet):
        """Simulate routing logic"""
        if packet['ttl'] > 0:
            packet['ttl'] -= 1
            return packet
        return None