
#----------------------------------------------------------------------------------------------------
#                                        VLSI Design Laboratory
#                               Istituto Nazionale di Fisica Nucleare (INFN)
#                                   via Giuria 1 10125, Torino, Italy
#----------------------------------------------------------------------------------------------------
# {Trace}
# [Filename]      EventPacket.py [CLASS]
# [Project]       CHIPIX65 demonstrator PyROOT-based DAQ
# [Author]        Luca Pacher - pacher@to.infn.it
# [Version]       1.0
# [Language]      Python/ROOT
# [Created]       Oct 22, 2017
# [Description]   Class for raw UDP event packets
# [Notes]         -
# {Trace}
#----------------------------------------------------------------------------------------------------



############################
##   CLASS: EventPacket   ##
############################

"""
Class Reference:

EventPacket() - constructor
"""


class EventPacket(object) :

	##________________________________________________________________________________
	def __init__(self, replyString="\xdc\xba\x00\x00\x00\x00\x00\x17\x3c\x3c\x03\x01\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00") :

		self.fReplyString = replyString

		## Bytes slices
		self.fPacketHeader    = replyString[0:2]
		self.fPacketNumber    = replyString[2:6]
		self.fPacketSizeBytes = replyString[6:8]
		self.fPacketData      = replyString[8:self.GetPacketSizeBytes()]


	##________________________________________________________________________________
	def GetPacketData(self) :

		return self.fPacketData

	##________________________________________________________________________________
	def GetPacketHeader(self) :

		return self.fPacketHeader

	##________________________________________________________________________________
	def GetPacketNumber(self) :

		return int(self.fPacketNumber.encode("hex"), 16)

	##________________________________________________________________________________
	def GetPacketSizeBytes(self) :

		return int(self.fPacketSizeBytes.encode("hex"), 16)

	##________________________________________________________________________________
	def GetPixelRegionEvents(self, kCode="\x3c\x3c\x03") :

		return self.fPacketData.split(kCode)[1:]

	##________________________________________________________________________________
	def GetReplyString(self) :

		return self.fReplyString



"""end class"""

