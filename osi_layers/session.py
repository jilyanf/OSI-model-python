class SessionLayer:
    def __init__(self):
        self.session_id = 0
        self.active_sessions = {}
        
    def create_session(self, segment):
        """Establish session"""
        self.session_id += 1
        session = {
            'session_id': self.session_id,
            'state': 'ESTABLISHED',
            'payload': segment
        }
        self.active_sessions[self.session_id] = session
        return session
        
    def end_session(self, session_id):
        """Terminate session"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]