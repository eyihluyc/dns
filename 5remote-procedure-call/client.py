"""
Lab 5, Distributed & Network Programming
Client-server application with RPC

Client side
"""

import xmlrpc.client
import sys, os


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError("Usage example: python ./client.py <ip> <port>")
    ip = sys.argv[1]
    port = int(sys.argv[2])

    s = xmlrpc.client.ServerProxy(f"http://{ip}:{port}")

    while True:
        cmd = input("\nEnter the command:").split()
        res = (False, "Not implemented")
        try:
            if cmd[0] == "quit":
                break
            elif cmd[0] == "send":
                if not os.path.exists(f"client_files/{cmd[1]}"):
                    res = (False, "No such file")
                else:
                    with open(f"client_files/{cmd[1]}", "r") as file:
                        res = s.send(cmd[1], file.read())
            elif cmd[0] == "list":
                res = (True, )
                for file in s.list():
                    print(file)
            elif cmd[0] == "delete":
                res = s.delete(cmd[1])
            elif cmd[0] == "get":
                if os.path.exists(f"client_files/{cmd[-1]}"):
                    res = (False, "File already exists")
                else:
                    with open(f"client_files/{cmd[-1]}", "x") as file:
                        res = s.get(cmd[1])
                        if res[0]:
                            file.write(res[1])
            elif cmd[0] == "calc":
                res = s.calc(cmd[1], cmd[2], cmd[3])
                if res[0]:
                    print(res[1])
        except IndexError:
            res = (False, "Error in number of arguments")
        except Exception:  #Supposed to be KeyboardInterrupt, but Windows & Pycharm somehow don't allow me to handle it in a good way...
            break

        if res[0]:
            print("Completed")
        else:
            print("Not completed")
            print(res[1])

    print("Client is stopping")
    sys.exit()
