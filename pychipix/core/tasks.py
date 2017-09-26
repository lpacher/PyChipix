
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


## standard library components
import os


## ROOT components
try :
	import ROOT

except ImportError :

	print("**ERROR: ROOT components are required to run this application!")

	if( os.name == 'nt') :
		print("           call %ROOTSYS%\bin\thisroot.bat might solve this problem.")
	else :
		print("           source $ROOTSYS/bin/thisroot.(c)sh might solve this problem.")

	raise SystemExit



## user-defined modules
from connection import Connection
from GbPhy import *
from registers import *

#from GUI import GUI 
import GUI
from ControlBar   import ControlBar
from TestCommands import TestCommandsGui
from PixelScan    import PixelScanGui


## keep track of the number if command errors with a ROOT histogram
global hCommandErrors
hCommandErrors = ROOT.TH1F("hCommandErrors", "", 2, -0.5, 1.5)


##________________________________________________________________________________
def broadcastiPCRconfiguration(r) :

	## **NOTE: mapped as "Write PCR Defaults" button in TestCommands.vi

	## **TODO
	pass


##________________________________________________________________________________
def browser() :

	global b
	b = ROOT.TBrowser()



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
		print "**INFO: Connection to FPGA successfully established!"
		Connection.isConnected = True
		return [1, firmwareVersion]

	else :
		print "**ERROR: Cannot connect to target FPGA!"
		Connection.isConnected = False
		return [0, "-1"]


##________________________________________________________________________________
def disconnect() :
	"""Try to close connection to target FPGA"""

	if(Connection.isConnected) :

		c.Close()
		return 1

	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1


##________________________________________________________________________________
def flushEvents() :

	if(Connection.isConnected) :

	
		## build command string
		commandString = commandPacket("flushEvents", 0x0)


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString != commandString) :

			print "**ERROR: Command error!"
			return -1

		else :

			## packets match, nothing to do
			return 1


	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1


##________________________________________________________________________________
def flushTxDataFifo() :

	## **NOTE: mapped as "Flush TX FIFO" button in TestCommands.vi


	if(Connection.isConnected) :

	
		## build command string
		commandString = commandPacket("flushTxDataFifo", 0x0)


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString != commandString) :

			print "**ERROR: Command error!"
			return -1

		else :

			## packets match, nothing to do
			return 1


	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1




##________________________________________________________________________________
def getFirmwareVersion() :

	try :

		## build command string
		commandString = cpuCommandPacket("getFirmwareVersion")


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString[0:3+1] != commandString[0:3+1]) :

			print "**ERROR: Command error!"

		else :

			## packets match, get firmware version from latest 2 characters out of 8
			firmwareVersion = "0x" + replyString[6:].encode("hex").upper()

			print "**INFO: FPGA firmware version is %s" % firmwareVersion
			return firmwareVersion

	except :

		print "**ERROR: Cannot get firmware version from FPGA!"
		return -1






##________________________________________________________________________________
def gui() :

	"""just an alias for less typing"""
	showBar()






##________________________________________________________________________________
def closeBar() :

	## TControlBar inherits from TObject, use Delete()
	if(GUI.bar != None) :	

		GUI.bar.__del__()

		ROOT.gROOT.Reset("a")


##________________________________________________________________________________
def man() :

	os.system("more README.md")

	"""
	f = open("./doc/help.txt")

	lines = f.read().splitlines()
	f.close()

	count = 0

	for line in lines :

		print line
		count = count+1

		if(count % 25 == 0) :
			raw_input()
	"""


##________________________________________________________________________________
def programSpiSequence(spiSequenceRamStartAddress=0, spiSequence=[0]) :

	## **TODO
	pass


##________________________________________________________________________________
def programTestPulseSequence(testPulseSequence=[0]) :

	## **TODO
	pass



##________________________________________________________________________________
def quit() :

	if(Connection.isConnected) :
		disconnect()

	print "Bye!"

	## close the main ROOT TApplication event loop and exit
	ROOT.gApplication.Terminate(0)
	ROOT.gROOT.Reset("a")

	#exit()
	raise SystemExit



##________________________________________________________________________________
def read8b10bErrorCounters() :

	## **TODO
	#return 8b10ErrorCount
	pass



##________________________________________________________________________________
def readExtADC() :


	if(Connection.isConnected) :


		## build command strings
		commandString  = commandPacket("readPcbAdc", 0x00000) 


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString[0:4+1] != commandString[0:4+1]) :

			print "**ERROR: Command error!"
			return -1

		else :

			## packets match, get ADC code from last 2 characters out of 8
			extAdcCode = int(replyString[6:].encode("hex"), 16)

			## ADC code validation (TBC)
			if(extAdcCode == 0xFFFF) :

				print "**WARN: invalid ADC code 0xFFFF from SPI"

			return extAdcCode 

	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1



##________________________________________________________________________________
def readADC(adcEocDelay=99999) :


	if(Connection.isConnected) :


		## build command strings
		commandString  = commandPacket("doSpiOperation", 0x70000) 
		commandString += commandPacket("waitDelay",      adcEocDelay)
		commandString += commandPacket("doSpiOperation", 0xF0000)


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString[0:20+1] != commandString[0:20+1]) :

			print "**ERROR: Command error!"
			return -1

		else :

			## packets match, get ADC code from last 2 characters out of 24
			adcCode = int(replyString[22:].encode("hex"), 16)

			## ADC code validation
			if(adcCode == 0xFFFF) :

				print "**WARN: invalid ADC code 0xFFFF from SPI"

			return adcCode 

	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1






##________________________________________________________________________________
def readECCR() :
	"""Read ECCR registers through SPI using normal mode (auto-increment not implemented for ECCR)"""


	## **NOTE: auto-increment mode is NOT implemented for ECCR registers!

	if(Connection.isConnected) :

		## create a default ECCR object, then fill with received words

		## **DEBUG
		#for i in range(2) :
		#	r.SetRegisterContent(i, int(ROOT.gRandom.Uniform(0, 2**16 -1)))


		## write POINTER register, select normal mode and select ECCR_0 => 0000|0_010|xxxx_xxxx_xxx0
		spiFrame = 0x02000
		commandString = commandPacket("doSpiOperation", spiFrame)


		## write DATA register for readback => 1001|xxxx_xxxx_xxxx_xxxx
		spiFrame = 0x90000
		commandString += commandPacket("doSpiOperation", spiFrame)


		## write POINTER register, select normal mode and select ECCR_0 => 0000|0_010|xxxx_xxxxi_xxx1
		spiFrame = 0x02001
		commandString += commandPacket("doSpiOperation", spiFrame)


		## write DATA register for readback => 1001|xxxx_xxxx_xxxx_xxxx
		spiFrame = 0x90000
		commandString += commandPacket("doSpiOperation", spiFrame)


		## **DEBUG
		#print commandString


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)

		#print commandString.encode("hex")
		#print replyString.encode("hex")


		## validate tx/rx packets
		for i in range(4) :

			if(replyString[8*i:8*i+5] != commandString[8*i:8*i+5]) :   ## Richard

				print "**ERROR: Command error!"
				return -1

			else :

				## if strings match, readback data are contained in latest 2-characters of even 8-characters strings
				if( i % 2 == 1) :

					word = int(replyString[8*i+6:8*i+6+2].encode("hex"), 16)
					r.SetRegisterContent(i/3, word)                                    ## i/3 => 1/3 = 0, 3/3 = 1 OK


		## update electrical parameters from register slices
		r.UpdateParameters()

		print "**INFO: ECCR values successfully read from chip!"
		return r

	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1


##________________________________________________________________________________
def readGCR(mode="auto") :
	"""Read all GRs through SPI using either normal or auto-increment modes"""

	if(Connection.isConnected) :

		## create a default GCR object, then fill with received words
		r = GCR()


		## **DEBUG
		#for i in range(14) :
		#	r.SetRegisterContent(i, int(ROOT.gRandom.Uniform(0, 2**16 -1)))


		########################
		##   auto-increment   ##
		########################
		if(mode == "auto") :

			## write POINTER register only once, select auto-increment and select GCR => 0000|1_001|xxxx_xxxxi_xxxx
			spiFrame = 0x09000
			commandString = commandPacket("doSpiOperation", spiFrame)


			## loop over GCRs and append command strings
			for i in range(14) :

				## read DATA registera => 1001|xxxx_xxxx_xxxx_xxxx
				spiFrame = 0x90000
				commandString += commandPacket("doSpiOperation", spiFrame)


			## send/receive packets
			replyString = GbPhyCommandAndResponse(c, commandString)

			## **DEBUG
			#print commandString.encode("hex")
			#print replyString.encode("hex")


			## validate tx/rx packets
			for i in range(15) :

				if(i == 0) :
				
					#if(replyString[8*i:8*i+5] != commandString[8*i:8*i+5]) :   ## Richard
					if(replyString[0:8] != commandString[0:8]) :                ## Luca

						print "**ERROR: Command error!"
						return -1

					else :
						pass

				else :

					if(replyString[8*i:8*i+5] != commandString[8*i:8*i+5]) :

						print "**ERROR: Command error!"
						return -1

					else :

						word = int(replyString[8*i+6:8*i+6+2].encode("hex"), 16)
						r.SetRegisterContent(i-1, word)

						## **DEBUG
						#print word
						#print r.GetRegisterBinWord(i-1)


			## update electrical parameters from register slices
			r.UpdateParameters()

			print "**INFO: GCR values successfully read from chip!"
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


			## send/receive packets
			replyString = GbPhyCommandAndResponse(c, commandString)


			## validate tx/rx packets
			if(replyString != commandString) :

				print "**ERROR: Command error!"
				return -1

			else :
				
				## update electrical parameters from registers slices
				return r.Update() 
			"""
		else :
			print "Incorrect usage: writeGCR(r, 'auto|normal')"


	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1


##________________________________________________________________________________
def readGbPhyEventsLost() :

	## **TODO
	#return GbPhyEventsLostCount

	pass



##________________________________________________________________________________
def readPCR() :
	pass


##________________________________________________________________________________
def readSpiReplyRam() :

	## **TODO
	#return spiReplyRamData
	pass


##________________________________________________________________________________
def readTxFifo() :

	## **TODO
	#return [fifoData, eventPackets, eventErrors, excessBytes]
	pass


##________________________________________________________________________________
def readTxFifoDataCount() :

	## **TODO
	#return TxFifoDataCount
	pass


##________________________________________________________________________________
def readTxFifoFullCounter() :

	## **TODO
	#return TxFifoFullCount
	pass


##________________________________________________________________________________
def readTxFifoMaxCount() :

	## **TODO
	#return TxFifoMaxCount
	pass


##________________________________________________________________________________
def reset() :

	"""alias for resetChip"""

	if(resetChip() == 1) :
		return 1

	else :
		return -1



##________________________________________________________________________________
def resetChip() :

	if(Connection.isConnected) :

		## build command strings
		commandString  = commandPacket("resetChip", 0x0) 


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString != commandString) :

			print "**ERROR: Command error!"
			return -1

		else :

			print "**INFO: reset sent to ASIC"
			return 1


	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1


##________________________________________________________________________________
def resetClockCounters() :


	if(Connection.isConnected) :

	
		## build command string
		commandString = commandPacket("resetClockCounters", 0x0)


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString != commandString) :

			print "**ERROR: Command error!"
			return -1

		else :

			## packets match, nothing to do
			return 1


	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1


##________________________________________________________________________________
def resetFpgaCounters() :


	if(Connection.isConnected) :

		## build command strings
		commandString  = commandPacket("resetFpgaCounters", 0x0) 


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString != commandString) :

			print "**ERROR: Command error!"
			return -1

		else :

			print "**INFO: reset sent to FPGA counters"
			pass


	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1


##________________________________________________________________________________
def resetTestPulseSerializer() :


	if(Connection.isConnected) :

		## build command strings
		commandString  = commandPacket("resetTestPulseSerializer", 0x0) 


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString != commandString) :

			print "**ERROR: Command error!"
			return -1

		else :

			print "**INFO: reset sent to FPGA counters"
			pass


	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1



##________________________________________________________________________________
def root() :
	os.system("root -l")


##________________________________________________________________________________
def runSpiSequence(spiSequenceEndAddress=0) :


	if(Connection.isConnected) :

	
		## build command string
		commandString = commandPacket("runSpiSequence", clamp(spiSequenceEndAddress, 0, 2**16-1))   ## **NOTE: SPI RAM address is 16-bit, clamp input value


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString != commandString) :

			print "**ERROR: Command error!"
			return -1

		else :

			## packets match, nothing to do
			return 1


	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1




##________________________________________________________________________________
def sendSpiFrame(spiFrame) :

	## **NOTE: mapped as "Do SPI operation" button in TestCommands.vi


	## **NOTE: spiFrame = 4-bit command + 16-bit payload data

	if(Connection.isConnected) :

		## build command strings
		commandString  = commandPacket("doSpiOperation", spiFrame) 

		## send command string
		print "**INFO: Sending SPI frame: %s" % format(spiFrame, "05x")

		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString[0:5+1] != commandString[0:5+1]) :

			print "**ERROR: Command error!"
			return -1

		else :

			## packets match, get SPI reply frame from latest 4 characters keeping only 20 LSBs
			spiReplyFrame = int(replyString[4:].encode("hex"), 16) & 0x0FFFFF

			print "**INFO: Received SPI reply frame: %s" % format(spiReplyFrame, "05x")
			return spiReplyFrame

	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1


##________________________________________________________________________________
def sendTestPulseSequence(mode="normal", frameDelay=0, frameInterval=0, numPulses=1, triggerEnable=0, triggerDelay=0) :

	## **NOTE: mapped to "Do TP" button in TestCommands.vi

	## **TODO

	"""
	if(mode == "autozero") :


	elif(mode == "normal") :   ## **NOTE: either "normal" or "sequence" in Richard code


	else :
		print "**ERROR: Unknown mode option"
	"""

	pass


##________________________________________________________________________________
def setAutozeroingEnable(autozeroingEnable, r) :

	## **TODO

	## **NOTE: this function in Richard's .vi => 1. enables AZ and 2. programs PWM generator according to GCR! Maye redundant?


	"""
	pwmHigh = r.GetParameter(0)
	pwmLow  = r.GetParameter(1)
	"""

	pass



##________________________________________________________________________________
def setBoardLines(gpio=0, pinswap=0) :

	## **TODO
	pass



##________________________________________________________________________________
def setExtTriggerEnable(extTriggerEnable=0, extTriggerTestPulseEnable=0, extTriggetTestPulseCounterMax=0) :

	## **TODO
	pass


##________________________________________________________________________________
def setFastOrMode(fastOrModeEnable=0) :


	if(Connection.isConnected) :

	
		## build command string
		commandString = commandPacket("setFastOrMode", fastOrModeEnable)


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString != commandString) :

			print "**ERROR: Command error!"
			return -1

		else :

			## packets match, nothing to do
			return 1


	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1
	pass


##________________________________________________________________________________
def setFrameCounterEventEnable(frameCounterEventEnable=0) :

	if(Connection.isConnected) :

	
		## build command string
		commandString = commandPacket("setFrameCounterEventEnable", frameCounterEventEnable)


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString != commandString) :

			print "**ERROR: Command error!"
			return -1

		else :

			## packets match, nothing to do
			return 1


	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1
	pass


##________________________________________________________________________________
def setMux(muxEnable=0, muxAddress=0) :

	"""
	implements CHIPIX_ADC_SetMUX.vi 
	"""

	if(Connection.isConnected) :

		## data to be sent (MUX enable, MUX address)
		data = clamp(muxAddress, 0, 3) << 1 | muxEnable
	
		## build command string
		commandString = commandPacket("setPcbMux", data)


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString != commandString) :

			print "**ERROR: Command error!"
			return -1

		else :

			## packets match, nothing to do
			return 1


	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1
	pass





##________________________________________________________________________________
def setPixelRegionDebugMode(pixelRegionDebugModeEnable=0) :

	"""
	just send the proper SPI frame:
	0100|xxxx_xxxx_xxxx_xxxx => enable PR debug mode => 0x40000
	1100|xxxx_xxxx_xxxx_xxxx => disable PR debug mode => 0xC0000

	"""
	

	if(pixelRegionDebugModeEnable == 0) :

		#frame = 0xC0000
		sendSpiFrame(0xC0000)

	else :

		#frame = 0x40000
		sendSpiFrame(0x40000)


##________________________________________________________________________________
def setScanMode(scanModeEnable=0) :


	if(Connection.isConnected) :

	
		## build command string
		commandString = commandPacket("setScanMode", scanModeEnable)


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString != commandString) :

			print "**ERROR: Command error!"
			return -1

		else :

			## packets match, nothing to do
			return 1


	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1


##________________________________________________________________________________
def setSpiRamAddress(address=0, autoIncrement=0) :

	## **TODO
	pass


##________________________________________________________________________________
def setSpiSerialOffsetEnable(spiSerialOffsetEnable=0) :


	if(Connection.isConnected) :

	
		## build command string
		commandString = commandPacket("setSpiSerialOffsetEnable", spiSerialOffsetEnable)


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString != commandString) :

			print "**ERROR: Command error!"
			return -1

		else :

			## packets match, nothing to do
			return 1


	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1


##________________________________________________________________________________
def setTxDataAlignEnable(txDataAlignEnable=0) :


	"""
	just send the proper SPI frame:
	0011|xxxx_xxxx_xxxx_xxxx => enable 8b/10b synch => 0x30000
	1011|xxxx_xxxx_xxxx_xxxx => disable 8b/10b synch => 0xB0000

	"""

	if(txDataAlignEnable == 0) :

		#frame = 0xB0000
		sendSpiFrame(0xB0000)

	else :

		#frame = 0x30000
		sendSpiFrame(0x30000)


##________________________________________________________________________________
def setTxDataEnable(txDataEnable=0) :


	if(Connection.isConnected) :

	
		## build command string
		commandString = commandPacket("setTxDataEnable", txDataEnable)


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString != commandString) :

			print "**ERROR: Command error!"
			return -1

		else :

			## packets match, nothing to do
			return 1


	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1



##________________________________________________________________________________
def showBar() :

	if(ROOT.gROOT.IsBatch()) :

		print ""
		print "**WARN: Application started in batch mode, cannot open GUI items !"
		print "        Use ROOT.gROOT.SetBatch(0) if you really want graphics. "
		pass

	else :

		#global bar
		#bar = ControlBar()
		#bar.Show()

		GUI.bar = ControlBar()


##________________________________________________________________________________
def source(fileName="") :

	"""just an alias for less typing"""
	execfile(fileName)



##________________________________________________________________________________
def synchronizeTx8b10b() :

	## **TODO
	#return syncOK

	pass


##________________________________________________________________________________
def waitDelay(delay=0x00000) :


	## **NOTE: delay counter inside FPGA is 20-bit, just keep 20 LSBs of delay integer variable

	if(Connection.isConnected) :

	
		## build command string
		commandString = commandPacket("waitDelay", delay & 0xFFFFF)


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString != commandString) :

			print "**ERROR: Command error!"
			return -1

		else :

			## packets match, nothing to do
			return 1


	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1


##________________________________________________________________________________
def writeECCR(r) :
	"""Write ECCR registers through SPI using normal mode (auto-increment not implemented for ECCR)"""


	if(Connection.isConnected) :


		commandString = ""


		## write POINTER register, select normal mode and select ECCR_0 => 0000|0_010|xxxx_xxxx_xxx0
		spiFrame = 0x02000
		commandString += commandPacket("doSpiOperation", spiFrame)


		## write DATA register and insert payload data => 0001|16-bit payload
		spiFrame = 0x10000 | r.GetRegisterContent(0)
		commandString += commandPacket("doSpiOperation", spiFrame)


		## write POINTER register, select normal mode and select ECCR_0 => 0000|0_010|xxxx_xxxxi_xxx1
		spiFrame = 0x02001
		commandString += commandPacket("doSpiOperation", spiFrame)


		## write DATA register and insert payload data => 0001|16-bit payload
		spiFrame = 0x10000 | r.GetRegisterContent(1)
		commandString += commandPacket("doSpiOperation", spiFrame)


		## **DEBUG
		#print commandString


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString != commandString) :

			print "**ERROR: Command error!"
			return -1

		else :
			print "**INFO: ECCR values successfully written to chip!"
			return 1

	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1


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


			## send/receive packets
			replyString = GbPhyCommandAndResponse(c, commandString)

			print "here"

			## validate tx/rx packets
			if(replyString != commandString) :

				print "**ERROR: Command error!"
				return -1

			else :
				print "**INFO: GCR values successfully written to chip!"
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


			## send/receive packets
			replyString = GbPhyCommandAndResponse(c, commandString)


			## validate tx/rx packets
			if(replyString != commandString) :

				print "**ERROR: Command error!"
				return -1

			else :
				print "**INFO: GCR values successfully written to chip!"
				return 1

		else :
			print "Incorrect usage: writeGCR(r, 'auto|normal')"


	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1





##________________________________________________________________________________
def writePCR(r) :

	## **TODO
	pass




##________________________________________________________________________________
def writeSpiCommandRam(spiCommandRamData=0x00000000) :


	if(Connection.isConnected) :

	
		## build command string
		commandString = commandPacket("writeSpiCommandRam", spiCommandRamData & 0xFFFFFFFF)   ## **NOTE: ensure 32-bit integer value


		## send/receive packets
		replyString = GbPhyCommandAndResponse(c, commandString)


		## validate tx/rx packets
		if(replyString != commandString) :

			print "**ERROR: Command error!"
			return -1

		else :

			## packets match, nothing to do
			return 1


	else :

		print "**ERROR: Connection to FPGA not available!"
		return -1

