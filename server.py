import socket
import threading

HOST = '192.168.1.3'
PORT = 5555

ready_players = 0
lock = threading.Lock()

def handle_client(conn, addr):
    global ready_players
    print(f"Connection from {addr}")
    with conn:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            # print(f"Received: {data}")
            if data == 'check_ready_count':
                with lock:
                    response = str(ready_players)
                conn.sendall(response.encode())
            else:
                with lock:
                    ready_players += 1
                conn.sendall(data.encode())
            print(data)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server is listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
