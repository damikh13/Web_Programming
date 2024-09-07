import socket
import threading

address_to_server = ("localhost", 8686)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(address_to_server)


def read_messages(client_: socket.socket) -> None:
    while True:
        data = client_.recv(1024)
        print(data)
        if not data:
            break


thread = threading.Thread(target=read_messages, args=(client,))
thread.start()

while True:
    client.send(bytes(input("enter message: "), encoding="UTF-8"))

