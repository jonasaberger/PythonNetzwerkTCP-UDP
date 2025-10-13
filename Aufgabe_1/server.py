import socket
import struct

UDP_IP = "0.0.0.0"
UDP_PORT = 2831
BUFFER_SIZE = 1024

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print(f"Server gestartet mit Port {UDP_PORT}")

    packet_count = 0

    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        packet_count += 1

        value = struct.unpack("!i", data)[0]

        if packet_count % 1000 == 0:
            print(f"{packet_count} ~ {addr} empfangen: {value}")

if __name__ == "__main__":
    start_server()