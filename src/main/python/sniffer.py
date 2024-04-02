import pyshark
from datetime import datetime
from loguru import logger

class TrafficCapture:
    """
    Class to manage network traffic capture.
    """

    def __init__(self, interface='eth0') -> None:
        """
        Initializes a TrafficCapture object.

        Args:
            interface (str): The network interface to capture traffic from (default is 'eth0').
        """
        self.interface = interface
        self.cap = None
        self.capture_running = False
        self.filename = None

    def start_capture(self) -> None:
        """
        Starts capturing network traffic.
        """
        if self.capture_running:
            logger.info("Capture is already running.")
            return
        try:
            self.cap = pyshark.LiveCapture(interface=self.interface)
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
                info = pkt.sniff_timestamp

                with open(self.filename, 'a') as f:
                    f.write(f"Source IP: {ip_src}, Destination IP: {ip_dst}, Source Port: {port_src}, Destination Port: {port_dst}, Size: {size}, Info: {info}\n")
            except AttributeError:
                pass

    def generate_filename(self) -> str:
        """
        Generates a filename for saving captured traffic.

        Returns:
            str: The generated filename.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d")
        return f"../logs/{timestamp}_traffic_capture.txt"

# Example usage
if __name__ == "__main__":
    capture = TrafficCapture(interface='Wi-Fi')
    capture.start_capture()  # Start capture
    input("Press Enter to stop capture...")
    capture.stop_capture()   # Stop capture

