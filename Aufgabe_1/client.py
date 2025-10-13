import socket
import struct
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 2831
SEND_INTERVAL = 0.001

def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    value = 0

    print("Sende UDP-Pakete an " + UDP_IP + ":" + str(UDP_PORT))
    while True:
        data = struct.pack("!i", value)
        sock.sendto(data, (UDP_IP, UDP_PORT))
        time.sleep(SEND_INTERVAL)

if __name__ == "__main__":
    start_client()