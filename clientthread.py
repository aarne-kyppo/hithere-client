# encoding=utf-8
from threading import Thread
import socket
class ClientThread(Thread):
	def __init__(self,mainwindow):
		super(ClientThread,self).__init__()
		self.window = mainwindow
		self.sock = mainwindow.sock
	def run(self):
		try:
			while 1:
				msg = self.sock.recv(1024)
				print msg
				messages = msg[:-1].split(';') #User may get many messages at the same time
				for m in messages:
					#splitting message to type and message
					print m
					tmp = m.split(':')
					type = tmp[0]
					#Operations for different kinds of messages
					if type == 'newusr': #New user notification
						self.window.addUser(tmp[1])
					elif type == 'leftusr': #Informs about left user
						self.window.deleteUser(tmp[1])
					elif type == 'msg': #Message from another client
						self.window.routeMessage(u'{0}'.format(tmp[1]),u'{0}'.format(tmp[2]))
		except socket.error:
			print "Connection is closed"
