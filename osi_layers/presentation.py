import json
import base64

class PresentationLayer:
    def encode_data(self, data):
        """Encode data for transmission"""
        try:
            # Convert to JSON-compatible format
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            return json.dumps(data)
        except Exception as e:
            return None
            
    def decode_data(self, data):
        """Decode received data"""
        try:
            return json.loads(data)
        except Exception as e:
            return None