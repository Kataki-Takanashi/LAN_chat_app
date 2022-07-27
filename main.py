# # import
# import socket
# import threading
#
# # Settings
#
# PORT = 8000
# ADDRESS = "localhost" # Same as "127.0.1.1"
#
# "Creating the socket object"
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# "Connecting"
# sock.connect((ADDRESS, PORT))
#
# msg = "msg"
# # while msg != "/quit":
# #     msg = input("Msg: >>> ")
# #     # if msg == "/quit":
# #     #     break
# #     sock.send(msg.encode())
#
# def thread_sending():
#     while True:
#         msg = input("Msg: >>> ")
#         sock.send(msg.encode())
#
#
# def thread_receiving():
#     while True:
#         message = sock.recv(1024).decode()
#         print(message)
#
#
# thread_send = threading.Thread(target=thread_sending)
# thread_receive = threading.Thread(target=thread_receiving)
#
# thread_send.start()
# thread_receive.start()

# client.py
import socket
import threading

nickname = input("Choose your nickname : ").strip()
while not nickname:
    nickname = input("Your nickname should not be empty : ").strip()
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"  # "127.0.1.1"
port = 8000
my_socket.connect((host, port))


def thread_sending():
    while True:
        message_to_send = input()
        if message_to_send:
            message_with_nickname = nickname + " : " + message_to_send
            my_socket.send(message_with_nickname.encode())


def thread_receiving():
    while True:
        message = my_socket.recv(1024).decode()
        print(message)


thread_send = threading.Thread(target=thread_sending)
thread_receive = threading.Thread(target=thread_receiving)
thread_send.start()
thread_receive.start()