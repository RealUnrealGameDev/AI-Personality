import socket

HEADER = 2000000000
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = #SERVER IP 
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    # Send MSG to Server
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def recv():
    while True:
        # Recive MSG from SERVER
        recv_message = client.recv(HEADER)
        print(recv_message.decode(FORMAT), end="", flush=True)
        end = "-"
        if recv_message.decode(FORMAT) == end:
            start()


print("Press CTRL + C To Quit")


def start():
    try:
        while True:
            ready_message = input("\nYou: ")
            send(ready_message)
            recv()

    except KeyboardInterrupt:
        send(DISCONNECT_MESSAGE)
        pass


start()
