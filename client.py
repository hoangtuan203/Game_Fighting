import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '192.168.1.3'
PORT = 1234

def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, 'end')  # Modified this line
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

def receive_messages():
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                username, content = message.split("~")
                add_message(f"[{username}] {content}")
        except ConnectionAbortedError:
            messagebox.showinfo("Disconnected", "Disconnected from the server.")
            break

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert('end', message + '\n')
    message_box.config(state=tk.DISABLED)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

root = tk.Tk()
root.geometry("600x600")
root.title("Messenger Client")

message_textbox = tk.Entry(root, font=("Helvetica", 12))
message_textbox.pack()

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

message_box = scrolledtext.ScrolledText(root, font=("Helvetica", 12), wrap=tk.WORD)
message_box.pack()

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

root.mainloop()