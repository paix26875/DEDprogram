import socket

PORT = 50000
BUFFER_SIZE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('169.254.227.158', PORT))
    data = input('Please input > ')
    s.send(data.encode())
    print(s.recv(BUFFER_SIZE).decode())
