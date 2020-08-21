import socket

s = socket.socket()

print('Socket created')
s.bind(('localhost',9999))

s.listen(1)

print('Waiting for connection...')

try:
    while(True):
        c, addr = s.accept()
        data = c.recv(1024)
        print('Connected with', addr,data)
        c.send('Hi, I can send this: [1,2,3] and these symbols as well: !@#$%^&*()?><}{[]";:" /n \n Did you know that I can add a new line as well?')
        c.close()
finally:
    s.close()

        
