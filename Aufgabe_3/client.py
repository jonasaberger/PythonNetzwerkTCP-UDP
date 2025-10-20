import socket
import struct
import time

SERVER_IP = '10.10.0.183'
SERVER_PORT = 5005
NUM_VALUES = 5
INTERVAL = 0.001

# TCP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, SERVER_PORT))

counter = 1
print(f"TCP Client sendet {NUM_VALUES} Werte an {SERVER_IP}:{SERVER_PORT}")

try:
    while True:
        values = [counter] + [0] * (NUM_VALUES - 1)
        data = struct.pack('<' + 'i' * NUM_VALUES, *values)
        sock.sendall(data)
        counter += 1
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    print("\n[INFO] Verbindung wird beendet")
finally:
    sock.close()
