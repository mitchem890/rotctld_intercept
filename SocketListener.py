import socket
import sys

# specify Host and Port
HOST = '127.0.0.1'
ROTCTLRS_KNOWN_PORT = 5789

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.bind((HOST, ROTCTLRS_KNOWN_PORT))

# print if Socket binding operation completed
print('Socket binding operation completed')

# With the help of listening () function
# starts listening
soc.listen()

conn, address = soc.accept()
# print the address of connection
print('Connected with ' + address[0] + ':'
      + str(address[1]))
