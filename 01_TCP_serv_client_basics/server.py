import socket
import threading
from queue import Queue
from typing import Generator

# Задаем адрес сервера
SERVER_ADDRESS = ("localhost", 8686)

server_queue = Queue(10)
# Настраиваем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.listen(10)
print("server is running, please, press ctrl+c to stop")


def wait_connection(
    server_: socket.socket,
) -> Generator[tuple[socket.socket, socket._RetAddress], None, None]:
    while True:
        connection, address = server_socket.accept()
        print("new connection from {address}".format(address=address))
        yield (connection, address)


def wait_message(connection_: socket.socket) -> bytes:
    while True:
        data = connection_.recv(1024)
        if not data:
            break
        yield data


def read_message(connection_: socket.socket, queue: Queue, address) -> None:
    for data in wait_message(connection_):
        print(str(data))
        queue.put((address, data))


def send_from_queue(connection_pul_: list[socket.socket], queue: Queue) -> None:
    while True:
        seneder_address, data = queue.get()
        print("send", data)
        for conn, address in connection_pul_:
            if address != seneder_address:
                res = conn.send(data)
        queue.task_done()


connection_pull = []
thread_write = threading.Thread(
    target=send_from_queue, args=(connection_pull, server_queue)
)
thread_write.start()

for connection, address in wait_connection(server_socket):
    connection_pull.append((connection, address))
    thread_read = threading.Thread(
        target=read_message, args=(connection, server_queue, address)
    )
    thread_read.start()

