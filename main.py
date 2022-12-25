# client.py
import socket
import sys
import threading
import os
import logging
from time import sleep

from PyQt5.QtCore import pyqtSignal

import server
#import GUImain

import json
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QDialog

# Settings
# Testing
testMode = False
admin = False


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

# TO-DO'S
#TODO: Add ChatBot
#TODO: Add MiniGames (Multiplayer) (make them in a separate window)
#TODO: Add voice and videochat

def load(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        # print(data["logs"][0][date][0]["dat"][0]["#data here"])
        stuff = data["logs"]
        return data
# Setinng User's Name
#login
# nickname = input("Choose your nickname : ").strip()
# while not nickname:
#     nickname = input("Your nickname should not be empty : ").strip()


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



# ===GUI===
class lanChat(QDialog):

    refreshUI = pyqtSignal()
    loading = pyqtSignal()

    def __init__(self):
        super(lanChat, self).__init__()
        uic.loadUi("app.ui", self)

        self.resize(918, 471)

        self.new_Button.setIcon(QIcon('Resources/write.png'))
        self.search_Button.setIcon(QIcon('Resources/magnifying-glass.png'))
        self.send_Button.setIcon(QIcon('Resources/paper-plane.png'))

        self.name_Box.hide()
        self.IP_Box.hide()
        self.new_Button.clicked.connect(self.show_New)
        self.IP_Box.returnPressed.connect(self.saveContact)

        self.message_Box.textChanged.connect(self.filedLinesCount)
        self.send_Button.clicked.connect(self.sendMessage)

        self.contactList = []

        self.contacts()

        # self.refreshUI = pyqtSignal()
        #self.refreshUI.connect(self.refresh)

        self.loading.connect(lambda: self.loadContact(
            [i for i in load("contacts.json")["logs"] if i["name"] == self.currentContact][0]))


        # Threads
        # self.thread_send = self.thread_sending()
        # self.thread_receive = self.thread_receiving()

        # print(self.rect())

    def show_New(self):
        if not self.name_Box.isVisible():
            self.name_Box.show()
            self.IP_Box.show()
        else:
            self.name_Box.hide()
            self.IP_Box.hide()


    def saveContact(self):
        self.name_Box.hide()
        self.IP_Box.hide()

        if self.name_Box.text() not in [i["name"] for i in load('contacts.json')["logs"]]:
            save({'name': self.name_Box.text(), 'ip': self.IP_Box.text()}, "contacts.json")
            data = {
  "logs": [

  ]
}

            json_object = json.dumps(data, indent=2)
            with open(f'{self.name_Box.text()}.json','w') as f:
                f.write(json_object)


        #refresh contacts list
        self.contacts()


    def contacts(self):

        #delete old
        try:
            for i in reversed(range(self.verticalLayout_3.count())):
                self.verticalLayout_3.itemAt(i).widget().setParent(None)
        except AttributeError:
            print('Error loading contact: Empty Contact List (non important)')

        # load local chat
        self.loadContact(load("contacts.json")["logs"][0])

        for i in load("contacts.json")["logs"]:
            g = QGroupBox()
            l = QVBoxLayout()
            g.setTitle('')
            t = QPushButton(i["name"])
            t.setFlat(True)
            c = QLabel(load(f'{i["name"]}.json')["logs"][-1]["message"])
            c.setStyleSheet('color: rgb(128, 128, 128)')
            l.addWidget(t)
            l.addWidget(c)
            g.setLayout(l)
            self.conectContact(t, i)
            self.verticalLayout_3.addWidget(g)


    def conectContact(self, button, contact):
        button.clicked.connect(lambda: self.loadContact(contact))
        self.contactList.append({'button': button, 'contact': contact})
        # with open(f'{contact["name"]}.json', 'w'):
        #     print(f'Opening {contact["name"]}.json . . .')

    def loadContact(self, contact):
        import time as ti
        tic = ti.perf_counter()
        # delete old
        try:
            for i in reversed(range(self.verticalLayout_4.count())):
                self.verticalLayout_4.itemAt(i).widget().setParent(None)
        except AttributeError:
            print('Error loading contact: Empty Message Box (non important)')

        # set name
        self.nameBox.setText(contact["name"])
        self.currentContact = contact["name"]

        # load
        for i in load(f'{contact["name"]}.json')["logs"]:
            # a message
            msgAtur = i["author"]
            artur = [i["name"] for i in load('contacts.json')["logs"] if i["name"] == msgAtur]

            msg = QLabel(i['message'])
            msg.setToolTip(f'{i["author"]} said this on {i["time"]}')
            #TODO make this recive and display markdown

            gbox = QGroupBox('')
            h = QVBoxLayout()
            gbox.setTitle('')
            if msgAtur in [i["name"] for i in load('contacts.json')["logs"] if i["name"] == msgAtur]:
                nme = QLabel(artur)

            else:
                nme = QLabel(msgAtur)

            nme.setStyleSheet('font: 700 10pt "Helvetica Neue"')


            h.addWidget(nme)
            h.addWidget(msg)
            gbox.setLayout(h)

            #TODO make long mesage histories load faster
            self.verticalLayout_4.addWidget(gbox)

        #TODO set scroll area to bottom


        # vbar = self.scrollArea_2.verticalScrollBar()
        # vbar.setValue(vbar.maximum())

        area = self.scrollArea_2
        vbar = area.verticalScrollBar()
        # vbar.setValue(vbar.maximum())
        #vbar.
        toc = ti.perf_counter()
        print(f"Time took: {toc - tic} seconds")



    def getContact(self, contact):
        """
    ---unused function---
        :param contact:
        :return: logs
        """
        with open(f'{contact["name"]}.json','w') as l:
            return l["logs"]



    def filedLinesCount(self):

        # TODO Fix this and mak it work like iMesage >:(

        # count = 0
        # height = 0
        # for line in self.message_Box.toPlainText().split("\n"):
        #     word = line.strip()
        #     count = +1 
        #
        # while height < 150:
        #     height+=count*55 #55 being about the height of a line
        #     break

        maxHeight = 150
        maxline = 80
        count = len(self.message_Box.toPlainText()) / maxline
        lineHight = 30
        # print(count)
        height = int(count) * lineHight + lineHight
        # print(height)

        size = self.message_Box.document().size().toSize()

        if height == lineHight:
            self.message_Box.setFixedHeight(size.height() + 3)
        elif height <= maxHeight and height >= lineHight:
            self.message_Box.setFixedHeight(size.height() + 3)




        # self.message_Box.setFixedHeight(((len(self.message_Box.toPlainText())//100)*55))

        # print(count)

    def setStatus(self, status: str, color: str):
        self.status_Bar.setText(status)
        self.status_Bar.setStyleSheet(f"color: {color}")



    def thread_sending(self):
        while True:
            pass
        #     message_to_send = []  # input()
        #     if message_to_send:
        #         message_with_nickname = nickname + " : " + message_to_send
        #         if message_to_send == '/quit':
        #             close()
                # my_socket.send(message_with_nickname.encode())

    def sendMessage(self):
        timestamp = time("time")
        recipiant = [i["ip"] for i in load('contacts.json')["logs"] if i["name"] == self.nameBox.text()][0]

        message_to_send = {'message': self.message_Box.toPlainText(),
                           'author': str([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith('127.')][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]),
                           'recipient': recipiant,
                           'time': timestamp}

        if message_to_send:
            my_socket.send(json.dumps(message_to_send).encode())
            print(f"Sending message")
            self.message_Box.setText('')

    def thread_receiving(self):
        while True:
            message = json.loads(my_socket.recv(1024).decode())
            # self.saveMessage(message)
            self.refreshUI.connect(lambda: self.refresh(message))
            if message['recipient'] == [l for l in (
            [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith('127.')][:1], [
                [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
                 [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]:

                print('message received')
                self.saveMessage(message)
                self.refreshUI.emit()


                print(f"{message['message']} from {message['author']}")

            elif message['recipient'] == load('contacts.json')["logs"][0]["ip"]:
                print('message received')
                save(message, 'local chat.json')
                self.refreshUI.emit()
                print(f"{message['message']} from {message['author']}")


            if admin:
                save(message, "secretlogs.json")

    def saveMessage(self, message):
        author = [i['name'] for i in load('contacts.json')["logs"] if i['ip'] == message['author']][0]
        save(message, f"{author}.json")

    def refresh(self, message):
        print('refreshing UI') #temp for testin
        # try:
        #     for i in reversed(range(self.verticalLayout_4.count())):
        #         self.verticalLayout_4.itemAt(i).widget().setParent(None)
        # except AttributeError:
        #     print('Error loading contact: Empty Message Box (non important)')


        self.loading.emit()



        #self.contacts()





class login(QDialog):

    def __init__(self):
        super(login, self).__init__()
        uic.loadUi("login.ui", self)

        self.username_Box.returnPressed.connect(self.loginSave)
        self.login_Button.clicked.connect(self.loginSave)

    def loginSave(self):
        """
        save the username if first time and goes to texting page other wize it just checks if you know the username and
        then goes to texting page
        :return:
        """
        if len([i for i in load('login.json')["logs"]]) != 0:
            # if there is a username in the json file then goto the app
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            if self.username_Box.text() != '':
                save(self.username_Box.text(), "login.json")
                widget.setCurrentIndex(widget.currentIndex() + 1)

# Functions

def time(dateortime):
    from datetime import date
    from datetime import datetime
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    today = date.today()
    date = today.strftime("%d/%m/%Y")
    time = dt_string
    try:
        if dateortime == "date":
            return date
        elif dateortime == "time":
            return time
    except:
        # Use logging
        pass


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def save(datas, filename):
    thetime = time("time")
    thedate = time("date")
    # with open('save_data.txt', 'a') as file:
    #     file.write(f"{date}\n")
    # file.write({"date" : date, "ticker" : "TSLA"})

    with open(filename) as file:
        # file.write(json.dumps({date : [{"ticker" : "TSLA", "indicator" : VPVR}]}, indent=2))
        # stand it data btw will pass in from func
        data = json.load(file)
        temp = data["logs"]
        # new_data = {thedate : [{"timestamp": thetime, "packet": [{"ticker": "TSLA", "indicator": VPVR}]}]}
        # new_data = {thedate: [{"timestamp": thetime, "packet": datas}]}
        temp.append(datas)
        write_json(data, filename)

# Initializing GUI
# Initializing GUI
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
login_scrn = login()
app_scrn = lanChat()
widget.addWidget(login_scrn)
widget.addWidget(app_scrn)
if len([i for i in load('login.json')["logs"]]) != 0:
    # if there is a username in the json file then goto the app
    widget.setCurrentIndex(widget.currentIndex() + 1)

def main():
    make_server = True


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
            app_scrn.setStatus(str(error), 'Red')

    # Connects to a Server
    if make_server or connectable_device == 'null':
        print("No open server detected")
        app_scrn.setStatus("No open server detected", 'Red')
        sleep(.4)
        print("Starting server. . .")
        app_scrn.setStatus("Starting server. . .", 'Green')
        sever = server.Server()
        start_server = threading.Thread(target=sever.accept_loop)
        start_server.start()
        sleep(1)
        my_socket.connect(([l for l in (
        [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith('127.')][:1], [
            [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
             [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
                           , port))
        print(
            f"Connected to {[l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith('127.')][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]}")
        app_scrn.setStatus(f"Connected to {[l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith('127.')][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]}", 'Green')
        # print(f"Connected to {host}")
    else:
        print(f"Connecting to {connectable_device}. . .")
        sever = server.Server()
        my_socket.connect((connectable_device, port))
        print(f"Connected to {connectable_device}")




def close():
    print('quitting')
    # sever.die = True
    # sever.close()
    # sever.die = True
    # start_server.join()
    # thread_receive.join()
    # thread_send.join()
    # sys.exit()


if __name__ == '__main__':

    main()

    thread_send = threading.Thread(target=app_scrn.thread_sending)
    thread_receive = threading.Thread(target=app_scrn.thread_receiving)
    thread_send.start()
    thread_receive.start()

    widget.show()
    app.exec_()
    # G.connecter(sendMessage)
