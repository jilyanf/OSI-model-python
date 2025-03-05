from osi_layers.physical import PhysicalLayer
from osi_layers.datalink import DataLinkLayer
from osi_layers.network import NetworkLayer
from osi_layers.transport import TransportLayer
from osi_layers.session import SessionLayer
from osi_layers.presentation import PresentationLayer
from osi_layers.application import ApplicationLayer
import json

class OSIStack:
    def __init__(self):
        self.physical = PhysicalLayer()
        self.datalink = DataLinkLayer()
        self.network = NetworkLayer()
        self.transport = TransportLayer()
        self.session = SessionLayer()
        self.presentation = PresentationLayer()
        self.application = ApplicationLayer()
        
    def send_data(self, method, resource, data, dest_mac, dest_ip):
        """Send data down through all OSI layers"""
        try:
            # Application Layer
            request = self.application.create_request(method, resource, data)
            
            # Presentation Layer
            encoded_data = self.presentation.encode_data(request)
            
            # Session Layer
            session = self.session.create_session(encoded_data)
            
            # Transport Layer
            segment = self.transport.create_segment(session)
            
            # Network Layer
            packet = self.network.create_packet(segment, dest_ip)
            routed_packet = self.network.route_packet(packet)
            
            # Data Link Layer
            frame = self.datalink.create_frame(routed_packet, dest_mac)
            
            # Physical Layer
            binary_data = self.physical.send_bits(json.dumps(frame))
            
            return binary_data
            
        except Exception as e:
            raise Exception(f"Error in send_data: {str(e)}")
        
    def receive_data(self, binary_data):
        """Receive data up through all OSI layers"""
        try:
            # Physical Layer
            raw_data = self.physical.receive_bits(binary_data)
            
            # Parse the JSON data
            frame = json.loads(raw_data)
            
            # Data Link Layer
            if frame['checksum'] != self.datalink._calculate_checksum(str(frame['payload'])):
                return None
                
            # Network Layer
            packet = frame['payload']
            if not self.network.route_packet(packet):
                return None
                
            # Transport Layer
            segment = packet['payload']
            if not self.transport.handle_errors(segment):
                return None
                
            # Session Layer
            session = segment['payload']
            if session['session_id'] not in self.session.active_sessions:
                return None
                
            # Presentation Layer
            decoded_data = self.presentation.decode_data(session['payload'])
            
            # Application Layer
            response = self.application.create_response(200, decoded_data)
            
            return response
            
        except Exception as e:
            raise Exception(f"Error in receive_data: {str(e)}")