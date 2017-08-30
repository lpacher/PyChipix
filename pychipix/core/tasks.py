
#----------------------------------------------------------------------------------------------------
#                                        VLSI Design Laboratory
#                               Istituto Nazionale di Fisica Nucleare (INFN)
#                                   via Giuria 1 10125, Torino, Italy
#----------------------------------------------------------------------------------------------------
# {Trace}
# [Filename]      tasks.py
# [Project]       CHIPIX65 demonstrator PyROOT-based DAQ
# [Author]        Luca Pacher - pacher@to.infn.it
# [Version]       1.0
# [Language]      Python/ROOT
# [Created]       Aug 26, 2017
# [Description]   Collection of standalone low-level functions, also callable interactively from CLI
# [Notes]         -
# {Trace}
#----------------------------------------------------------------------------------------------------

#import sys

import ROOT

from connection import Connection
from GbPhy import *

from typedef import *





##________________________________________________________________________________
def connect(hostIpAddress="192.168.1.1", boardNumber=0, timeoutMilliSeconds=1000) :
	"""Try to open connection to target FPGA according to board number"""

	## create and bind UDP socket (define c as global for usage in other functions)

	global c
	c = Connection(hostIpAddress, boardNumber, timeoutMilliSeconds*1e-3)
	c.Open()

	## not required to return Connection() object, c is already global to this module
	#return c

	## get FPGA firmware version to validate the connection
	firmwareVersion = getFirmwareVersion()

	if(firmwareVersion != -1) :
		print "\n**INFO: Connection to FPGA successfully established!\n"
		Connection.isConnected = True
		return [1, firmwareVersion]

	else :
		print "\n**ERROR: Cannot connect to target FPGA!\n"
		Connection.isConnected = False
		return [0, "-1"]


##________________________________________________________________________________
def disconnect() :
	"""Try to close connection to target FPGA"""

	if(Connection.isConnected) :

		c.Close()
		return 1

	else :

		print "\n**ERROR: Connection to FPGA not available!\n"
		return -1	



##________________________________________________________________________________
def getFirmwareVersion() :

	try :

		## build command string
		commandString = cpuCommandPacket("getFirmwareVersion")

		## send command string
		sendCommandStringToFPGA(commandString)	

		## get reply
		replyString = getReplyStringFromFPGA()

		## validate tx/rx packets
		if(replyString[0:3+1] != commandString[0:3+1]) :

			print "\n**ERROR: Command error!"

		else :

			## packets match, get firmware version from latest 2 characters out of 8
			firmwareVersion = "0x" + replyString[6:].encode("hex").upper()

			print "\n**INFO: FPGA firmware version is %s\n" % firmwareVersion
			return firmwareVersion

	except :

		print "\n**ERROR: Cannot get firmware version from FPGA!\n"
		return -1


##________________________________________________________________________________
def getReplyStringFromFPGA(bufferSize=8192) :
	return Connection.udpSocket.recvfrom(bufferSize)[0]



##________________________________________________________________________________
def man() :

	f = open("./doc/help.txt")

	lines = f.read().splitlines()
	f.close()

	for line in lines :
		print line


##________________________________________________________________________________
def quit() :

	if(Connection.isConnected) :
		disconnect()

	print "Bye!"

	## close the main ROOT TApplication event loop and exit
	ROOT.gApplication.Terminate(0)
	raise SystemExit



##________________________________________________________________________________
def read8b10bErrorCounters() :
	pass



##________________________________________________________________________________
def readADC(adcEocDelay=99999) :


	if(Connection.isConnected) :

		## build command strings
		commandString  = commandPacket("doSpiOperation", 0x70000) 
		commandString += commandPacket("waitDelay",      adcEocDelay)
		commandString += commandPacket("doSpiOperation", 0xF0000)

		## send command string
		sendCommandStringToFPGA(commandString)

		## get reply
		replyString = getReplyStringFromFPGA()

		## validate tx/rx packets
		if(replyString[0:20+1] != commandString[0:20+1]) :

			print "\n**ERROR: Command error!"
			return -1

		else :

			## packets match, get ADC code from last 2 characters out of 24
			adcCode = int(replyString[22:].encode("hex"), 16)

			## ADC code validation
			if(adcCode == 0xFFFF) :

				print "\n**WARN: invalid ADC code 0xFFFF from SPI\n"

			return adcCode 

	else :

		print "\n**ERROR: Connection to FPGA not available!\n"
		return -1







##________________________________________________________________________________
def readECCR() :
	pass


##________________________________________________________________________________
def readGCR(mode="auto") :
	"""Read all GRs through SPI using either normal or auto-increment modes"""

	if(Connection.isConnected) :

		## create a default GCR, then fill with received words
		r = GCR()


		## **DEBUG
		#for i in range(14) :
		#	r.SetRegisterContent(i, int(ROOT.gRandom.Uniform(0, 2**16 -1)))


		########################
		##   auto-increment   ##
		########################
		if(mode == "auto") :

			## write POINTER register only once, select auto-increment and select GCR => 0000|1_001|xxxxxxxxxxxx
			spiFrame = 0x09000
			commandString = commandPacket("doSpiOperation", spiFrame)


			## loop over GCRs and append command strings
			for i in range(14) :

				## read DATA registera => 1001|xxxx_xxxx_xxxx_xxxx
				spiFrame = 0x90000
				commandString += commandPacket("doSpiOperation", spiFrame)


			## send command string
			sendCommandStringToFPGA(commandString)


			## get reply string
			replyString = getReplyStringFromFPGA()

			#print commandString.encode("hex")
			#print replyString.encode("hex")


			## validate tx/rx packets
			for i in range(15) :

				if(i == 0) :
				
					if(replyString[8*i:8*i+5] != commandString[8*i:8*i+5]) :

						print "\n**ERROR: Command error!"
						return -1

					else :
						pass

				else :

					if(replyString[8*i:8*i+5] != commandString[8*i:8*i+5]) :

						print "\n**ERROR: Command error!"
						return -1

					else :

						word = int(replyString[8*i+6:8*i+6+2].encode("hex"), 16)
						r.SetRegisterContent(i-1, word)

						## **DEBUG
						#print word
						#print r.GetRegisterBinWord(i-1)


			## update electrical parameters from register slices
			r.UpdateParameters()

			print "\n**INFO: GCR values successfully read from chip!\n"
			return r


		#####################
		##   normal mode   ##
		#####################
		elif(mode == "normal") :

			commandString = ""
			"""
			## loop over GCRs and build POINTER/DATA sequences
			for i in range(14) :
				
				## write POINTER register each time, select normal mode and insert GCR address from iterator => 0000|0_001|xxxx_xxxx_a3a2a1a0
				spiFrame = 0x01000 | i
				commandString += commandPacket("doSpiOperation", spiFrame)

				## write DATA register and add payload => 0001|word
				spiFrame = 0x10000 | r.GetRegisterContent(i)
				commandString += commandPacket("doSpiOperation", spiFrame)


			## send command string
			sendCommandStringToFPGA(commandString)


			## get reply string
			replyString = getReplyStringFromFPGA()



			## validate tx/rx packets
			if(replyString != commandString) :

				print "\n**ERROR: Command error!"
				return -1

			else :
				
				## update electrical parameters from registers slices
				return r.Update() 
			"""
		else :
			print "Incorrect usage: writeGCR(r, 'auto|normal')"


	else :

		print "\n**ERROR: Connection to FPGA not available!\n"
		return -1







##________________________________________________________________________________
def readPCR() :
	pass



##________________________________________________________________________________
def reset() :
	resetChip()


##________________________________________________________________________________
def resetChip() :

	if(Connection.isConnected) :

		## build command strings
		commandString  = commandPacket("resetChip", 0x0) 

		## send command string
		sendCommandStringToFPGA(commandString)

		## get reply
		replyString = getReplyStringFromFPGA()

		## validate tx/rx packets
		if(replyString != commandString) :

			print "\n**ERROR: Command error!"
			return -1

		else :

			print "\n**INFO: reset sent to ASIC\n"
			pass


	else :

		print "\n**ERROR: Connection to FPGA not available!\n"
		return -1


##________________________________________________________________________________
def resetClockCounters() :
	pass



##________________________________________________________________________________
def resetFpgaCounters() :


	if(Connection.isConnected) :

		## build command strings
		commandString  = commandPacket("resetFpgaCounters", 0x0) 

		## send command string
		sendCommandStringToFPGA(commandString)

		## get reply
		replyString = getReplyStringFromFPGA()

		## validate tx/rx packets
		if(replyString != commandString) :

			print "\n**ERROR: Command error!"
			return -1

		else :

			print "\n**INFO: reset sent to FPGA counters\n"
			pass


	else :

		print "\n**ERROR: Connection to FPGA not available!\n"
		return -1



##________________________________________________________________________________
def sendCommandStringToFPGA(commandString) :
	Connection.udpSocket.sendto(commandString, (c.fRemoteAddress, c.fRemotePort))



##________________________________________________________________________________
def sendSpiFrame(spiFrame) :

	## **NOTE: spiFrame = 4-bit command + 16-bit payload data

	if(Connection.isConnected) :

		## build command strings
		commandString  = commandPacket("doSpiOperation", spiFrame) 

		## send command string
		print "\n**INFO: Sending SPI frame: %s\n" % format(spiFrame, "05x")
		sendCommandStringToFPGA(commandString)

		## get reply
		replyString = getReplyStringFromFPGA()

		## validate tx/rx packets
		if(replyString[0:5+1] != commandString[0:5+1]) :

			print "\n**ERROR: Command error!"
			return -1

		else :

			## packets match, get SPI reply frame from latest 4 characters keeping only 20 LSBs
			spiReplyFrame = int(replyString[4:].encode("hex"), 16) & 0x0FFFFF

			print "\n**INFO: Received SPI reply frame: %s\n" % format(spiReplyFrame, "05x")
			return spiReplyFrame

	else :

		print "\n**ERROR: Connection to FPGA not available!\n"
		return -1



##________________________________________________________________________________
def sendTestPulse() :
	pass




##________________________________________________________________________________
def synchronizeTx8b10b() :

	#return syncOK

	pass


##________________________________________________________________________________
def writeECCR() :
	pass



##________________________________________________________________________________
def writeGCR(r, mode="auto") :
	"""Writes all GCRs through SPI using either normal or auto-increment modes"""


	if(Connection.isConnected) :


		########################
		##   auto-increment   ##
		########################
		if(mode == "auto") :

			## write POINTER register only once, select auto-increment and select GCR => 0000|1_001|xxxxxxxxxxxx
			spiFrame = 0x09000
			commandString = commandPacket("doSpiOperation", spiFrame)


			## loop over GCRs and append command strings
			for i in range(14) :

				## write DATA register and insert payload data => 0001|16-bit payload
				spiFrame = 0x10000 | r.GetRegisterContent(i)
				commandString += commandPacket("doSpiOperation", spiFrame)


			## send command string
			sendCommandStringToFPGA(commandString)


			## get reply string
			replyString = getReplyStringFromFPGA()


			## validate tx/rx packets
			if(replyString != commandString) :

				print "\n**ERROR: Command error!"
				return -1

			else :
				print "\n**INFO: GCR values successfully written to chip!\n"
				return 1


		#####################
		##   normal mode   ##
		#####################
		elif(mode == "normal") :

			commandString = ""

			## loop over GCRs and build POINTER/DATA sequences
			for i in range(14) :
				
				## write POINTER register each time, select normal mode and insert GCR address from iterator => 0000|0_001|xxxx_xxxx_a3a2a1a0
				spiFrame = 0x01000 | i
				commandString += commandPacket("doSpiOperation", spiFrame)

				## write DATA register and add payload => 0001|word
				spiFrame = 0x10000 | r.GetRegisterContent(i)
				commandString += commandPacket("doSpiOperation", spiFrame)


			## send command string
			sendCommandStringToFPGA(commandString)


			## get reply string
			replyString = getReplyStringFromFPGA()



			## validate tx/rx packets
			if(replyString != commandString) :

				print "\n**ERROR: Command error!"
				return -1

			else :
				print "\n**INFO: GCR values successfully written to chip!\n"
				return 1

		else :
			print "Incorrect usage: writeGCR(r, 'auto|normal')"


	else :

		print "\n**ERROR: Connection to FPGA not available!\n"
		return -1





##________________________________________________________________________________
def writePCR() :
	pass


