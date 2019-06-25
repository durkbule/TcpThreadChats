#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import socket
import _thread


class MyThread(QtCore.QThread):

	def __init__(self, win):
		super(MyThread, self).__init__(win) 
		self.win = win

	def run(self):
		print(type(self.win))
		while True:
			try:
				data = self.win.client_socket.recv(Client.BUF_LEN)
			except:
				break
			if not data or not len(data):
				break
			self.win.txt_recvMessage.append(data)
			print(data)
		self.win.disConnect()


class Client(QtWidgets.QWidget):

	BUF_LEN = 1024

	def __init__(self, parent=None):

		QtWidgets.QWidget.__init__(self, parent)

		self.setWindowTitle(u'TCP客户端')
		self.resize(600, 500)
		self.center()
		layout = QtWidgets.QGridLayout(self)

		label_ip = QtWidgets.QLabel(u'远程主机IP：')
		layout.addWidget(label_ip, 0, 0, 1, 1)
		self.txt_ip = QtWidgets.QLineEdit('127.0.0.1')
		layout.addWidget(self.txt_ip, 0, 1, 1, 3)

		label_port = QtWidgets.QLabel(u'端口：')
		layout.addWidget(label_port, 0, 4, 1, 1)
		self.txt_port = QtWidgets.QLineEdit('9003')
		layout.addWidget(self.txt_port, 0, 5, 1, 3)

		self.isConnected = False
		self.btn_connect = QtWidgets.QPushButton(u'连接')
		self.btn_connect.clicked.connect(self.myConnect())
		#self.connect(self.btn_connect, QtCore.SIGNAL(
			#'clicked()'), self.myConnect)
		layout.addWidget(self.btn_connect, 0, 8, 1, 2)

		label_recvMessage = QtWidgets.QLabel(u'消息内容：')
		layout.addWidget(label_recvMessage, 1, 0, 1, 1)

		self.btn_clearRecvMessage = QtWidgets.QPushButton(u'↓ 清空消息框')
		self.btn_clearRecvMessage.clicked.connect(self.myClearRecvMessage())
		#self.connect(self.btn_clearRecvMessage, QtCore.SIGNAL(
			#'clicked()'), self.myClearRecvMessage)
		layout.addWidget(self.btn_clearRecvMessage, 1, 7, 1, 3)


		self.txt_recvMessage = QtWidgets.QTextEdit()
		self.txt_recvMessage.setReadOnly(True)
		self.txt_recvMessage.setStyleSheet('background-color:yellow')
		layout.addWidget(self.txt_recvMessage, 2, 0, 1, 10)

		lable_name = QtWidgets.QLabel(u'姓名(ID)：')
		layout.addWidget(lable_name, 3, 0, 1, 1)
		self.txt_name = QtWidgets.QLineEdit()
		layout.addWidget(self.txt_name, 3, 1, 1, 3)

		self.isSendName = QtWidgets.QRadioButton(u'发送姓名')
		self.isSendName.setChecked(False)
		layout.addWidget(self.isSendName, 3, 4, 1, 1)

		label_sendMessage = QtWidgets.QLabel(u' 输入框：')
		layout.addWidget(label_sendMessage, 4, 0, 1, 1)
		self.txt_sendMessage = QtWidgets.QLineEdit()
		self.txt_sendMessage.setStyleSheet("background-color:cyan")
		layout.addWidget(self.txt_sendMessage, 4, 1, 1, 7)
		self.btn_send = QtWidgets.QPushButton(u'发送')
		self.btn_send.clicked.connect(self.myConnect)
		#self.connect(self.btn_send, QtCore.SIGNAL('clicked()'), self.mySend)
		layout.addWidget(self.btn_send, 4, 8, 1, 2)

		self.btn_clearSendMessage = QtWidgets.QPushButton(u'↑ 清空输入框')
		self.btn_clearSendMessage.clicked.connect(self.myClearSendMessage)
		#self.connect(self.btn_clearSendMessage, QtCore.SIGNAL(
			#'clicked()'), self.myClearSendMessage)
		layout.addWidget(self.btn_clearSendMessage, 5, 6, 1, 2)
		self.btn_quit = QtWidgets.QPushButton(u'退出')
		self.btn_quit.clicked.connect(self.my.Quit)
		#self.connect(self.btn_quit, QtCore.SIGNAL('clicked()'), self.myQuit)
		layout.addWidget(self.btn_quit, 5, 8, 1, 2)

	def myConnect(self):
		if self.isConnected == False:
			host = str(self.txt_ip.text())
			port = int(self.txt_port.text())
			try:
				self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
				self.client_socket.connect((host, port))
			except:
				self.txt_recvMessage.append(u'服务器连接失败，请检查网络连接或者稍后再试。')
				return

			_thread.start_new_thread(self.recv_func, ())
			# td = MyThread(self)
			# td.start()
			self.txt_recvMessage.append(u'服务器连接成功！')
			self.setWindowTitle(self.windowTitle() + ' --> ' + host + ':' + str(port))
			self.isConnected = True

			self.btn_connect.setText(u'断开连接')
		else:
			self.disConnect()

	def disConnect(self):
		self.client_socket.close()
		self.txt_recvMessage.append(u'已断开与服务器的连接。')
		self.setWindowTitle(u'TCP客户端')
		self.isConnected = False
		self.btn_connect.setText(u'连接')

	def recv_func(self):
		while True:
			try:
				data = self.client_socket.recv(Client.BUF_LEN)
			except:
				break
			if not data or not len(data):
				break
			data = data[:-1]
			self.txt_recvMessage.append(data.decode('utf8'))	# 很重要
		self.disConnect()

	def myClearRecvMessage(self):
		self.txt_recvMessage.setText('')

	def myClearSendMessage(self):
		self.txt_sendMessage.setText('')

	def mySend(self):
		if self.isSendName.isChecked() == True:
			data = self.txt_name.text()
			if data == '':
				data = u'[匿名]'
			data =  str((data + ': ' + self.txt_sendMessage.text() + '\n').toUtf8())
		else:
			data =  str((self.txt_sendMessage.text() + '\n').toUtf8())
		try:
			self.client_socket.sendall(data)
		except:
			self.txt_recvMessage.append(u'消息发送失败...')
			return 
		self.txt_sendMessage.setText('')

	def myQuit(self):
		self.close()

	def center(self):
		screen = QtWidgets.QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move((screen.width() - size.width()) / 2,
				(screen.height() - size.height()) / 2)

	def closeEvent(self, event):
		reply = QtWidgets.QMessageBox.question(self, u'消息', u'你确定要退出吗？',
										 QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
		if reply == QtWidgets.QMessageBox.Yes:
			event.accept()
			self.client_socket.close()
		else:
			event.ignore()

app = QtWidgets.QApplication(sys.argv)
c = Client()
c.show()
sys.exit(app.exec_())
