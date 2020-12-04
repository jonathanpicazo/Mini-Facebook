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
# returns user index of array of arrays
def findUser(search ,myList):
	for i in range(0, len(myList)):
		if myList[i][0] == search:
			return i
	return -1

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
groups = ['group1', 'group2', 'group3']
subscriptions = [[],[],[]] # Store the group info (users in group)
online = []
unreadCount = [0,0,0]
# group1, group2, group3

def clientThread(conn):
	global clients
	global count
	global messages
	global userpass
	global groups
	global subscriptions
	global online
	global unreadCount
	uppair = conn.recv(1024)
	uppair = stringToTuple(uppair)
	username = ''
	if uppair in userpass:
		user = userpass.index(uppair)
		username = userpass[user][0]
		online.append(username)

		try:
			conn.sendall('valid')
		except socket.error:
			print 'Send failed'
			sys.exit()
		
		'''
		Part-2:TODO: 
		After the user logs in, check the unread message for this user.
		Return the number of unread messages to this user.
		'''
		# Send messages to user here so it doesnt mess up buffer
		try:
			# conn.sendall(str(len(messages[user])))
			a = str(unreadCount[user])
			conn.sendall(a)
		except socket.error:
			print 'Send failed'
			sys.exit()
		pr = ''
		for i in range(0, len(messages[user])):
			pr += tupleToString(messages[user][i]) + ':'

		if len(messages[user]) != 0:
			try:
				conn.sendall(pr)
			except socket.error:
				print 'Send failed'
				sys.exit()		

		while True:
			try :
				option = conn.recv(1024)
			except:
				break
			if option == str(1):
				# Logout that you implemented in Part-1
				break;
			elif option == str(2):
				message = conn.recv(1024)
				if message == str(1):
					'''
					Part-2:TODO: Send private message
					'''
					pmsg = conn.recv(1024)
					rcv_id = conn.recv(1024)
					addtoMsg = username + '<>' + pmsg
					addtoMsg = stringToTuple(addtoMsg)
					# find index of the recipient
					recptID = findUser(rcv_id, userpass)
					if recptID == -1:
						# invalid id
						break
					# add to their message list
					messages[recptID].append(addtoMsg)
					print 'To: ' + userpass[recptID][0]
					print addtoMsg
					unreadCount[recptID] += 1
					
				if message == str(2):
					'''
					Part-2:TODO: Send broadcast message
					'''
					bmsg = conn.recv(1024)
					print 'Sending broadcast msg, ' + bmsg
					addtoMsg = 'broadcast' + '<>' + bmsg
					addtoMsg = stringToTuple(addtoMsg)

					# for i in range(0, len(messages)):
					# 	messages[i].append(addtoMsg)
					# 	print 'Sent to ' + userpass[i][0]
					for i in range(0, len(online)):
						uid = findUser(online[i], userpass)
						messages[uid].append(addtoMsg)
						unreadCount[uid] += 1
						print 'sent to user with id of ' + str(uid)
				if message == str(3):
					'''
					Part-2:TODO: Send group message
					'''
					gmsg = conn.recv(1024)
					gid = conn.recv(1024)
					addtoMsg = gid + '<>' + gmsg
					addtoMsg = stringToTuple(addtoMsg)
					idx = int(gid[len(gid) - 1]) - 1
					print idx
					for i in range(0, len(subscriptions[idx])):
						toFind = subscriptions[idx][i]
						uid = findUser(toFind, userpass)
						if uid == -1:
							break
						messages[uid].append(addtoMsg)
						unreadCount[uid] += 1
						print 'Sent group msg to ' + toFind


			elif option == str(3):
				'''
				Part-2:TODO: Join/Quit group
				'''
				message = conn.recv(1024)
				#group = conn.recv(1024)
				if message == str(1):
					group = conn.recv(1024)
					for i in range(0,len(groups)):
						if groups[i] == group:
							subscriptions[i].append(username)
							print username + ' joined ' + groups[i]
				if message == str(2):
					group = conn.recv(1024)
					for i in range(0, len(groups)):
						if groups[i] == group:
							subscriptions[i].remove(username)
							print 'Removed ' + username + ' from ' + groups[i]
				if message == str(3):
					print 'list groups'
					# list all groups

			elif option == str(4):
				'''
				Part-2:TODO: Read offline message
				'''
				suboption = conn.recv(1024)
				howmanyread = conn.recv(1024)
				if suboption == str(1):
					unreadCount[user] = 0
				else:
					unreadCount[user] -= int(howmanyread)
					if unreadCount[user] < 0:
						unreadCount[user] = 0
				print 'Option: ' + suboption
				
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
	if username in online:
		online.remove(username)

def receiveClients(s):
	# Use the code in Part-1, do some modification if necessary
	global clients
	while 1:
		# Tips: Wait to accept a new connection (client) - blocking call
		conn, addr = s.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
		clients.append(conn)
		# Tips: start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		start_new_thread(clientThread ,(conn,))
		
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
		for i in range (0, len(groups)):
			print groups[i]
s.close()