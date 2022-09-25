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
import sys
import threading
import logging

# Logging

log = logging.getLogger(__name__)
stream = logging.StreamHandler()
file = logging.FileHandler('server.log')
stream.setLevel(logging.WARNING)
file.setLevel(logging.ERROR)
formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
stream.setFormatter(formater)
file.setFormatter(formater)
log.addHandler(stream)
log.addHandler(file)


class Server():
    def __init__(self):

        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.PORT = 8000
        self.ADDRESS = "0.0.0.0"
        self.broadcast_list = []
        while True:
            try:
                self.my_socket.bind((self.ADDRESS, self.PORT))
            except OSError as e:
                log.error(e)
        self.die = False


    def accept_loop(self):
        while True:
            if self.die:
                break
            self.my_socket.listen()
            self.client, self.client_address = self.my_socket.accept()
            self.broadcast_list.append(self.client)
            self.start_listenning_thread(self.client)

    def start_listenning_thread(self, client):
        self.client_thread = threading.Thread(
            target=self.listen_thread,
            args=(client,),   # the list of argument for the function
            daemon=True
        )

        self.client_thread.start()

    def listen_thread(self, client):
        while True:
            if self.die:
                self.close()
            message = client.recv(1024).decode()
            if message:
                log.info(f"Received message : {message}")
                self.broadcast(message)
            else:
                log.warning(f"client has been disconnected : {client}")
                return

    def broadcast(self, message):
        for client in self.broadcast_list:
            try:
                client.send(message.encode())
            except:
                self.broadcast_list.remove(client)
                log.info(f"Client removed : {client}")

    def close(self):
        #self.client_thread.join()
        self.die = True
        #sys.exit()


# accept_loop()
