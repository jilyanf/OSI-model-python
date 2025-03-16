from osi_layers.physical import PhysicalLayer
from osi_layers.datalink import DataLinkLayer
from osi_layers.network import NetworkLayer
from osi_layers.transport import TransportLayer
from osi_layers.session import SessionLayer
from osi_layers.presentation import PresentationLayer
from osi_layers.application import ApplicationLayer
import json

class OSIStack:
    def __init__(self, verbose=True):
        self.physical = PhysicalLayer()
        self.datalink = DataLinkLayer()
        self.network = NetworkLayer()
        self.transport = TransportLayer()
        self.session = SessionLayer()
        self.presentation = PresentationLayer()
        self.application = ApplicationLayer()
        self.verbose = verbose
        
    def log(self, layer, message, data=None):
        """Print verbose information if enabled"""
        if self.verbose:
            print(f"[{layer.upper()}] {message}")
            if data is not None:
                if isinstance(data, str) and len(data) > 200:
                    print(f"  Data: {data[:100]}...{data[-100:]}")
                else:
                    print(f"  Data: {data}")
                print()
        
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
            
            print("\n[✓] Data successfully sent through all OSI layers")
            return binary_data
            
        except Exception as e:
            print(f"\n[✗] Error in send_data: {str(e)}")
            raise
        
    def receive_data(self, binary_data):
        """Receive data up through all OSI layers"""
        try:
            # Physical Layer
            self.log("PHYSICAL", "Receiving binary data", binary_data[:50] + "..." if len(binary_data) > 50 else binary_data)
            raw_data = self.physical.receive_bits(binary_data)
            self.log("PHYSICAL", "Converted to raw data")
            
            # Parse the JSON data
            frame = json.loads(raw_data)
            
            # Data Link Layer
            self.log("DATA LINK", f"Verifying frame from {frame['source_mac']} to {frame['dest_mac']}")
            self.log("DATA LINK", f"Checking checksum: {frame['checksum']}")
            calculated_checksum = self.datalink._calculate_checksum(str(frame['payload']))
            
            if frame['checksum'] != calculated_checksum:
                self.log("DATA LINK", f"Checksum failed: Expected {frame['checksum']}, Got {calculated_checksum}")
                return None
            self.log("DATA LINK", "Checksum verified ✓")
                
            # Network Layer
            packet = frame['payload']
            self.log("NETWORK", f"Routing packet from {packet['source_ip']} to {packet['dest_ip']}")
            self.log("NETWORK", f"Current TTL: {packet['ttl']}")
            
            if not self.network.route_packet(packet):
                self.log("NETWORK", "Packet routing failed - TTL expired")
                return None
            self.log("NETWORK", "Packet routed successfully ✓")
                
            # Transport Layer
            segment = packet['payload']
            self.log("TRANSPORT", f"Checking segment sequence: {segment['sequence_number']}")
            
            if not self.transport.handle_errors(segment):
                self.log("TRANSPORT", "Transport error handling failed")
                return None
            self.log("TRANSPORT", "Segment verified ✓")
                
            # Session Layer
            session = segment['payload']
            self.log("SESSION", f"Verifying session ID: {session['session_id']}")
            self.log("SESSION", f"Session state: {session['state']}")
            
            if session['session_id'] not in self.session.active_sessions:
                self.log("SESSION", "Session verification failed - Unknown session")
                return None
            self.log("SESSION", "Session verified ✓")
                
            # Presentation Layer
            self.log("PRESENTATION", "Decoding data", session['payload'])
            decoded_data = self.presentation.decode_data(session['payload'])
            self.log("PRESENTATION", "Data decoded successfully ✓", decoded_data)
            
            # Application Layer
            self.log("APPLICATION", "Creating response")
            response = self.application.create_response(200, decoded_data)
            self.log("APPLICATION", "Response created with status code 200 ✓", response)
            
            print("\n[✓] Data successfully received through all OSI layers")
            return response
            
        except Exception as e:
            print(f"\n[✗] Error in receive_data: {str(e)}")
            raise

if __name__ == "__main__":
    print("=================================================")
    print("           OSI MODEL DATA FLOW VISUALIZER         ")
    print("=================================================")
    
    # Create OSI stack instance with verbose=False to suppress sending output
    osi_stack = OSIStack(verbose=False)
    
    # Sample data to transmit
    method = "GET"
    resource = "/api/users"
    data = {"id": 123, "name": "Test User", "role": "admin"}
    dest_mac = "AA:BB:CC:DD:EE:FF"
    dest_ip = "192.168.1.100"
    
    print(f"\nRequest Information:")
    print(f"  Method: {method}")
    print(f"  Resource: {resource}")
    print(f"  Data: {json.dumps(data)}")
    print(f"  Destination MAC: {dest_mac}")
    print(f"  Destination IP: {dest_ip}")
    
    try:
        # Send data through the stack (silently)
        binary_data = osi_stack.send_data(method, resource, data, dest_mac, dest_ip)
        
        # Now enable verbose mode for the receiving part
        osi_stack.verbose = True
        
        # Show only the receiving data flow
        print("\n========== RECEIVING DATA (UP THE STACK) ==========\n")
        response = osi_stack.receive_data(binary_data)
        
        print("\n=================================================")
        print("                 FINAL RESPONSE                   ")
        print("=================================================")
        print(json.dumps(response, indent=2))
        
    except Exception as e:
        print(f"\nError during demonstration: {str(e)}")