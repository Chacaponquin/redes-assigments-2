from socket import *
import ssl
import base64

msg = "\r\nI love computer networks!"
end_msg = "\r\n.\r\n"

MAIL_SERVER = 'smtp.gmail.com'
PORT = 587

username = 'hectorangel2001@gmail.com'
password = 'hwej jpou qiwi qwsf '
recept_user = 'chacaponquin@gmail.com'

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((MAIL_SERVER, PORT))
recv = client_socket.recv(1024).decode()
print(recv)

if recv[:3] != '220':
    print('220 reply not received from server.')

ehlo_command = 'EHLO Alice\r\n'
client_socket.send(ehlo_command.encode())
recv_ehlo = client_socket.recv(1024).decode()
print(recv_ehlo)

if recv_ehlo[:3] != '250':
    print('250 reply not received after EHLO command.')

# Send STARTTLS
starttlsCommand = 'STARTTLS\r\n'
client_socket.send(starttlsCommand.encode())
recv_starttls = client_socket.recv(1024).decode()
print(recv_starttls)

if recv_starttls[:3] != '220':
    print('220 reply not received after STARTTLS command.')

# Create an SSL
context = ssl.create_default_context()
client_socket = context.wrap_socket(client_socket, server_hostname=MAIL_SERVER)

# Send EHLO
ehlo_command = 'EHLO Alice\r\n'
client_socket.send(ehlo_command.encode())
recv_ehlo_tls = client_socket.recv(1024).decode()
print(recv_ehlo_tls)

if recv_ehlo_tls[:3] != '250':
    print('250 reply not received after EHLO command (TLS).')

# Authenticate
auth_command = 'AUTH LOGIN\r\n'
client_socket.send(auth_command.encode())
recv_auth = client_socket.recv(1024).decode()
print(recv_auth)

if recv_auth[:3] != '334':
    print('334 reply not received after AUTH LOGIN command.')

client_socket.send(base64.b64encode(username.encode()) + b'\r\n')
recv_username = client_socket.recv(1024).decode()
print(recv_username)

if recv_username[:3] != '334':
    print('334 reply not received after sending username.')

client_socket.send(base64.b64encode(password.encode()) + b'\r\n')
recv_password = client_socket.recv(1024).decode()
print(recv_password)

if recv_password[:3] != '235':
    print('235 reply not received after sending password. Authentication failed.')


# Send MAIL FROM
mailFromCommand = 'MAIL FROM: <' + username + '>\r\n'
client_socket.send(mailFromCommand.encode())
recv2 = client_socket.recv(1024).decode()
print(recv2)

if recv2[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO
rcpt_to_command = 'RCPT TO: <' + recept_user + '>\r\n'
client_socket.send(rcpt_to_command.encode())
recv3 = client_socket.recv(1024).decode()
print(recv3)

if recv3[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.
data_command = 'DATA\r\n'
client_socket.send(data_command.encode())
recv4 = client_socket.recv(1024).decode()
print(recv4)

if recv4[:3] != '354':
    print('354 reply not received from server.')

# Send message data.
client_socket.send(msg.encode())

client_socket.send(end_msg.encode())
recv5 = client_socket.recv(1024).decode()
print(recv5)

if recv5[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT
quit_command = 'QUIT\r\n'
client_socket.send(quit_command.encode())
recv6 = client_socket.recv(1024).decode()
print(recv6)

if recv6[:3] != '221':
    print('221 reply not received from server.')

client_socket.close()
