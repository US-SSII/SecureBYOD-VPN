import pyshark
from datetime import datetime

class TrafficCapture:
    def __init__(self, interface='eth0'):
        self.interface = interface
        self.cap = None
        self.capture_running = False
        self.filename = None

    def start_capture(self):
        if self.capture_running:
            print("La captura ya está en marcha.")
            return
        try:
            self.cap = pyshark.LiveCapture(interface=self.interface)
            self.capture_running = True
            self.filename = self.generate_filename()
            print(f"Captura iniciada. Guardando en '{self.filename}'.")
            self.cap.apply_on_packets(self.packet_callback)
        except Exception as e:
            print(f"Error al iniciar la captura: {e}")

    def stop_capture(self):
        if not self.capture_running:
            print("No hay captura en ejecución para detener.")
            return
        self.capture_running = False
        if self.cap:
            self.cap.close()
            print("Captura detenida.")

    def packet_callback(self, pkt):
        if self.capture_running:
            try:
                ip_src = pkt.ip.src
                ip_dst = pkt.ip.dst
                port_src = pkt.tcp.srcport
                port_dst = pkt.tcp.dstport
                size = pkt.length
                info = pkt.sniff_timestamp

                with open(self.filename, 'a') as f:
                    f.write(f"IP Origen: {ip_src}, IP Destino: {ip_dst}, Puerto Origen: {port_src}, Puerto Destino: {port_dst}, Tamaño: {size}, Info: {info}\n")
            except AttributeError:
                pass

    def generate_filename(self):
        timestamp = datetime.now().strftime("%Y-%m-%d")
        return f"../logs/{timestamp}_traffic_capture.txt"

# Ejemplo de uso
if __name__ == "__main__":
    capture = TrafficCapture(interface='Wi-Fi')
    capture.start_capture()  # Iniciar la captura
    input("Presiona Enter para detener la captura...")
    capture.stop_capture()   # Detener la captura
