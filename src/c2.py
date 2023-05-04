import socket
import threading
from colorama import Fore
import os

HOST = '127.0.0.1'
PORT = 1234

def listen_for_messages_from_server(client):
    while 1:
        msg = client.recv(2048).decode('utf-8')
        if msg != '':
            print(msg)
        else:
            print("Message recevied from client is empty")


def send_message_to_server(email, client):
    while 1:
        message = ""  # set message to null
        while message == "":
            message = input()
            if message != '' and message != "q":
                new_msg = f"{email}:{message}{Fore.RESET}"
                client.sendall(new_msg.encode())
                break;
            elif message == "q":
                break;
            else:
                print("Input can not be empty")
        # Check again if message is equal to "q"
        if message == "q":
            break;


def communicate_to_server(client, conv_id, email):
    username = f"{email} {str(conv_id)}"
    if username != '':
        client.sendall(username.encode())
    else:
        print("Username cannot be empty")
        exit(0)
    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()
    send_message_to_server(email, client)


# main function
def start(conv_id, email):
    # Clear screen
    os.system('cls')
    # Creating a socket object
    #
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # try except block
    try:
        # Connect to the server
        client.connect((HOST, PORT))
        print("Successfully connected to server")
    except:
        print(f"Unable to connect to server {HOST} {PORT}")
        exit(0)

    communicate_to_server(client, conv_id, email)

# if __name__ == "__main__":
# 	try:
# 		main()
# 	except KeyboardInterrupt:
# 		exit(0)
