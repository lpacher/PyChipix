
#----------------------------------------------------------------------------------------------------
#                                        VLSI Design Laboratory
#                               Istituto Nazionale di Fisica Nucleare (INFN)
#                                   via Giuria 1 10125, Torino, Italy
#----------------------------------------------------------------------------------------------------
# {Trace}
# [Filename]      PixelRegionEventPacket.py [CLASS]
# [Project]       CHIPIX65 demonstrator PyROOT-based DAQ
# [Author]        Luca Pacher - pacher@to.infn.it
# [Version]       1.0
# [Language]      Python/ROOT
# [Created]       Oct 22, 2017
# [Description]   Class for raw region-based data
# [Notes]         -
# {Trace}
#----------------------------------------------------------------------------------------------------



#######################################
##   CLASS: PixelRegionEventPacket   ##
#######################################

"""
Class Reference:

PixelRegionEventPacket() - constructor
"""


class PixelRegionEventPacket(object) :

	##________________________________________________________________________________
	def __init__(self, s="\x0a\x00\x00\x00\x00\x00\x00\xc8\x00\x14\x6d\x00") :

		## reversed-bytes with skipped \x00
		self.fRegionEvent = s[10] + s[9] + s[7] + s[6] + s[4] + s[3] + s[1] + s[0]

		self.fPixelRegionEventBinaryString = format(int(pixelRegionEvent.encode("hex"), 16), "064b")

		regionCol     = int(pixelRegionEventBinaryString[ 0: 4], 2)
		timeStamp = pixelRegionEventBinaryString[ 4:14]
		regionRow     = int(pixelRegionEventBinaryString[14:18], 2)
		hitMap    = pixelRegionEventBinaryString[18:34]
		totData   = pixelRegionEventBinaryString[34:64]

		tot.append(int(pixelRegionEventBinaryString[59:64], 2))
 		tot.append(int(pixelRegionEventBinaryString[54:59], 2))
 		tot.append(int(pixelRegionEventBinaryString[49:54], 2))
 		tot.append(int(pixelRegionEventBinaryString[44:49], 2))
		tot.append(int(pixelRegionEventBinaryString[39:44], 2))
 		tot.append(int(pixelRegionEventBinaryString[34:39], 2))





"""end class"""

