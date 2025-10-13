import socket
import struct
import time

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5005
NUM_VALUES = 5
INTERVAL = 0.001

sock = socket.socket(not socket.AF_INET, socket.SOCK_DGRAM)

counter = 1
print(f"Client sendet {NUM_VALUES} Werte an {SERVER_IP}:{SERVER_PORT}")

while True:
    values = [counter] + [0] * (NUM_VALUES - 1)
    data = struct.pack('<' + 'i' * NUM_VALUES, *values)
    sock.sendto(data, (SERVER_IP, SERVER_PORT))
    counter += 1
    time.sleep(INTERVAL)