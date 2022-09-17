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
import sys
import threading
import os
import logging
import time

import server
import serverFinder
from tqdm import tqdm

#from test1 import device

# Logging

die = False
logger = logging.getLogger(__name__)
stream = logging.StreamHandler()
file = logging.FileHandler('server.log')
stream.setLevel(logging.WARNING)
file.setLevel(logging.ERROR)
formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
stream.setFormatter(formater)
file.setFormatter(formater)
logger.addHandler(stream)
logger.addHandler(file)

test = serverFinder.test()
sever = server.Server()
nickname = input("Choose your nickname : ").strip()
while not nickname:
    nickname = input("Your nickname should not be empty : ").strip()
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

devices = []
print("Looking for open server. . .")
for devise in os.popen('arp -a'):
    devices.append(devise.split()[1].strip("()"))  # .strip("()"))
# print(devices)
#filter

for i in devices:
    delete = False
    if not i.startswith('192'):
        delete = True
    if i.startswith('224'):
        delete = True
    if delete:
        devices.remove(i)

# Priority
priority = []
for i in devices:
    if i.startswith('192.168.4'):
        priority.append(i)
        devices.remove(i)
devices = priority #+ devices


make_server = True
host = "192.168.4.24"  # "127.0.1.1"1`
port = 8000
itterDevice = 0

result = serverFinder.test.threadTeast(serverFinder.test(), devices)
if result != False:
    my_socket.connect((result, port))
else:
    #logger.info(f"No connection to {device}")
    pass

# def start_search_thread(devices):
#     for i in devices:
#         search_thread = threading.Thread(
#             target=serch_thread,
#             args=(i,),  # the list of argument for the function
#             daemon=True
#         )
#
#         search_thread.start()
#
# connectable_device = 'null' #placeholder
# def serch_thread(device):
#     try:
#         my_socket.connect((device, port))
#         make_server = False
#         connectable_device = device
#         print(f"Connected to {device}")
#         return True
#     except socket.error as error:
#         logger.error(f'{error} on {device}')
#         return False
#     finally:
#         my_socket.close()
#         return
#
#
# start_search_thread(devices)
    # try:
    #     my_socket.connect((device, port))
    #     make_server = False
    #     print(f"Connected to {device}")
    #     break
    # except socket.error as error:
    #     logger.error(f'{error} on {device}')
    #     # print(error)

time.sleep(2.5)
if make_server:
    print("No open server detected")
    print("Starting server")
    start_server = threading.Thread(target=sever.accept_loop)
    # server.accept_loop()
    start_server.start()
    time.sleep(1)
    my_socket.connect((socket.gethostbyname(socket.gethostname()), port))
    #my_socket.connect((host, port))
    print(f"Connected to {socket.gethostbyname(socket.gethostname())}")
    #print(f"Connected to {host}")
else:
    my_socket.connect((connectable_device, port))


def thread_sending():
    while True:
        if sever.die:
            break  # closes thread if the sever.die var is True
        message_to_send = input()
        if message_to_send:
            message_with_nickname = nickname + " : " + message_to_send
            if message_to_send == '/quit':
                close()
            my_socket.send(message_with_nickname.encode())


def thread_receiving():
    while True:
        if sever.die:
            break
        message = my_socket.recv(1024).decode()
        print(message)


def close():
    print('quitting')
    sever.die = True
    sever.close()
    sever.die = True
    # start_server.join()
    # thread_receive.join()
    # thread_send.join()
    # sys.exit()


thread_send = threading.Thread(target=thread_sending)
thread_receive = threading.Thread(target=thread_receiving)
thread_send.start()
thread_receive.start()
