# encoding=utf-8
from PyQt4.QtGui import *
from PyQt4 import QtCore
import atexit
import sys

class LoginWindow(QWidget):
	def __init__(self, client):
		super(LoginWindow,self).__init__()
		#Setting client window to loginwindow's attribute. Now it is possible to call clientwindow's connectToServer()-operation.
		self.client = client
		
		#Mainlayout
		grid = QGridLayout()
		grid.setSpacing(5)
		
		#Creating controls
		nicknamelabel = QLabel('Nickname:')
		self.nicknameinput = QLineEdit()
		addresslabel = QLabel('Server address:')
		self.addressinput = QLineEdit('0.0.0.0')
		portlabel = QLabel('Port:')
		self.portinput = QLineEdit('8080')
		loginbtn = QPushButton('Login')
		
		#Adding controls to main layout
		grid.addWidget(nicknamelabel,0,0)
		grid.addWidget(self.nicknameinput,0,1)
		grid.addWidget(addresslabel,1,0)
		grid.addWidget(self.addressinput,1,1)
		grid.addWidget(portlabel,2,0)
		grid.addWidget(self.portinput,2,1)
		grid.addWidget(loginbtn,3,0,1,2)
		
		#Set listener for login-button
		loginbtn.clicked.connect(self.login)
		
		#Set main layout
		self.setLayout(grid)
		
		#Modify login-window and show it
		self.setWindowTitle('Login Window')
		self.show()
		
	def login(self):
		address = self.addressinput.text()
		port = self.portinput.text()
		nickname = self.nicknameinput.text()
		
		#If connection is successfully established, login window is closed.
		if self.client.connectToServer(address, port, nickname) is True:
			self.close()
	def keyPressEvent(self,e):
		#print '{0}=={1} returns {2}'.format(e.key(),QtCore.Qt.Key_Return,QtCore.Qt.Key_Return==e.key())
		if e.key() == QtCore.Qt.Key_Enter:
			print 'jsjsj'
			self.login()
		else:
			print 'failed'
