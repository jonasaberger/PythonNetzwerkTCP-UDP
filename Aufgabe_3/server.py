import socket
import struct
import threading

# Server-Konfiguration
SERVER_IP = "0.0.0.0"  # alle Interfaces
SERVER_PORT = 5005     # TCP-Port
NUM_VALUES = 5         # Anzahl 32-bit ints pro Paket

def handle_client(client_socket, client_address):
    expected_counter = 1   # nächster erwarteter seq
    received_packets = 0   # Zähler empfangener Pakete
    lost_packets = 0       # Zähler verlorener Pakete
    print(f"[INFO] Verbindung von {client_address} hergestellt")

    try:
        while True:
            # Lese ein Paket (NUM_VALUES * 4 Bytes) — recv kann fragmentieren
            data = client_socket.recv(NUM_VALUES * 4)
            if not data:
                print(f"[INFO] Verbindung von {client_address} beendet")
                break

            # Entpacke little-endian 32-bit signed ints
            values = struct.unpack('<' + 'i' * NUM_VALUES, data)
            seq = values[0]          # erste Integer = Sequenznummer
            received_packets += 1

            # Wenn Lücke in der Sequenz => als verloren zählen
            if seq != expected_counter:
                lost_packets += seq - expected_counter

            expected_counter = seq + 1

            # Alle 1000 Pakete kurze Statistik ausgeben
            if received_packets % 1000 == 0:
                loss_percent = (lost_packets / expected_counter) * 100
                print(f"[{received_packets}] Von {client_address}: seq={seq} |")
                print(f"Verloren={lost_packets} ({loss_percent:.2f}%)")

    except Exception as e:
        print(f"[ERROR] Verbindung von {client_address} unterbrochen: {e}")

    finally:
        client_socket.close()  # Verbindung aufräumen

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)  # max 5 wartende Verbindungen

    print(f"TCP Server lauscht auf {SERVER_IP}:{SERVER_PORT}...")
    while True:
        # Warte auf eingehende Verbindung
        client_sock, client_addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_sock, client_addr))
        client_thread.daemon = True  # Threads mit Hauptprogramm beenden
        client_thread.start()

if __name__ == "__main__":
    main()