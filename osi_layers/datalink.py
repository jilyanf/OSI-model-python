import socket
import uuid

class DataLinkLayer:
    def __init__(self):
        self.mac_address = self._get_mac_address()
        
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
    
    def _get_mac_address(self):
        """Get the MAC address of the current machine"""
        try:
            # Get the MAC address (hardware address)
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                           for elements in range(0, 48, 8)][::-1])
            return mac
        except Exception:
            # Fallback to default MAC if detection fails
            return "00:11:22:33:44:55"