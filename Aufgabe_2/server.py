import socket
import struct

SERVER_IP = "0.0.0.0"
SERVER_PORT = 5005
NUM_VALUES = 5

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))

expected_counter = 1
received_packets = 0
lost_packets = 0

print(f"UDP Server V2 lauscht auf {SERVER_IP}:{SERVER_PORT}")

while True:
    data, addr = sock.recvfrom(1024)
    values = struct.unpack('<' + 'i' * NUM_VALUES, data)
    seq = values[0]
    received_packets += 1

    if seq != expected_counter:
        lost_packets += seq - expected_counter

    expected_counter = seq + 1

    if received_packets % 1000 == 0:
        loss_percent = (lost_packets / expected_counter) * 100
        print(f"[{received_packets}] Von {addr}: seq={seq} | "
              f"Verloren={lost_packets} ({loss_percent:.2f}%)")
