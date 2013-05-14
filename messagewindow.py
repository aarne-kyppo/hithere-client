# encoding=utf-8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
class MessageWindow(QWidget):
	def __init__(self, client, nick):
		super(MessageWindow,self).__init__()
		
		self.nick = str(nick) #Client who receives messages from this window
		self.client = client #Clientsocket.
		
		self.grid = QGridLayout() #Main layout for MessageWindow-object
		self.grid.setSpacing(5)
		
		#Creating controls
		self.talkbox = QTextEdit() #In this control conversation is shown
		self.msginput = QLineEdit() #Input for new messages
		self.msgsnd = QPushButton('Send') #Button to send message
		
		#Setting action for message-sending button(self.msgsnd)
		self.msgsnd.clicked.connect(self.sendMessage)
		
		#Add controls to grid
		self.grid.addWidget(self.talkbox,0,0,5,5)
		self.grid.addWidget(self.msginput,5,0,1,4)
		self.grid.addWidget(self.msgsnd,5,4)
		
		#Set grid to be main layout
		self.setLayout(self.grid)
		
		#Modify window and show it
		self.setGeometry(200,200,400,500)
		self.setWindowTitle(self.nick)
		self.show()
	def sendMessage(self):
		if self.msginput.text:
			print unicode(self.msginput.text(),'utf-8')
			self.client.sendall('msg:{0}:{1};'.format(self.nick, unicode(self.msginput.text(),'utf-8')))
			self.displayMessage('Me',self.msginput.text())
	def displayMessage(self, sender, msg):
		print u'hähähähägh'
		self.talkbox.append(u'{0}: {1}\n'.format(sender,msg))
