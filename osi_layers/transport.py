class TransportLayer:
    def __init__(self):
        self.sequence_number = 0
        
    def create_segment(self, packet):
        """Create TCP-like segment"""
        segment = {
            'sequence_number': self.sequence_number,
            'ack_number': 0,
            'payload': packet
        }
        self.sequence_number += 1
        return segment
        
    def handle_errors(self, segment):
        """Basic error detection"""
        return 'sequence_number' in segment and 'payload' in segment