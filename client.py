# Client Program.

import socket
import tkinter as tk
from tkinter import scrolledtext
import threading

SERVER = "127.0.0.1"  
HEADER = 64
PORT = 5128
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "bye"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect(ADDR)
except Exception as e:
    print(f"Connection error: {e}")
    exit()

def send_message(event = None):
    message = message_entry.get()
    if message:
        username = "Poornasree"
        formatted_message = f"{username}: {message}"
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, formatted_message + "\n")
        chat_display.config(state=tk.DISABLED)
        message_entry.delete(0, tk.END)
        message = formatted_message.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length)) 
        try:
            client_socket.send(send_length)
            client_socket.send(message)
            if formatted_message == f"{username}: {DISCONNECT_MESSAGE}":
                client_socket.close()
                window.quit()
        except Exception as e:
            print(f"Error sending message: {e}")

def receive_messages():
    while True:
        try:
            msg_length = client_socket.recv(HEADER).decode(FORMAT).strip()
            if msg_length:
                msg_length = int(msg_length)
                msg = client_socket.recv(msg_length).decode(FORMAT)
                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, msg + "\n")
                chat_display.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Connection error or disconnection: {e}")
            break

def start_receiving():
    thread = threading.Thread(target=receive_messages)
    thread.daemon = True
    thread.start()

window = tk.Tk()
window.title("Chat Client")

chat_display = scrolledtext.ScrolledText(window, state=tk.DISABLED, width=50, height=20, wrap=tk.WORD)
chat_display.grid(row=0, column=0, padx=10, pady=10)

message_entry = tk.Entry(window, width=40)
message_entry.grid(row=1, column=0, padx=10, pady=10)

send_button = tk.Button(window, text="Send", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

window.bind('<Return>', send_message)

start_receiving()

window.mainloop()
