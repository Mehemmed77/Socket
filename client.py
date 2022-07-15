import socket
from threading import Thread
from settings import HOST,PORT,BUFFER_SIZE,DISCONNECT_MESSAGE
import time
from sql import insert_or_login_person

class Client:
    def __init__(self):
        self.server = socket.socket()
        self.setup()

    def setup(self):
        result = (HOST,PORT)
        self.server.connect(result)
        self.welcome()

    def get_msg(self):
        while True:
            data = self.server.recv(BUFFER_SIZE).decode('utf-8')

            if data==DISCONNECT_MESSAGE:
                self.server.close()
                return

            print(data)
    
    def send_msg(self):
        data = input('')
        if data==DISCONNECT_MESSAGE:
            self.server.close()
            return

        self.server.send(data.encode('utf-8'))

    def welcome(self):
        name = ''
        password = ''

        while (len(name)<3 or len(password)<8):
            if len(name)>3 and len(password)<8:
                password = input('Your Password: ')

            if len(name)<3 and len(password)>8:
                password = input('Your Name: ')
            
            if len(name)<3 and len(password)<8:
                name = input('Your Name: ')
                password = input('Your Password: ')
                    
        msg = insert_or_login_person(name = name, password = password)

        if type(msg)==tuple:
            self.server.send(msg[0].encode('utf-8'))
            name = msg[1]
        else:
            self.server.send(msg.encode('utf-8'))

        time.sleep(0.3)

        self.server.send(f'{name} {password}'.encode('utf-8'))

        to = input('Who Do You Want To Send Message To: ')

        self.server.send(to.encode('utf-8'))

        print()
        print(f'You Are In A Chat With {to}')
        print()

        get_msg = Thread(target = self.get_msg)
        send_msg = Thread(target = self.send_msg)

        get_msg.start()
        send_msg.start()

Client()