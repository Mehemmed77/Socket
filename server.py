import socket
from threading import Thread
from settings import HOST,PORT,BUFFER_SIZE,DISCONNECT_MESSAGE

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

        self.clients_list = []
        self.setup()

    def setup(self):
        result = (HOST,PORT)

        print("------------------- SERVER STARTED ----------------------")
        self.server.bind(result)

        self.server.listen()

        self.welcome()

    def rcv_and_send(self,client: socket.socket,my_username: str):
        data = client.recv(BUFFER_SIZE).decode('utf-8')

        to = ''

        for i in self.clients_list:
            if i[2][0].lower()==data.lower():
                to = i[0]

        if to:
            while True:
                data = client.recv(BUFFER_SIZE).decode('utf-8')

                if data==DISCONNECT_MESSAGE:
                    for i in range(len(self.clients_list)):
                        username = self.clients_list[i][2][0].lower()

                        if username==my_username.lower():
                            self.clients_list.pop(i)
                        
                        data = f'{my_username} DISCONNECTED'
                        print(data)

                        to.send(DISCONNECT_MESSAGE.encode('utf-8'))
                        return

                data = f'{my_username}: {data}'.encode('utf-8')
                to.send(data)
        else:
            return

    def welcome(self):
        while True:
            client,address = self.server.accept()
            msg = client.recv(BUFFER_SIZE).decode('utf-8')
            print(f'{msg}')

            user = client.recv(BUFFER_SIZE).decode('utf-8').split()
            self.clients_list.append([client,address,user])

            print()
            print('+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=')
            for i in self.clients_list:
                print(f'{i[2][0].title()} Is Online.')
            
            print('+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=')  

            a = Thread(target = self.rcv_and_send, args=(client,user[0]))
            a.start()

print('salam')
Server()