import socket
import struct
import time

# Zielserver und Paketkonfiguration
SERVER_IP = '10.10.0.183'   # Server-IP
SERVER_PORT = 5005          # Server-Port
NUM_VALUES = 5              # Anzahl 32-bit ints pro Paket
INTERVAL = 0.001            # Pause zwischen Sends / Sendeintervall 

# TCP Socket erstellen und verbinden
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, SERVER_PORT))

counter = 1
print(f"TCP Client sendet {NUM_VALUES} Werte an {SERVER_IP}:{SERVER_PORT}")

try:
    while True:
        # Paket: erste Zahl = Sequenznummer, restliche Werte = 0
        values = [counter] + [0] * (NUM_VALUES - 1)

        # https://www.geeksforgeeks.org/python/struct-pack-in-python/
        data = struct.pack('<' + 'i' * NUM_VALUES, *values)
        sock.sendall(data)   # sendall stellt sicher dass alle Bytes gesendet werden
        counter += 1
        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("\n[INFO] Verbindung wird beendet")

    
finally:
    sock.close()  # Socket schließen
