import socket

class NetworkLayer:
    def __init__(self):
        self.ip_address = self._get_ip_address()
        
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
    
    def _get_ip_address(self):
        """Get the IP address of the current machine"""
        try:
            # Create a socket connection to get the local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Doesn't need to be reachable, just to determine interface IP
            s.connect(('8.8.8.8', 1))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            # Fallback to default IP if detection fails
            return "192.168.1.1"