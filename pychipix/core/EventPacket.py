
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
# [Created]       Sep 1, 2017
# [Description]   Class for events from pixels. Implements CHIPIX_EventPacket.ctl
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
	def __init__(self, timestamp=0, pixelNumber=0, tot=0) :

		self.fTimestamp   = timestamp
		self.fPixelNumber = pixelNumber
		self.fTOT         = tot




	##________________________________________________________________________________
	def GetPixelNumber(self) :

		return self.fPixelNumber


	##________________________________________________________________________________
	def GetTimestamp(self) :

		return self.fTimestamp


	##________________________________________________________________________________
	def GetTOT(self) :

		return self.fTOT


	##________________________________________________________________________________
	def SetPixelNumber(selfi, pixelNumberValue) :

		self.fPixelNumber = pixelNumberValue


	##________________________________________________________________________________
	def SetTimestamp(selfi, timestampValue) :

		self.fTimestamp = timestampValue


	##________________________________________________________________________________
	def SetTOT(self, totValue) :

		self.fTOT = totValue


"""end class"""

