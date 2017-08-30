
#----------------------------------------------------------------------------------------------------
#                                        VLSI Design Laboratory
#                               Istituto Nazionale di Fisica Nucleare (INFN)
#                                   via Giuria 1 10125, Torino, Italy
#----------------------------------------------------------------------------------------------------
# {Trace}
# [Filename]      GbPhy.py [FUNCTIONS]
# [Project]       CHIPIX65 demonstrator PyROOT-based DAQ
# [Author]        Luca Pacher - pacher@to.infn.it
# [Version]       1.0
# [Language]      Python/ROOT
# [Created]       Aug 17, 2017
# [Description]   Collection of functions to create UDP packets according to commands and payload data
# [Notes]         -
# {Trace}
#----------------------------------------------------------------------------------------------------


import binascii


##________________________________________________________________________________
def clamp(N, Nmin, Nmax) :
	"""for a given integer, returns either the number or its min/max permitted values"""
	return max(min(Nmax, N), Nmin)


##________________________________________________________________________________
def ror(x, y) :
	"""bitwise right-rotation, 16-bit max. data width"""
	mask = (2**y) -1
	mask_bits = x & mask
	return (x >> y) | (mask_bits << (16-y))


##________________________________________________________________________________
def rol(x, y) :
	"""bitwise left-rotation, 16-bit max. data width"""
	return ror(x, 16-y)


##________________________________________________________________________________
def phyCommandPacket(phyCommandTarget="", commandCode=0x00, commandData=0x00000000) :
	"""Python implementation of GbPhy_CommandPacket.vi"""

	phyCmdHex = 0x00

	if(phyCommandTarget == "cpu") :
		phyCmdHex = 0x01

	elif(phyCommandTarget == "ethernetStats") :
		phyCmdHex = 0x08

	else :
		pass

	commandPacket = format(phyCmdHex, '02x') + format(clamp(commandCode, 0, 255), '02x') + format(0, '04x') + format(clamp(commandData, 0, 0xffffffff), '08x')

	#return commandPacket
	return binascii.unhexlify(commandPacket)   # automatically add \x escape characters to identify single bytes (characters)


##________________________________________________________________________________
def cpuCommandPacket(cpuCommand="", cpuData=0x00000000) :
	"""Python implementation of GbPhy_CPU_Command.vi"""

	## 8-bit unsigned integer
	cpuCmdHex = 0x00

	if(cpuCommand == "fifoCommand") :
		cpuCmdHex = 0x01

	elif(cpuCommand == "getFirmwareVersion") :
		cpuCmdHex = 0x02

	elif(cpuCommand == "setEventsMaxBufferSize") :
		cpuCmdHex = 0x10

	elif(cpuCommand == "setEventsIdleTimeout") :
		cpuCmdHex = 0x11

	elif(cpuCommand == "getEventsFifoMaxCount") :
		cpuCmdHex = 0x12

	elif(cpuCommand == "setEventsEnable") :
		cpuCmdHex = 0x13

	else :
		pass

	return phyCommandPacket("cpu", cpuCmdHex, cpuData)


##________________________________________________________________________________
def commandPacket(command="", data=0x00000000) :
	"""Python implementation of CHIPIX_Command_Packet.vi"""

	## 16-bit hex command ID
	cmdHex = 0x0000

	if(command == "resetFpgaCounters") :
		cmdHex = 0x0001

	elif(command == "resetChip") :
		cmdHex = 0x0010

	elif(command == "syncTx8b10b") :
		cmdHex = 0x0011

	elif(command == "readTx8b10bErrorCounters") :
		cmdHex = 0x0012

	elif(command == "setTxDataEnable") :
		cmdHex = 0x0013

	elif(command == "setExtTriggerEnable") :
		cmdHex = 0x0014

	elif(command == "setScanMode") :
		cmdHex = 0x0015

	elif(command == "setFastOrMode") :
		cmdHex = 0x0016

	elif(command == "resetTpSerializer") :
		cmdHex = 0x0020

	elif(command == "setTpSequenceAddressMax") :
		cmdHex = 0x0021

	elif(command == "setTpTriggerParameters") :
		cmdHex = 0x0022

	elif(command == "setTpParameters") :
		cmdHex = 0x0023

	elif(command == "doTp") :
		cmdHex = 0x0024

	elif(command == "setAutozeroingMirrorParameters") :
		cmdHex = 0x0025

	elif(command == "resetAutozeroingMirror") :
		cmdHex = 0x0026

	elif(command == "setAutozeroingTpParameters") :
		cmdHex = 0x0027

	elif(command == "doAutozeroingTp") :
		cmdHex = 0x0028

	elif(command == "resetClkCounters") :
		cmdHex = 0x0080

	elif(command == "setBoardLines") :
		cmdHex = 0x0081

	elif(command == "waitDelay") :
		cmdHex = 0x0082

	elif(command == "readTxFifoDataCount") :
		cmdHex = 0x0090

	elif(command == "readTxDataFifo") :
		cmdHex = 0x0091

	elif(command == "flushTxDataFifo") :
		cmdHex = 0x0092

	elif(command == "readTxDataFifoFullCounter") :
		cmdHex = 0x0093

	elif(command == "readTxDataFifoMaxCount") :
		cmdHex = 0x0094

	elif(command == "readTxFifoFullCounter") :
		cmdHex = 0x0095

	elif(command == "readTxFifoMaxCount") :
		cmdHex = 0x0096

	elif(command == "readEventsFifoFullCounter") :
		cmdHex = 0x0097

	elif(command == "doSpiOperation") :
		cmdHex = 0x00A0

	elif(command == "setSpiRamAddress") :
		cmdHex = 0x00A1

	elif(command == "writeSpiCommandRam") :
		cmdHex = 0x00A2

	elif(command == "runSpiSequence") :
		cmdHex = 0x00A3

	elif(command == "readSpiReplyRam") :
		cmdHex = 0x00A4

	elif(command == "setSpiSerialOffset") :
		cmdHex = 0x00A5

	elif(command == "setTpSequenceRamAddress") :
		cmdHex = 0x00B0

	elif(command == "writeTpSequenceRam") :
		cmdHex = 0x00B1

	elif(command == "setFrameCounterEventEnable") :
		cmdHex = 0x00C0

	elif(command == "flushEvents") :
		cmdHex = 0x00C1

	else :
		pass


	"""
	Richard code to build 32-bit CPU data:

	1. rotate-left cmdHex by 4, i.e. add a '0' to the right, e.g. 0x00C1 => 0x0C10) 

	2. rotate-left the constant 0x0004 by 12, i.e. 0x0004 => 0x4000 

	3. bitwise-or together the tho results, e.g. 0x4000 | 0x0C10 = 0x4C10

	4. split 32-bit user data into 16-bit low and 16-bit high slices dataHi and dataLo

	5. remove 12 MSBs from dataHi by and-ing with 0x000F

	6. bitwise-or (3) with stripped dataHi to form packetHi

	7. join together the partial results packetHi and packetLo
	"""

	dataLo = data & 0x0000FFFF
	dataHi = (data >> 16) & 0x0000FFFF
	cmdOr = rol(0x0004, 12) | rol(cmdHex, 4)
	packetHi = cmdOr | (dataHi & 0x000F)
	packetLo = dataLo

	packet = str(format(packetHi, '04x')) + str(format(packetLo, '04x'))
	p = int(packet, 16)

	## brute-force solution, build the CPU data hex string and convert it to integer
	#data = clamp(data, 0, 0xFFFFFFFF) & 0x0FFFFF
	#s = '4' + str(format(cmdHex, '02x')) + str(format(data, '05x'))
	#p = int(s, 16)

	return cpuCommandPacket("fifoCommand", p)



