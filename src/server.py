import socket
import threading
import db
import datetime

# Main function
HOST = '127.0.0.1'
PORT = 1234  # You can use any port between 0 to 65535

active_clients = []  # List of all currently connected users

CONVERSATION_ID = -1


# Function to listen for upcoming messages from a cleint
def listen_for_messages(client, id):
    while 1:
        try:
            response = client.recv(2048).decode('utf-8')
        except Exception as e:
            # Cleint no longer connected
            # remove it from the list
            for user in active_clients:
                if user[0] == int(id) and user[1] == client:
                    active_clients.remove(user)
                    break
        else:
            if response != "":
                print(f"this is {response}")
                sent_email = response.split(":")[0]
                content = response.split(":")[1].rstrip()
                now = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
                # first = response.split(":")[0]
                # second= response.split(":")[1]
                # final_msg = first+now+second
                # Persisting data to db
                db.create_message(sent_email, content, now, int(id))
                response = response.replace(":", f":{now}-> ")
                send_message_to_all(id, response, client)
            else:
                print(f"The message sent from client{'username'} is Empty")


# Fucntion to send message to a single client
def send_message_to_single_client(client, message):
    # database
    # print(f"{client}, {message}")
    client.sendall(message.encode())


# Function to send any new message to all the client that
# are currently connected to the server
def send_message_to_all(id, message, sent_client):
    for user in active_clients:
        if user[0] == int(id) and user[1] != sent_client:
            send_message_to_single_client(user[1], message)


# Function to handle client
def client_handler(client):
    # Server will listen for client message that will
    # Contain the user

    while 1:
        username = client.recv(2048).decode('utf-8')
        # print(username)
        email = username.split(' ')[0]
        conv_id = username.split(' ')[1]
        CONVERSATION_ID = conv_id
        # print(f"{email} {conv_id}")
        if email != " " and conv_id != "":
            # datase
            # active_clients.append((username, client))
            active_clients.append((int(conv_id), client))
        prompt_msg = "SERVER~" + f"{email} has added to the chat"
        send_message_to_all(conv_id, prompt_msg, None)
        # Get old messages from db
        old_messages = db.get_messages(int(conv_id))
        # Run online when clinet connect to the server
        for msg in old_messages:
            # send_message_to_all(conv_id, f"{msg.from_email}:{msg.sent_date}-> {msg.message_text}", None)
            send_message_to_single_client(client, f"{msg.from_email}:{msg.sent_date}-> {msg.message_text}")
        # print(f"{msg.from_email}:{msg.sent_date}-> {msg.message_text}")
        break;
    # else:
    # 	print("Client username is Empty")
    threading.Thread(target=listen_for_messages, args=(client, conv_id)).start()


def main():
    # Creating the socket class object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP  packets fro comminucation
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Binding
    # s.bind((socket.gethostname(), 1234))
    try:
        s.bind((HOST, PORT))
        print(f"Running the server of {HOST} {PORT}")
    except:
        print(f"Unable to bind to host{HOST} and port {PORT}")
    # Set server limit
    s.listen(10)
    while 1:
        client, address = s.accept()
        print(client)
        print(f"Connection from {address[0]} {address[1]} has establised!")
        threading.Thread(target=client_handler, args=(client,)).start()
    # clientsocket.send(bytes("Welcome to the server!", "utf-8"))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
