# py_server_client-msg
quick start

How to disconnect client from server side, after deside existed login name? 

                else:
                    print("User already exist! Please try again")
                    self.transport.write(
                        f"Hello,the user with login '{prelogin}' already exists!\nPlease try another name".encode()
                    )
                    # Don't andestend HOW DISCONNECT CLIENT FROM SERVER SIDE?
