import asyncio
from asyncio import transports
from typing import Optional  # hz


userlist = []   # temporary list connected users

what_is_new = []

class ClientProtocol(asyncio.Protocol):
    login: str
    server: 'Server'    # Server - class
    transport: transports.Transport

    def __init__(self, server: 'Server'):
        self.server = server
        self.login = None

    def send_history(self):
        for stroke in what_is_new:
            self.transport.write(stroke)

    def data_received(self, data: bytes):
        decoded = data.decode()
        print(decoded)

        if self.login is None:
            # login:User
            """
            Check if existed name from userlist. 
            """
            if decoded.startswith("login:"):
                prelogin = decoded.replace("login:", "").replace("\r\n", "")    # get login for checking in userlist
                if prelogin not in userlist:
                    self.login = decoded.replace("login:", "").replace("\r\n", "")
                    userlist.append(self.login)
                    print("Login write", self.login)
                    self.transport.write(
                        f"Hello, {self.login}!".encode()
                    )
                    self.send_history()
                    #for stroke in what_is_new:
                    #    self.transport.write(stroke)
                else:
                    print("User already exist! Please try again")
                    self.transport.write(
                        f"Hello,the user with login '{prelogin}' already exists!\nPlease try another name".encode()
                    )
                    # Don't andestend HOW DISCONNECT CLIENT FROM SERVER SIDE?

        else:

            self.send_message(decoded)
            # check users list
            #for client in self.server.clients:
            #    print(client.login)


    def send_message(self, message):
        print("USERLIST", userlist)
        format_string = f"{self.login}> {message}"
        encoded = format_string.encode()

        for client in self.server.clients:
            if client.login != self.login:
                client.transport.write(encoded)

        # Last 10 messages
        number_of_mesages = len(what_is_new)
        format_string = f"||{self.login}> {message}\n"
        encoded = format_string.encode()
        if number_of_mesages < 10:
            what_is_new.append(encoded)
        else:
            what_is_new.remove(what_is_new[0])
            what_is_new.append(encoded)

    def connection_made(self, transport: transports.Transport):
        self.transport = transport
        self.server.clients.append(self)  # append to list
        print("Connection made")

    def connection_lost(self, exception):
        self.server.clients.remove(self)
        userlist.remove(self.login)
        print("Disconnected")


class Server:
    clients: list

    def __init__(self):
        self.clients =[]

    def create_protocol(self):
        return ClientProtocol(self)

    async def start(self):
        loop = asyncio.get_running_loop()

        coroutine = await loop.create_server(
            self.create_protocol,
            "127.0.0.1",
            8888
        )

        print("Server started.")
        await coroutine.serve_forever()


process = Server()
try:
    asyncio.run(process.start())
except KeyboardInterrupt:
    print("Disconnected manualy")
