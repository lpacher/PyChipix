
#----------------------------------------------------------------------------------------------------
#                                        VLSI Design Laboratory
#                               Istituto Nazionale di Fisica Nucleare (INFN)
#                                   via Giuria 1 10125, Torino, Italy
#
#----------------------------------------------------------------------------------------------------
# {Trace}
# [Filename]      acquisition.py [SCRIPT]
# [Project]       CHIPIX65 pixel ASIC demonstrator
# [Author]        Luca Pacher - pacher@to.infn.it
# [Version]       1.0
# [Language]      Python/ROOT
# [Created]       Oct 17, 2017
# [Description]   First trial to implement free-running data readout from pixels. Will be moved 
#                 into a class. Ref. to CHIPIX_Acquisition.vi for the source code in LabView.
#
# [Notes]         Usage:
#
#                 ./bin/lin/pychipix ./user/scripts/acquisition.py
# {Trace}
#----------------------------------------------------------------------------------------------------


## STL components
#import ... 



## ROOT components
import ROOT

ROOT.gStyle.SetOptStat(0)

ROOT.gStyle.SetCanvasDefH(600)
ROOT.gStyle.SetCanvasDefW(600)


global hMap

hMap = ROOT.TH2F("hMap", "", 64, -0.5, 63.5, 64, -0.5, 63.5)

hMap.Draw("colz")

hMap.GetXaxis().SetNdivisions(64, ROOT.kFALSE)
hMap.GetYaxis().SetNdivisions(64, ROOT.kFALSE)

hMap.GetXaxis().SetLabelSize(0.0)
hMap.GetYaxis().SetLabelSize(0.0)

ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()

ROOT.gStyle.SetGridStyle(0)
ROOT.gStyle.SetGridColor(12)
"""
for i in range(64) :
	for j in range(64) :
		hMap.Fill(i, j, -1)    # just to have a nice blue background for the pixel map
"""
ROOT.gPad.Modified()
ROOT.gPad.Update()


############################
##   binary  utput file   ##
############################


## create a new binary file in writing mode
binFile = open("./output.bin", "wb")


## test histogram

global hPacketSize

hPacketSize = ROOT.TH1F("hPacketSize","", 1200, 0.5, 1200 + 0.5)
hPacketSize.SetXTitle("packet size [Bytes]")
hPacketSize.SetYTitle("entries")


#hPacketSize.Draw()
#ROOT.gPad.SetLogy()


###########################
##   GCR configuration   ##
###########################

## create a new GCR object
gcr = GCR()

## set desired values
gcr.SetParameter( 1,    1)         #   1. TO:  PWM delay   default = 0
gcr.SetParameter( 2,    3)         #   2. TO:  PWM high    default = 20
gcr.SetParameter( 3, 3980)         #   3. TO:  PWM low     default = 3980
gcr.SetParameter( 4,  100)         #   4. TO:  ICTRL_TOT   default = 100
gcr.SetParameter( 5,   65)         #   5. TO:  VTH_DISC    default = 1023
gcr.SetParameter( 6,  450)         #   6. TO:  VBL_DISC    default = 450
gcr.SetParameter( 7,  100)         #   7. TO:  IBIASP1     default = 100
gcr.SetParameter( 8,  150)         #   8. TO:  IBIASP2     default = 150
gcr.SetParameter( 9,  200)         #   9. TO:  IBIAS_DISC  default = 200
gcr.SetParameter(10,  100)         #  10. TO:  IBIAS_SF    default = 100
gcr.SetParameter(11,  490)         #  11. TO:  VREF_KRUM   default = 490
gcr.SetParameter(12,   80)         #  12. TO:  IBIAS_FEED  default = 80
gcr.SetParameter(13,   20)         #  13. GBL: IREF_TRIM   default = 20
gcr.SetParameter(14,    5)         #  14. GBL: BGR_TRIM    default = 5
gcr.SetParameter(15,   16)         #  15. ADC: MON_MUX     default = 16
gcr.SetParameter(16,  160)         #  16. PV:  ILDAC       default = 160
gcr.SetParameter(17, 1023)         #  17. PV:  IGDAC       default = 1023
gcr.SetParameter(18,  300)         #  18. PV:  VREF_KRUM   default = 300
gcr.SetParameter(19,   50)         #  19. PV:  IKRUM       default = 50
gcr.SetParameter(20,  200)         #  20. PV:  IFC_BIAS    default = 200
gcr.SetParameter(21,  300)         #  21. PV:  IPA_IN_BIAS default = 300
gcr.SetParameter(22,    0)         #  22. GBL: CAL_LEVEL   default = 0
gcr.SetParameter(23,    0)         #  23. ADC: MODE        default = 0
gcr.SetParameter(24,    8)         #  24. ADC: GAIN        default = 8
gcr.SetParameter(25,   28)         #  25. ADC: IDISCH      default = 28
gcr.SetParameter(26,   28)         #  26. ADC: ICH         default = 28
gcr.SetParameter(27,   16)         #  27. ADC: VTH         default = 16

gcr.UpdateRegisters()



############################
##   ECCR configuration   ##
############################

## create a new ECCR object
eccr = ECCR()

## set desired values
eccr.SetParameter(1,0)         # 1. Trigger latency            default = 0
eccr.SetParameter(2,0)         # 2. Triggered operations       default = 0
eccr.SetParameter(3,1)         # 3. TOT mode                   default = 0
eccr.SetParameter(4,0)         # 4. High-deadtime mode         default = 0
eccr.SetParameter(5,0)         # 5. Binary timestamp encoding  default = 0
eccr.SetParameter(6,0)         # 6. Disable 88/10b encoding    default = 0
eccr.SetParameter(7,0)         # 7. MCD mask                   default = 0

eccr.UpdateRegisters()


###########################
##   PCR configuration   ##
###########################

## **TODO



####################################
##   TX I/O delay configuration   ##
####################################

txDelay = 0


########################
##   events timeout   ##
########################

eventsTimeoutMilliSeconds = 20


##########################################
##   trigger/test-pulse configuration   ##
##########################################

frameCounterEventEnable = 0

extTriggerEnable = 0
extTriggerTestPulseEnable = 0
extTriggerTestPulseCounterMax = 200

triggerEnable = 0
triggerDelay = 0




######################
##   "Initialize"   ##
######################

## error flags
GCRerror = False
ECCRerror = False
busy = False
SPIerror = False
#
# etc.


## counters
badHeadersCounter = 0
lostPacketsCounter = 0
receivedPacketsCounter = 0
#
# etc.


######################
##   "Init comms"   ##
######################

## create a connection
c = connect()


#packetsHeader = c.GetRemoteEventHeader()
#eventsPort = c.GetRemoteEventsPort()



##############################
##   "Reset and align Tx"   ##
##############################


## reset delay controls
resetDelayControls()


## program TX delay
programTxDelay(txDelay)


## reset chip
resetChip()


## write GCR configuration
writeGCR(gcr)

## write ECCR configuration
writeECCR(eccr)


## start auto-zeroing
#setAutozeroingEnable()    **TODO
sendSpiFrame(0x60000)                  # SPI command 0110 => start-autozeroing


## start serializer synchronization (from SPI)
setTxDataAlignEnable(1)
#sendSpiFrame(0x30000)


## synchronize TX 8b/10b
synchronizeTx8b10b()


## stop serializer synchronization (from SPI)
setTxDataAlignEnable(0)
#sendSpiFrame(0xB0000)


## disable pixel-region debug
setPixelRegionDebugMode(0)


## reset test-pulse serializer
resetTestPulseSerializer()



######################################
##   "Program T01 pixel registers   ##
######################################

## **TODO


######################################
##   "Program T02 pixel registers   ##
######################################

## **TODO



########################################
##   "Program BG/PV pixel registers   ##
########################################

## **TODO



##############################
##   "Prepare for events"   ##
##############################

## set events idle timeout
setEventsIdleTimeout(30000)


## set events max. buffer size
setEventsMaxBufferSize(15)


## reset FPGA counters
resetFpgaCounters()


## reset clock counters
resetClockCounters()


## enable/disable frame-counter event
setFrameCounterEventEnable(frameCounterEventEnable)


## enable/disable external trigger
setExtTriggerEnable(extTriggerEnable, extTriggerTestPulseEnable, extTriggerTestPulseCounterMax)


## flush events
flushEvents()


## enable data transmission
setTxDataEnable(1)



########################
##   "Acquire data"   ##
########################


## create a new dedicated UDP socket for events reception

## create socket (Internet protocol, UDP protocol)
eventsUdpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

eventsTimeoutSeconds = eventsTimeoutMilliSeconds*1e3
eventsUdpSocket.settimeout(eventsTimeoutSeconds)


## bind socket to UDP port
eventsUdpSocket.bind((c.GetLocalAddress(), c.GetRemoteEventsPort()))
#eventsUdpSocket.bind(("192.168.1.1", 10020))


## this is the main event-loop

i = 0

hitCounter = 0

while(i != -1) :

## **DEBUG: just one-event acquisition
#while(i <= 1) :

	try :

		if(i == 0) :

			## enable events transmission from FPGA to PC
			setEventsEnable(1)

			## increment counter
			i += 1


		else :

			## get reply string from FPGA
			replyString = eventsUdpSocket.recvfrom(1200)[0]
			
			## check first 2-Bytes packet header
			packetHeader = replyString[0:2]

			## check 4-Bytes packet number
			packetNumber = int(replyString[2:6].encode("hex"), 16)

			## N-Bytes packet length to be dumped into binary file
			packetSizeBytes = int(replyString[6:8].encode("hex"), 16)

			hPacketSize.Fill(packetSizeBytes)

			## payload data are after the 8-Bytes header
			packetData = replyString[8:packetSizeBytes]     ## => [3c3c03 ... 00] [3c3c03 ... 00] [3c3c03 ... 00] etc.



			## dump string selection to binary file
			eventPacket = replyString[0:packetSizeBytes]

			binFile.write(eventPacket)


			firedPixelRegions = (packetSizeBytes -8)/15


			## **DEBUG
			#print "Packet header: %s" % packetHeader.encode("hex")
			#print "Packet size:   %d" % packetSizeBytes
			#print "Pixel regions: %d" % firedPixelRegions
			#print "Packet data:   %s" % packetData.encode("hex")


			## events
			#s = packetData.encode("hex")

			## split each pixel-region event from k-codes
			l = packetData.split("\x3c\x3c\x03")


			if(len(l) != 0) :

				for word in l[1:] :


					pixelRegionEvent = word[10] + word[9] + word[7] + word[6] + word[4] + word[3] + word[1] + word[0]

			
					pixelRegionEventBinaryString = format(int(pixelRegionEvent.encode("hex"), 16), "064b")

					regionCol = int(pixelRegionEventBinaryString[ 0: 4], 2)
					regionRow = int(pixelRegionEventBinaryString[14:18], 2)
					hitMap    =     pixelRegionEventBinaryString[18:34]

					for i in range(16) :
	
						if(int(hitMap[15-i]) == 1) :
	
							regionPixelRow = i % 4
							regionPixelCol = i / 4

							pixelRow = 4*regionRow + regionPixelRow
							pixelCol = 4*regionCol + regionPixelCol

							hMap.Fill(pixelCol, pixelRow) ; hitCounter += 1

			
			if(hitCounter % 1000 == 0) :
				ROOT.gPad.Modified()
				ROOT.gPad.Update()
			
			## increment counter
			i += 1


	## catch a Ctrl-C interrupt to safely exit from the while loop
	except KeyboardInterrupt :

		i = -1


## close the events UDP socket
eventsUdpSocket.close()



##########################
##   "Disable events"   ##
##########################


## disable data reception from chip to FPGA
setTxDataEnable(0)


## disable events transmission from FPGA to PC
setTxDataEnable(0)


## disable all trigger features
#setExtTriggerEnable(0, 0, 0)        **TODO


## disable frame counter
setFrameCounterEventEnable(0)


## read TX FIFO full
readTxFifoFullCounter()      # **TODO


## get events FIFO max. count
# **TODO


## read GbPhy events lost
# **TODO


## read 8b/10b errors counter
# **TODO







#######################
##   "Close comms"   ##
#######################

## close the connection
disconnect()




######################
##   "Close file"   ##
######################

binFile.close()

