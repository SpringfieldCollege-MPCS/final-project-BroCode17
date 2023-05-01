import socket
import threading

from pydub.playback import play

import db
from playsound import playsound
from pydub import AudioSegment

# SONG = AudioSegment.from_mp3('C:\Users\ebene\Desktop\Python\oti.mp3')
HOST = '127.0.0.1'
PORT = 1234
def listen_for_messages_from_server(client):
	while 1:
		msg = client.recv(2048).decode('utf-8')
		if msg != '':
			# username = msg.split("~")[0]
			# content = msg.split("~")[1]
			# print(f"[{username}] {content}")
			print(msg)
			# playsound("oti.mp3")
		else:
			print("Message recevied from client is empty")	

def send_message_to_server(email,client):

	while 1:
		message = input("~: ")
		new_msg = f"{email}:{message}"
		print(new_msg)
		if message != '':
			client.sendall(new_msg.encode())
		else:
			print("Empty msg")
			exit(0)


def communicate_to_server(client,conv_id,email):
	username = f"{email} {str(conv_id)}"
	if username !='':
		client.sendall(username.encode())
	else:
		print("Username cannot be empty")
		exit(0)
	threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()
	send_message_to_server(email, client)


# main function
def start(conv_id,email):
	# Creating a socket object
	# 
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# try except block
	try:
		# Connect to the server
		client.connect((HOST, PORT))
		print("Successfully coonected to server")
		old_messages = db.get_messages(int(conv_id))
		# Run online when clinet connect to the server
		# for msg in old_messages:
		# 	print(f"{msg.from_email}:{msg.sent_date}-> {msg.message_text}")
	except:
		print(f"Unable to connect to server {HOST} {PORT}")
		exit(0)

	communicate_to_server(client,conv_id,email)

# if __name__ == "__main__":
# 	try:
# 		main()
# 	except KeyboardInterrupt:
# 		exit(0)
		