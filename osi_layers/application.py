class ApplicationLayer:
    def create_request(self, method, resource, data):
        """Create HTTP-like request"""
        request = {
            'method': method,
            'resource': resource,
            'headers': {
                'Content-Type': 'application/json',
                'Content-Length': len(str(data))
            },
            'body': data
        }
        return request
        
    def create_response(self, status_code, data):
        """Create HTTP-like response"""
        response = {
            'status_code': status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Content-Length': len(str(data))
            },
            'body': data
        }
        return response