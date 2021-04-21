import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.86', 9999))
message = 'hello fils de pute'
s.send(message.encode("ascii"))
data = s.recv(1024)
s.close()
print(repr(data), 'Reçue')