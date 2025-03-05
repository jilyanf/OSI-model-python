class DataLinkLayer:
    def __init__(self):
        self.mac_address = "00:11:22:33:44:55"
        
    def create_frame(self, data, dest_mac):
        """Create a frame with MAC addressing"""
        frame = {
            'source_mac': self.mac_address,
            'dest_mac': dest_mac,
            'payload': data,
            'checksum': self._calculate_checksum(str(data))
        }
        return frame
        
    def _calculate_checksum(self, data):
        """Calculate simple checksum"""
        return sum(ord(c) for c in str(data)) & 0xFF