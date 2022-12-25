#
# Imports
import sys
import json
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QDialog

# Settings
# Testing
testMode = False


class lanChat(QDialog):

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

        self.contactList = []

        self.contacts()

        # print(self.rect())

    def show_New(self):
        self.name_Box.show()
        self.IP_Box.show()

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
        for i in reversed(range(self.verticalLayout_3.count())):
            self.verticalLayout_3.itemAt(i).widget().setParent(None)

        # add local chat

        g = QGroupBox()
        l = QVBoxLayout()
        g.setTitle('')
        t = QPushButton("Local Chat")
        t.setFlat(True)
        # TODO recent message
        c = QLabel('Recent Message')
        l.addWidget(t)
        l.addWidget(c)
        g.setLayout(l)
        self.verticalLayout_3.addWidget(g)

        for i in load("contacts.json")["logs"]:
            g = QGroupBox()
            l = QVBoxLayout()
            g.setTitle('')
            t = QPushButton(i["name"])
            t.setFlat(True)
            # TODO recent message
            c = QLabel('Recent Message')
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
        # delete old
        try:
            for i in reversed(range(self.verticalLayout_2.count())):
                self.verticalLayout_2.itemAt(i).widget().setParent(None)
        except AttributeError:
            print('Error loading contact: Empty Message Box (non important)')

        # set name
        self.nameBox.setText(contact['name'])


    def getContact(self, contact):
        with open(f'{contact["name"]}.json','w') as l:
            return l["logs"]



    def filedLinesCount(self):

        # TODO
        # Fix this and mak it work like iMesage >:(

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

        if height == lineHight:
            self.message_Box.setFixedHeight(height)
        elif height <= maxHeight and height >= lineHight:
            self.message_Box.setFixedHeight(height)

        # self.message_Box.setFixedHeight(((len(self.message_Box.toPlainText())//100)*55))

        # print(count)

    def connecter(self, func):
        send = self.send_Button
        send.clicked.connect(func)


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


def load(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        # print(data["logs"][0][date][0]["dat"][0]["#data here"])
        stuff = data["logs"]
        return data


# Vars

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
login_scrn = login()
app_scrn = lanChat()
widget.addWidget(login_scrn)
widget.addWidget(app_scrn)

if __name__ == '__main__':
    if len([i for i in load('login.json')["logs"]]) != 0:
        # if there is a username in the json file then goto the app
        widget.setCurrentIndex(widget.currentIndex() + 1)
    widget.show()
    app.exec_()
