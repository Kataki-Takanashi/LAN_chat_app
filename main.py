# client.py
import socket
import sys
import threading
import os
import logging
import time


# Logging

die = False
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
while True:
    try:
        import server
        sever = server.Server()
        break
    except OSError as e:
        log.error(e)

sever = server.Server()
nickname = input("Choose your nickname : ").strip()
while not nickname:
    nickname = input("Your nickname should not be empty : ").strip()

# Initializing Socket
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Gets Servers
devices = []
print("Looking for open server. . .")
for devise in os.popen('arp -a'):
    devices.append(devise.split()[1].strip("()"))  # .strip("()"))

# Filter

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
        #devices.remove(i)
devices = priority #+ devices

# Checks Connectivity
connectable_device = 'null' # Placeholder

make_server = True
host = "192.168.4.24"  # "127.0.1.1"
port = 8000
itterDevice = 0

for device in devices:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        s.connect((device, port))
        make_server = False
        connectable_device = device
        break
    except socket.error as error:
        log.error(f'{error} on {device}')


# Connects to a Server
if make_server:
    print("No open server detected")
    print("Starting server")
    start_server = threading.Thread(target=sever.accept_loop)
    start_server.start()
    time.sleep(1)
    my_socket.connect((socket.gethostbyname(socket.gethostname()), port))
    print(f"Connected to {socket.gethostbyname(socket.gethostname())}")
    #print(f"Connected to {host}")
else:
    my_socket.connect((connectable_device, port))
    print(f"Connected to {connectable_device}")


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
