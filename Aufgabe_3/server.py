import socket
import struct
import threading

SERVER_IP = "0.0.0.0"
SERVER_PORT = 5005
NUM_VALUES = 5

def handle_client(client_socket, client_address):
    """Thread-Funktion für jeden Client"""
    expected_counter = 1
    received_packets = 0
    lost_packets = 0
    print(f"[INFO] Verbindung von {client_address} hergestellt")

    try:
        while True:
            data = client_socket.recv(NUM_VALUES * 4)  # 4 Bytes pro int
            if not data:
                print(f"[INFO] Verbindung von {client_address} beendet")
                break

            values = struct.unpack('<' + 'i' * NUM_VALUES, data)
            seq = values[0]
            received_packets += 1

            if seq != expected_counter:
                lost_packets += seq - expected_counter

            expected_counter = seq + 1

            if received_packets % 1000 == 0:
                loss_percent = (lost_packets / expected_counter) * 100
                print(f"[{received_packets}] Von {client_address}: seq={seq} | "
                      f"Verloren={lost_packets} ({loss_percent:.2f}%)")

    except Exception as e:
        print(f"[ERROR] Verbindung von {client_address} unterbrochen: {e}")
    finally:
        client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)  # max 5 wartende Verbindungen
    print(f"TCP Server lauscht auf {SERVER_IP}:{SERVER_PORT}")

    while True:
        client_sock, client_addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_sock, client_addr))
        client_thread.daemon = True
        client_thread.start()


if __name__ == "__main__":
    main()