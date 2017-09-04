
#----------------------------------------------------------------------------------------------------
#                                        VLSI Design Laboratory
#                               Istituto Nazionale di Fisica Nucleare (INFN)
#                                   via Giuria 1 10125, Torino, Italy
#----------------------------------------------------------------------------------------------------
# {Trace}
# [Filename]      Connection.py [CLASS]
# [Project]       CHIPIX65 demonstrator PyROOT-based DAQ
# [Author]        Luca Pacher - pacher@to.infn.it
# [Version]       1.0
# [Language]      Python/ROOT
# [Created]       Aug 26, 2017
# [Description]   Global connection class, mainly used as a namespace and C-style struct
# [Notes]         -
# {Trace}
#----------------------------------------------------------------------------------------------------


import socket


class Connection(object) :

	## class attributes
	udpSocket     = None
	isConnected   = False

	remoteAddress = 65535 
	remotePort    = 65535


	##________________________________________________________________________________
	def __init__(self, hostIpAddress="192.168.1.1", boardNumber=0, timeoutSeconds=1.0) :

		self.fLocalAddress   = hostIpAddress
		self.fBoardNumber    = boardNumber
		self.fTimeoutSeconds = timeoutSeconds


	##________________________________________________________________________________
	def BoardMapping(self) :
		"""Python implementation of GbPhy_BoardMapping.vi"""


		## attributes determined from board number
		self.fRemoteAddress     = ""
		self.fRemotePort        = 65535 
		self.fRemoteEventsPort  = 65535
		self.fRemoteEventHeader = 65535


		## determine IP address/port according to board number
		if(self.fBoardNumber == 0) :
			self.fRemoteAddress     = "192.168.1.10"
			self.fRemotePort        = 10000
			self.fRemoteEventsPort  = 10020
			self.fRemoteEventHeader = 0xDCBA
		elif(self.fBoardNumber == 1) :
			self.fRemoteAddress     = "192.168.1.11"
			self.fRemotePort        = 10001
			self.fRemoteEventsPort  = 10021
			self.fRemoteEventHeader = 0xDCBB
		elif(self.fBoardNumber == 2) :
			self.fRemoteAddress     = "192.168.1.12"
			self.fRemotePort        = 10002
			self.fRemoteEventsPort  = 10022
			self.fRemoteEventHeader = 0xDCBC
		elif(self.fBoardNumber == 3) :
			self.fRemoteAddress     = "192.168.1.13"
			self.fRemotePort        = 10003
			self.fRemoteEventsPort  = 10023
			self.fRemoteEventHeader = 0xDCBD
		elif(self.fBoardNumber == 4) :
			self.fRemoteAddress     = "192.168.1.14"
			self.fRemotePort        = 10004
			self.fRemoteEventsPort  = 10024
			self.fRemoteEventHeader = 0xDCBE
		elif(self.fBoardNumber == 5) :
			self.fRemoteAddress     = "192.168.1.15"
			self.fRemotePort        = 10005
			self.fRemoteEventsPort  = 10025
			self.fRemoteEventHeader = 0xDCBF
		elif(self.fBoardNumber == 6) :
			self.fRemoteAddress     = "192.168.1.16"
			self.fRemotePort        = 10006
			self.fRemoteEventsPort  = 10026
			self.fRemoteEventHeader = 0xDCB8
		elif(self.fBoardNumber == 7) :
			self.fRemoteAddress     = "192.168.1.17"
			self.fRemotePort        = 10007
			self.fRemoteEventsPort  = 10027
			self.fRemoteEventHeader = 0xDCB9
		else :	
			self.fRemoteAddress     = ""
			self.fRemotePort        = 65535
			self.fRemoteEventsPort  = 65535
			self.fRemoteEventHeader = 65535


		## required to send/receive from FPGA
		Connection.remoteAddress = self.fRemoteAddress
		Connection.remotePort    = self.fRemotePort

		## no necessity to return any values since the function already modifies class attributes
		#return [remoteAddress, remotePort, remoteEventsPort, remoteEventHeader]


	##________________________________________________________________________________
	def Close(self) :

		Connection.udpSocket.close()
		Connection.isConnected = False

		## reset class attributes
		Connection.udpSocket   = None
		Connection.isConnected = False

		print "\n**INFO: Connection closed!\n"



	##________________________________________________________________________________
	def GetBoardNumber(self) :

		return self.fBoardNumber



	##________________________________________________________________________________
	def GetLocalAddress(self) :

		return self.fLocalAddress


	##________________________________________________________________________________
	def GetRemoteAddress(self) :

		return self.fRemoteAddress


	##________________________________________________________________________________
	def GetRemoteEventHeader(self) :

		return self.fRemoteEventHeader



	##________________________________________________________________________________
	def GetRemoteEventPort(self) :

		return self.fRemoteEventPort


	##________________________________________________________________________________
	def GetRemotePort(self) :

		return self.fRemotePort



	##________________________________________________________________________________
	def Open(self) :

		try :

			if(Connection.isConnected == False) :

				## assign IP addresses/ports according to board number
				self.BoardMapping()

				## create socket (Internet protocol, UDP protocol)
				Connection.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				Connection.udpSocket.settimeout(self.fTimeoutSeconds)

				## bind socket to UDP port
				Connection.udpSocket.bind((self.fLocalAddress, self.fRemotePort))

			else :

				## connection already established otherwise, do nothing
				pass

		except :

			## socket error
			print "\n**ERROR: Cannot bind UDP socket!\n"
			pass

