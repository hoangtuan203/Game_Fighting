import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except Exception as e:
            print("Error receiving message:", e)
            break

def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

def main():
    host = '127.0.0.1'  # Địa chỉ IP của máy chủ
    port = 5555  # Cổng kết nối

    # Tạo socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Kết nối đến máy chủ
    try:
        client_socket.connect((host, port))
        print("Connected to server.")
    except Exception as e:
        print("Error connecting to server:", e)
        return

    # Bắt đầu một luồng để nhận tin nhắn từ máy chủ
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Bắt đầu một luồng để gửi tin nhắn đến máy chủ
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

    # Chờ cả hai luồng kết thúc
    receive_thread.join()
    send_thread.join()

    # Đóng kết nối
    client_socket.close()

if __name__ == "__main__":
    main()
