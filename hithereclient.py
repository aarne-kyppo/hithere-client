# encoding=utf-8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from loginwindow import LoginWindow
from messagewindow import MessageWindow
from clientthread import ClientThread
from PyQt4 import QtGui
import socket
import sys
class Client(QtGui.QMainWindow):
	def __init__(self,application, parent = None):
		QtGui.QMainWindow.__init__(self,parent) #Calling for QMainWindows constructor
		
		self.app = application
		
		self.nick = ''
		
		#Making central widget
		self.central = QWidget(self)
		self.setCentralWidget(self.central)
		
		#Creating grid for UI controls
		self.grid = QGridLayout(self.centralWidget())
		self.grid.setSpacing(5)
		
		#Creating controls
		self.contactlist = QListWidget() #This widget shows online users for client
		
		#Adding controls to grid
		self.grid.addWidget(self.contactlist,0,0)
		
		#Listener for contactlist
		self.contactlist.itemDoubleClicked.connect(self.chat)
		
		#Get user login information
		self.loginwindow = LoginWindow(self)
		
		#Modify window and show it
		self.setGeometry(100,100,300,300)
		self.setWindowTitle('HelloThere-Client')
		self.show()
		
		self.msgwindows = []
	def login(self,nick): #This function returns True, if users nickname is accepted. Otherwise it returns False
		if self.sock is None:
			return False
		if nick is '': #Nickname must not be empty. Think about empty nickname in your contact list.
			QMessageBox.about(self,'Empty nickname','Nickname must not be empty')
			return False
		self.sock.sendall(str(nick)) #Sending chosen nickname to be validated
		msg = self.sock.recv(1024) #Return-message, that tells if chosen nickname is valid or not
		print msg
		if msg == 'invalidnick': #Nickname is already chosen.
			QMessageBox.about(self,'Invalid nickname','Nickname is already chosen by another client. Choose another')
			return False
		elif msg == 'nickreserved': #Nickname is not chosen by another client and that why it is reserved for the user.
			return True
	def addUser(self, nick): #Function to add new user to contact list.
		self.contactlist.addItem(u'{0}'.format(nick))
		print u'uusi käyttäjä {0}'.format(nick)
	def deleteUser(self,nick):
		i = 0
		while i<self.contactlist.count():
			print self.contactlist.item(i).text()
			print self.contactlist.count
			if self.contactlist.item(i).text() == nick:
				self.contactlist.takeItem(i)
				return
			i=i+1
	def closeEvent(self,event):
		print u'täällä'
		if hasattr(self, 'sock'):
			self.sock.shutdown(socket.SHUT_RDWR)
			self.sock.close()
		event.accept()
	def connectToServer(self,address,port,nick): #Function that creates socket and connects it to the server. Also validates given nickname by login()-function.
		try:#Check for given portnumber
			portno = int(port)
		except ValueError:
			QMessageBox.about(self,'Invalid port number','Port number must be integer')
			return False
		
		#Creating socket
		try:
			self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		except socket.error as msg:
			QMessageBox.about(self,'SocketError','Failed to create socket')
			self.sock = None
		
		#Connecting to server
		try:
			self.sock.connect((address,portno))
		except socket.error as msg:
			QMessageBox.about(self,'SocketError','Cannot connect to server')
			self.sock.close()
			self.sock = None
		
		#If socket is not created successfully or connecting to server is failed, function return False.
		if self.sock is None:
			return False
		
		#If nickname is already taken. User have to choose another nickname.
		if self.login(nick) is False:
			self.sock.close()
			self.sock = None
			return False
			
		self.nick = nick
		
		#Connecting client to server is done. So now client thread is created and started for communication
		self.loginwindow.close()
		ct = ClientThread(self)
		ct.start()
	def routeMessage(self, sender, msg):
		for m in self.msgwindows:
			print '{0}:{1}'
			if m.nick == sender:
				m.displayMessage(sender,msg)
				return
		m = MessageWindow(self.sock, sender) #If there is no messagewindow for client yet, it is created now.
		self.msgwindows.append(m)
		self.routeMessage(sender,msg)
	def chat(self,item):
		m = MessageWindow(self.sock,item.text())
		self.msgwindows.append(m)
app = QApplication(sys.argv)
client = Client(app)
sys.exit(app.exec_())
