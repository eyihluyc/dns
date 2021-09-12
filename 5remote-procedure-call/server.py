"""
Lab 5, Distributed & Network Programming
Client-server application with RPC

Server side
"""
import re
import sys, os
from xmlrpc.server import SimpleXMLRPCServer
import operator


def send_file(filename, data):
    try:
        with open(f"server_files/{filename}", "x") as file:
            file.write(data)
            print(f"{filename} saved")
            return (True, )
    except FileExistsError:
        print(f"{filename} not saved")
        return (False, "File already exists")
    except Exception as e:
        return (False, e.__str__())


def list_files():
    return os.listdir("server_files")


def delete_file(filename):
    try:
        if os.path.exists(f"server_files/{filename}"):
            os.remove(f"server_files/{filename}")
            print(f"{filename} deleted")
            return (True, )
        else:
            print(f"{filename} not deleted")
            return (False, "No such file")
    except Exception as e:
        return (False, e.__str__())


def get_file(filename):
    try:
        if os.path.exists(f"server_files/{filename}"):
            file = open(f"server_files/{filename}", "r")
            print(f"File sent: {filename}")
            return (True, file.read())
        else:
            print(f"No such file: {filename}")
            return (False, f"No such file")
    except Exception as e:
        return (False, e.__str__())

def calculate(operation, left, right):
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '>': operator.gt,
        ">=": operator.ge,
        '<': operator.lt,
        "<=": operator.le
    }
    try:
        if operation in ops and bool(re.fullmatch("-?[0-9]+", left)) and bool(re.fullmatch("-?[0-9]+", right)):
            cast = int
        elif operation in ops and bool(re.fullmatch("-?[0-9]+(.[0-9]*)?", left)) and bool(re.fullmatch("-?[0-9]+(.[0-9]*)?", right)):
            cast = float
        else:
            print(f"{operation} {left} {right} -- not done")
            return (False, "Wrong expression")

        left = cast(left)
        right = cast(right)

        print(f"{operation} {left} {right} -- done")
        return (True, ops[operation](left, right))
    except Exception as e:
        return (False, e.__str__())


if __name__ == '__main__':
    try:
        if len(sys.argv) != 3:
            raise ValueError("Usage example: python ./server.py <ip> <port>")
        ip = sys.argv[1]
        port = int(sys.argv[2])

        with SimpleXMLRPCServer((ip, port)) as server:
            server.register_introspection_functions()
            server.register_function(send_file, "send")
            server.register_function(list_files, "list")
            server.register_function(delete_file, "delete")
            server.register_function(get_file, "get")
            server.register_function(calculate, "calc")
            server.serve_forever()
    except KeyboardInterrupt:
        print("Server is stopping")
        sys.exit()
