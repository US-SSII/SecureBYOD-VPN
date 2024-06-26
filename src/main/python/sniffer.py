import pyshark
from datetime import datetime
from loguru import logger


class TrafficCapture:
    """
    Class to manage network traffic capture.
    """

    def __init__(self, interface='lo') -> None:
        """
        Initializes a TrafficCapture object.

        Args:
            interface (str): The network interface to capture traffic from (default is 'lo').
        """
        self.interface = interface
        self.cap = None
        self.capture_running = False
        self.filename = None

    def start_capture(self, ip_src=None, port_src=None, ip_dst=None, port_dst=None, protocol=None) -> None:
        """
        Starts capturing network traffic.

        Args:
            ip_src (str): Source IP address filter.
            port_src (int): Source port filter.
            ip_dst (str): Destination IP address filter.
            port_dst (int): Destination port filter.
            protocol (str): Protocol filter (e.g., 'tcp', 'udp', etc.).
        """
        if self.capture_running:
            logger.info("Capture is already running.")
            return
        try:
            # Constructing the capture filter based on provided parameters
            capture_filter = '(tcp.srcport == 12345) or (tcp.dstport == 12345) and tls'

            # Removing the trailing ' and ' if it exists
            if capture_filter.endswith(' and '):
                capture_filter = capture_filter[:-5]

            self.cap = pyshark.LiveCapture(interface=self.interface, display_filter=capture_filter, capture_filter=capture_filter)
            self.capture_running = True
            self.filename = self.generate_filename()
            logger.info(f"Capture started. Saving to '{self.filename}'.")
            self.cap.apply_on_packets(self.packet_callback)
        except Exception as e:
            logger.error(f"Error starting capture: {e}")

    def stop_capture(self):
        """
        Stops capturing network traffic.
        """
        if not self.capture_running:
            logger.info("No capture running to stop.")
            return
        self.capture_running = False
        if self.cap:
            self.cap.close()
            logger.info("Capture stopped.")

    def packet_callback(self, pkt: pyshark.packet.packet.Packet) -> None:
        """
        Callback function to process captured packets.

        Args:
            pkt: Captured packet.
        """
        if self.capture_running:
            try:
                ip_src = pkt.ip.src
                ip_dst = pkt.ip.dst
                port_src = pkt.tcp.srcport
                port_dst = pkt.tcp.dstport
                size = pkt.length
                protocol = pkt.transport_layer

                with open(self.filename, 'a') as f:
                   f.write(f"Source IP: {ip_src}, Destination IP: {ip_dst}, Source Port: {port_src}, Destination Port: {port_dst}, Size: {size}, Info: {protocol}\n")
            except AttributeError as e:
                print(e.with_traceback())

    def generate_filename(self) -> str:
        """
        Generates a filename for saving captured traffic.

        Returns:
            str: The generated filename.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d")
        return f"../_traffic_capture/{timestamp}_traffic_capture.txt"

# Example usage
if __name__ == "__main__":
    capture = TrafficCapture(interface='Adapter for loopback traffic capture')
    capture.start_capture(ip_src='192.168.1.100', port_src=12345, ip_dst='192.168.1.200', port_dst=12345, protocol='tcp')
    input("Press Enter to stop capture...")
    capture.stop_capture()


