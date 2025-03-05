class PhysicalLayer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        
    def send_bits(self, data):
        """Convert data to binary representation"""
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        # Convert string data to binary string
        return ''.join(format(ord(c), '08b') for c in str(data))
        
    def receive_bits(self, binary_data):
        """Convert binary back to string data"""
        if isinstance(binary_data, bytes):
            binary_data = binary_data.decode('utf-8')
        # Convert binary string back to text
        text = ''
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i+8]
            text += chr(int(byte, 2))
        return text