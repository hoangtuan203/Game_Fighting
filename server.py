import socket
import threading

HOST = '192.168.1.3'  # Sử dụng địa chỉ IP công cộng của máy chủ
PORT = 8080
MAX_CLIENTS = 2  # Số lượng kết nối tối đa cho phép

clients = []
ready_count = 0


def check_ready_count():
    return str(ready_count)

def handle_client(client_socket):
    global ready_count
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print("Received:", data)    
            # Xử lý dữ liệu nhận được từ client

            # Kiểm tra nếu client đã sẵn sàng
            print(data)
            if data == "check_ready_count":
                ready_count += 1
                print(ready_count)
                if ready_count == MAX_CLIENTS:
                    # Gửi sự kiện USEREVENT cho tất cả client để thông báo đã đủ người chơi
                    for client in clients:
                        client.sendall(b"check_ready_count")
                    print("Both players are ready, starting the game...")
    except Exception as e:
        print("Error:", e)
    finally:
        client_socket.close()

def start_server():
    global ready_count
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(MAX_CLIENTS)
        print(f"Server is listening on {HOST}:{PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            clients.append(client_socket)

            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()

            if len(clients) == MAX_CLIENTS:
                ready_count = 0  # Reset biến ready_count để chuẩn bị cho trò chơi mới

    except Exception as e:
        print("Error:", e)
    finally:
        server_socket.close()



if __name__ == "__main__":
    start_server()
