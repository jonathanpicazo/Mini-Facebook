# server.py, Part 2

import socket
import sys
from thread import *
import time

'''
Function Definition
'''
def tupleToString(t):
	s=""
	for item in t:
		s = s + str(item) + "<>"
	return s[:-2]

def stringToTuple(s):
	t = s.split("<>")
	return t

def findUser(search ,myList):
	for i in range(0, len(myList)):
		if myList[i][0] == search:
			return i
	return -1

def getMessages(user, myList):
	retString = ''
	size = len(myList[user])
	for i in range(0, size):
		retString += myList[user][i]
	return retString
'''
Create Socket
'''
HOST = 'localhost'
#HOST = ''	# Symbolic name meaning all available interfaces
PORT = 9486	# Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'

'''
Bind socket to local host and port
'''
try:
	s.bind((HOST, PORT))
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
print 'Socket bind complete'

'''
Start listening on socket
'''
s.listen(10)
print 'Socket now listening'


clients = []
userpass = [["user1", "passwd1"], ["user2", "passwd2"], ["user3", "passwd3"]]
messages = [[],[],[]]
subscriptions = [[],[],[]] # Store the group info

def clientthread(conn):
	global clients
	global count
    global messages
    global userpass

	uppair = conn.recv(1024)
	uppair = stringToTuple(uppair)
	if uppair in userpass:
		user = userpass.index(uppair)
		
		'''
		Part-2:TODO: 
		After the user logs in, check the unread message for this user.
		Return the number of unread messages to this user.
		'''

		while True:
			try :
				option = conn.recv(1024)
			except:
				break
			if option == str(1):
				# Logout that you implemented in Part-1
                user = ''
				break;
			elif option == str(2):
				message = conn.recv(1024)
				if message == str(1):
					'''
					Part-2:TODO: Send private message
					'''
              
				if message == str(2):
					'''
					Part-2:TODO: Send broadcast message
					'''
				if message == str(3):
					'''
					Part-2:TODO: Send group message
					'''
			elif option == str(3):
				'''
				Part-2:TODO: Join/Quit group
				'''
			elif option == str(4):
				'''
				Part-2:TODO: Read offline message
				'''
			else:
				try :
					conn.sendall('Option not valid')
				except socket.error:
					print 'option not valid Send failed'
					conn.close()
					clients.remove(conn)
	else:
		try :
			conn.sendall('nalid')
		except socket.error:
			print 'nalid Send failed'
	print 'Logged out'
	conn.close()
	if conn in clients:
		clients.remove(conn)

def receiveClients(s):
	# Use the code in Part-1, do some modification if necessary

start_new_thread(receiveClients ,(s,))
while 1:
	message = raw_input()
	if message == 'messagecount':
		print 'Since the server was opened ' + str(count) + ' messages have been sent'
	elif message == 'usercount':
		print 'There are ' + str(len(clients)) + ' current users connected'
	elif message == 'storedcount':
		print 'There are ' + str(sum(len(m) for m in messages)) + ' unread messages by users'
	elif message == 'newuser':
		user = raw_input('User:\n')
		password = raw_input('Password:')
		userpass.append([user, password])
		messages.append([])
		subscriptions.append([])
		print 'User created'
	elif message == 'listgroup':
		'''
		Part-2:TODO: Implement the functionality to list all the available groups
		'''
s.close()