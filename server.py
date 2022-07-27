# # import
# import socket
# import threading
#
# # Settings
#
# PORT = 8000
# ADDRESS = "0.0.0.0"
# broadcast_list = []
#
# "Creating the socket object"
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# sock.bind((ADDRESS, PORT))
# "Listening"
# sock.listen()
# client, client_address = sock.accept()
#
# def accept_loop():
#     while True:
#         sock.listen()
#         client, client_address = sock.accept()
#         broadcast_list.append(client)
#         start_listenning_thread(client)
#
# def start_listenning_thread(client):
#     client_thread = threading.Thread(
#             target = listen_thread,
#             args = (client,) #the list of argument for the function
#         )
#     client_thread.start()
#
#
# def listen_thread(client):
#     while True:
#         message = client.recv(1024).decode()
#         if message == "/quit":
#             break
#         print(f"Received message : {message}")
#         broadcast(message)
#
#
# def broadcast(message):
#     for client in broadcast_list:
#         client.send(message.encode())
#
#
# # while True:
# #     message = client.recv(1024) #bytes
# #     if message.decode() == "/quit":
# #         break
# #     print(message.decode())
# #     client.send("\nMessage received !".encode())
# accept_loop()
#
#
#
#
#


# server.py
import socket
import threading

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 8000
ADDRESS = "0.0.0.0"
broadcast_list = []
my_socket.bind((ADDRESS, PORT))


def accept_loop():
    while True:
        my_socket.listen()
        client, client_address = my_socket.accept()
        broadcast_list.append(client)
        start_listenning_thread(client)


def start_listenning_thread(client):
    client_thread = threading.Thread(
        target=listen_thread,
        args=(client,)  # the list of argument for the function
    )
    client_thread.start()


def listen_thread(client):
    while True:
        message = client.recv(1024).decode()
        if message:
            print(f"Received message : {message}")
            broadcast(message)
        else:
            print(f"client has been disconnected : {client}")
            return


def broadcast(message):
    for client in broadcast_list:
        try:
            client.send(message.encode())
        except:
            broadcast_list.remove(client)
            print(f"Client removed : {client}")


accept_loop()
