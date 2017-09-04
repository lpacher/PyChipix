
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

	def __init__(self, Timestamp=0, PixelNumber=0, TOT=0) :

		self.fTimestamp   = Timestamp
		self.fPixelNumber = PixelNumber
		self.fTOT         = TOT





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
	def SetPixelNumber(selfi, value) :

		self.fPixelNumber = value


	##________________________________________________________________________________
	def SetTimestamp(selfi, value) :

		self.fTimestamp = value


	##________________________________________________________________________________
	def SetTOT(self, value) :

		self.fTOT = value


"""end class"""

