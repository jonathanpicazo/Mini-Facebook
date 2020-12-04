import socket
import sys
from thread import *
import getpass
import os
import time

'''
Function Definition
'''
def receiveThread(s):
    while True:
        try:
            reply = s.recv(4096) # receive msg from server
            # You can add operations below once you receive msg
            # from the server

        except:
            print "Connection closed"
            break
    

def tupleToString(t):
	s = ""
	for item in t:
		s = s + str(item) + "<>"
	return s[:-2]

def stringToTuple(s):
	t = s.split("<>")
	return t

'''
Create Socket
'''
try:
	# create an AF_INET, STREAM socket (TCP)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit();
print 'Socket Created'

'''
Resolve Hostname
'''

host = 'localhost'
#host = '10.0.0.4'
port = 9486
try:
	remote_ip = socket.gethostbyname(host)
except socket.gaierror:
	print 'Hostname could not be resolved. Exiting'
	sys.exit()
print 'Ip address of ' + host + ' is ' + remote_ip

'''
Connect to remote server
'''
s.connect((remote_ip , port))
print 'Socket Connected to ' + host + ' on ip ' + remote_ip


messageQueue = []

print 'Enter username: '
username = raw_input()
print 'Enter password: '
passwd = getpass.getpass()
# Send username && passwd to server

s.sendall(username + '<>' + passwd)
#msgBack = s.recv(1024)

# Start of the Skeleton Code
reply = s.recv(5)
if reply == 'valid':
    print 'Username and password valid'
    ss = s.recv(1)
    print 'You have ' + ss + ' unread messages'
    # receive user messages here, does not work past start_new_thread line for some reason :(
    if ss != '0':
        messageBuff = s.recv(4096)
        messList = messageBuff.split(':')
        messList = messList[:-1] # deletes empty array element
        for i in range(0, len(messList)):
            newList = messList[i].split('<>') # splits string into sender and message
            toAdd = newList[0] + ': ' + newList[1]
            messageQueue.append(toAdd)
        

    start_new_thread(receiveThread, (s,))
    message = ""
    while True :	
        message = raw_input("Choose an option (type the number): \n 1. Logout \n 2. Send messages \n 3. Group Configuration \n 4. Offline message \n")		
        try :
            s.sendall(message)
            if message == str(1):
                break
            if message == str(2):
                while True:
                    message2 = raw_input("Choose an option (type the number): \n 1. Private messages \n 2. Broadcast messages \n 3. Group messages \n")
                    try:
                        s.sendall(message2)
                        if message2 == str(1):
                            pmsg = raw_input("Enter your private message\n")
                            try:
                                # send private message
                                s.sendall(pmsg)
                            except socket.error:
                                print 'Private Message Send failed'
                                sys.exit()
                            rcv_id = raw_input("Enter the recevier ID:\n")
                            try :
                                # send recipient id
                                s.sendall(rcv_id)
                                break
                            except socket.error:
                                print 'rcv_id Send failed'
                                sys.exit()
                        if message2 == str(2):
                            bmsg = raw_input("Enter your broadcast message\n")
                            try :
                                '''
                                Part-2:TODO: Send broadcast message
                                '''
                                s.sendall(bmsg)
                                break
                            except socket.error:
                                print 'Broadcast Message Send failed'
                                sys.exit()
                        if message2 == str(3):
                            gmsg = raw_input("Enter your group message\n")
                            try :
                                '''
                                Part-2:TODO: Send group message
                                '''
                                s.sendall(gmsg)
                            except socket.error:
                                print 'Group Message Send failed'
                                sys.exit()
                            g_id = raw_input("Enter the Group ID:\n")
                            try :
                                '''
                                Part-2:TODO: Send group message
                                '''
                                s.sendall(g_id)
                                break
                            except socket.error:
                                print 'g_id Send failed'
                                sys.exit()
                    except socket.error:
                        print 'Message Send failed'
                        sys.exit() 
                    
            if message == str(3):
                option = raw_input("Do you want to: 1. Join Group 2. Quit Group 3. List Groups: \n")
                s.sendall(option)
                if option == str(1):
                    group = raw_input("Enter the Group you want to join: ")
                    try :
                        '''
                        Part-2:TODO: Join a particular group
                        '''
                        s.sendall(group)
                    except socket.error:
                        print 'group info sent failed'
                        sys.exit()
                elif option == str(2):
                    group = raw_input("Enter the Group you want to quit: ")
                    try :
                        '''
                        Part-2:TODO: Quit a particular group
                        '''
                        s.sendall(group)
                    except socket.error:
                        print 'group info sent failed'
                        sys.exit()
                elif option == str(3):
                    print 'Here are the available groups: '
                    print 'group1'
                    print 'group2'
                    print 'group3'
                else:
                    print 'Option not valid'
            
            if message == str(4):
                while not os.getpgrp() == os.tcgetpgrp(sys.stdout.fileno()):
                    pass
                option = raw_input("Do you want to: 1. View all offline messages; 2. View only from a particular Group\n")
                isread = 0
                s.sendall(option)
                if option == str(1):					
                    try :
                        '''
                        Part-2:TODO: View all offline messages
                        '''
                        for i in range(0, len(messageQueue)):
                            isread += 1
                            print messageQueue[i]
                        s.sendall(str(isread))
                    except socket.error:
                        print 'msg Send failed'
                        sys.exit()
                elif option == str(2):
                    group = raw_input("Enter the group you want to view the messages from: ")
                    try :
                        for i in range(0, len(messageQueue)):
                            if group in messageQueue[i]:
                                isread += 1
                                print messageQueue[i]
                        s.sendall(str(isread))
                    except socket.error:
                        print 'group Send failed'
                        sys.exit()
                        
                else:
                    print 'Option not valid'
        except socket.error:
            print 'Send failed'
            sys.exit()		
else:
    print 'Invalid username or password'

s.close()