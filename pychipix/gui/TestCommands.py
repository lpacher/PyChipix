
#----------------------------------------------------------------------------------------------------
#                                        VLSI Design Laboratory
#                               Istituto Nazionale di Fisica Nucleare (INFN)
#                                   via Giuria 1 10125, Torino, Italy
#----------------------------------------------------------------------------------------------------
# {Trace}
# [Filename]      TestCommands.py [CLASS]
# [Project]       CHIPIX65 demonstrator PyROOT-based DAQ
# [Author]        Luca Pacher - pacher@to.infn.it
# [Version]       1.0
# [Language]      Python/ROOT
# [Created]       Aug 5, 2017
# [Description]   TestCommands GUI class
# [Notes]         -
# {Trace}
#----------------------------------------------------------------------------------------------------

import time

## import ROOT components
import ROOT

## custom classes
from CommonFrames import MenuBar, ConnectionFrame
from CommonFrames import GcrReadFrame, GcrWriteFrame
from CommonFrames import EccrReadFrame, EccrWriteFrame
from CommonFrames import PcrReadFrame, PcrWriteFrame, PcrWriteDefaultsFrame 

import tasks

from typedef import *


###########################
##   FPGA-tab subclass   ##
###########################

class FpgaTab(ROOT.TGCompositeFrame) :

	##________________________________________________________________________________
	def __init__(self, parent) :

		parent.ChangeOptions(ROOT.kHorizontalFrame)

		self.fFpgaTabVerticalFrames = [] 

		self.fFpgaTabVerticalFrames.append(ROOT.TGVerticalFrame(parent, 0, 0, ROOT.kChildFrame))
		self.fFpgaTabVerticalFrames.append(ROOT.TGVerticalFrame(parent, 0, 0, ROOT.kChildFrame))
		self.fFpgaTabVerticalFrames.append(ROOT.TGVerticalFrame(parent, 0, 0, ROOT.kChildFrame))
		self.fFpgaTabVerticalFrames.append(ROOT.TGVerticalFrame(parent, 0, 0, ROOT.kChildFrame))


		##########################
		##   left-most frame    ##
		##########################

		self.fResetFpgaCountersButton       = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[0], "Reset FPGA counters")
		self.fResetAsicButton               = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[0], "Reset CHIPIX")
		self.fSetTxDataAlignEnableButton    = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[0], "Set TX data align-enable")
		self.fSynchronizeTx8b10bButton      = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[0], "Synchronize TX 8b/10b")
		self.fRead8b10bErrorCountersButton  = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[0], "Read 8b/10b error counters")
		self.fSetTxDataEnableButton         = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[0], "Set TX data enable")
		self.fReadTxFifoFullCounterButton   = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[0], "Read TX FIFO full counter")
		self.fSetScanModeButton             = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[0], "Set scan-mode")
		self.fSetPixelRegionDebugButton     = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[0], "Set pixel-region debug")
		self.fSetAutoZeroingModeButton      = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[0], "Set autozeroing mode")
		#self.fReadAdcButton                 = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[0], "Read ADC")

		self.fResetFpgaCountersButton.SetMargins(10 ,10, 1, 1)
		self.fResetAsicButton.SetMargins(10 ,10, 1, 1)
		self.fSetTxDataAlignEnableButton.SetMargins(10, 10, 1, 1)
		self.fSynchronizeTx8b10bButton.SetMargins(10, 10, 1, 1)
		self.fRead8b10bErrorCountersButton.SetMargins(10, 10, 1, 1)
		self.fSetTxDataEnableButton.SetMargins(10, 10, 1, 1)
		self.fReadTxFifoFullCounterButton.SetMargins(10, 10, 1, 1)
		self.fSetScanModeButton .SetMargins(10, 10, 1, 1)
		self.fSetPixelRegionDebugButton.SetMargins(10, 10, 1, 1)
		self.fSetAutoZeroingModeButton.SetMargins(10, 10, 1, 1)

		self.fFpgaTabVerticalFrames[0].AddFrame(self.fResetFpgaCountersButton,      ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[0].AddFrame(self.fResetAsicButton,              ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[0].AddFrame(self.fSetTxDataAlignEnableButton,   ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[0].AddFrame(self.fSynchronizeTx8b10bButton,     ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[0].AddFrame(self.fRead8b10bErrorCountersButton, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[0].AddFrame(self.fSetTxDataEnableButton,        ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0)) 
		self.fFpgaTabVerticalFrames[0].AddFrame(self.fReadTxFifoFullCounterButton,  ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[0].AddFrame(self.fSetScanModeButton,            ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[0].AddFrame(self.fSetPixelRegionDebugButton,    ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[0].AddFrame(self.fSetAutoZeroingModeButton,     ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0)) 



		###########################
		##   middle-left frame   ##
		###########################

		self.fTxDataAlignEnable = ROOT.TGCheckButton(self.fFpgaTabVerticalFrames[1], "TX data-align enable")
		self.fSyncOk            = ROOT.TGCheckButton(self.fFpgaTabVerticalFrames[1], "Sync OK")
		self.fTxDataEnable      = ROOT.TGCheckButton(self.fFpgaTabVerticalFrames[1], "TX data enable")
		self.fScanModeEnable    = ROOT.TGCheckButton(self.fFpgaTabVerticalFrames[1], "Scan mode enable")
		self.fDebugEnable       = ROOT.TGCheckButton(self.fFpgaTabVerticalFrames[1], "Pixel debug enable")
		self.AutozeroingEnable  = ROOT.TGCheckButton(self.fFpgaTabVerticalFrames[1], "Autozeroing enable")

		self.fFpgaTabVerticalFrames[1].AddFrame(self.fTxDataAlignEnable, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[1].AddFrame(self.fSyncOk,            ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[1].AddFrame(self.fTxDataEnable,      ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[1].AddFrame(self.fScanModeEnable,    ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[1].AddFrame(self.fDebugEnable,       ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[1].AddFrame(self.AutozeroingEnable,  ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))



		############################
		##   middle-right frame   ##
		############################

		self.fResetClkCountersButton     = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[2], "Reset clock counters")
		self.fSetBoardLinesButton        = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[2], "Set board lines")
		self.fWaitDelayButton            = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[2], "Wait delay")
		self.fReadTxFifoDataCountButton  = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[2], "Read TX data FIFO data count")
		self.fReadTxFifoButton           = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[2], "Read TX FIFO")
		self.fReadTxFifoCountMaxButton   = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[2], "Read TX FIFO count max.")
		self.fFlushTxFifoButton          = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[2], "Flush TX FIFO")
		self.fFlushEventsButton          = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[2], "Flush events")

		self.fResetClkCountersButton.SetMargins(10, 10, 1, 1)
		self.fSetBoardLinesButton.SetMargins(10, 10, 1, 1)
		self.fWaitDelayButton.SetMargins(10, 10, 1, 1)
		self.fReadTxFifoDataCountButton.SetMargins(10, 10, 1, 1)
		self.fReadTxFifoButton.SetMargins(10, 10, 1, 1)
		self.fReadTxFifoCountMaxButton.SetMargins(10, 10, 1, 1)
		self.fFlushTxFifoButton.SetMargins(10, 10, 1, 1)
		self.fFlushEventsButton.SetMargins(10, 10, 1, 1)


		self.fFpgaTabVerticalFrames[2].AddFrame(self.fResetClkCountersButton,    ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[2].AddFrame(self.fSetBoardLinesButton,       ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[2].AddFrame(self.fWaitDelayButton,           ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[2].AddFrame(self.fReadTxFifoDataCountButton, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[2].AddFrame(self.fReadTxFifoButton,          ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[2].AddFrame(self.fReadTxFifoCountMaxButton,  ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[2].AddFrame(self.fFlushTxFifoButton,         ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))
		self.fFpgaTabVerticalFrames[2].AddFrame(self.fFlushEventsButton,         ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0))


		##########################
		##   right-most frame   ##
		##########################


		#self.WaitDelayLabel = ROOT.TGLabel(self.fFpgaTabVerticalFrames[3], "Delay (ms)")
		self.WaitDelayFrame = ROOT.TGGroupFrame(self.fFpgaTabVerticalFrames[3], "Delay (ms)")

		self.WaitDelayEntry = ROOT.TGNumberEntry(
			self.fFpgaTabVerticalFrames[3], 0, 10, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 1000)

		self.WaitDelayFrame.AddFrame(self.WaitDelayEntry, ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 10, 10, 20, 10))

		self.fFpgaTabVerticalFrames[3].AddFrame(self.WaitDelayFrame, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 20, 0)) 

		#self.fFpgaTabVerticalFrames[3].AddFrame(
		#self.fFpgaTabVerticalFrames[3].AddFrame(

		parent.AddFrame(self.fFpgaTabVerticalFrames[0], ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 10, 30, 20, 10))
		parent.AddFrame(self.fFpgaTabVerticalFrames[1], ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 20, 30, 20, 10))
		parent.AddFrame(self.fFpgaTabVerticalFrames[2], ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 20, 30, 20, 10))
		parent.AddFrame(self.fFpgaTabVerticalFrames[3], ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 20, 30, 20, 10))



##########################
##   SPI-tab subclass   ##
##########################

class SpiTab(ROOT.TGCompositeFrame) :

	##________________________________________________________________________________
	def __init__(self, parent) :

		parent.ChangeOptions(ROOT.kHorizontalFrame)

		self.fSpiTabVerticalFrames = [] 

		self.fSpiTabVerticalFrames.append(ROOT.TGVerticalFrame(parent, 0, 0, ROOT.kChildFrame))
		self.fSpiTabVerticalFrames.append(ROOT.TGVerticalFrame(parent, 0, 0, ROOT.kChildFrame))
		self.fSpiTabVerticalFrames.append(ROOT.TGVerticalFrame(parent, 0, 0, ROOT.kChildFrame))
		self.fSpiTabVerticalFrames.append(ROOT.TGVerticalFrame(parent, 0, 0, ROOT.kChildFrame))

		##########################
		##   left-most frame    ##
		##########################

		self.fSetSpiSerialOffsetButton = ROOT.TGTextButton(self.fSpiTabVerticalFrames[0], "Set SPI serial offset") ;   self.fSetSpiSerialOffsetButton.SetMargins(10, 10, 1, 1)
		self.fSendSpiFrameButton       = ROOT.TGTextButton(self.fSpiTabVerticalFrames[0], "Send SPI frame") ;          self.fSendSpiFrameButton.SetMargins(10, 10, 1, 1)
		self.fReadSpiReplyButton       = ROOT.TGTextButton(self.fSpiTabVerticalFrames[0], "Read SPI reply") ;          self.fReadSpiReplyButton.SetMargins(10, 10, 1, 1)
		self.fSetSpiRamAddress         = ROOT.TGTextButton(self.fSpiTabVerticalFrames[0], "Set SPI RAM address") ;     self.fSetSpiRamAddress.SetMargins(10, 10, 1, 1)
		self.fWriteSpiCommandRamButton = ROOT.TGTextButton(self.fSpiTabVerticalFrames[0], "Write SPI command RAM") ;   self.fWriteSpiCommandRamButton.SetMargins(10, 10, 1, 1)
		self.fRunSpiSequenceButton     = ROOT.TGTextButton(self.fSpiTabVerticalFrames[0], "Run SPI sequence") ;        self.fRunSpiSequenceButton.SetMargins(10, 10, 1, 1)
		self.fReadSpiReplyRamButton    = ROOT.TGTextButton(self.fSpiTabVerticalFrames[0], "Read SPI reply RAM") ;      self.fReadSpiReplyRamButton.SetMargins(10, 10, 1, 1)
		self.fProgramSpiSequenceButton = ROOT.TGTextButton(self.fSpiTabVerticalFrames[0], "Program SPI sequence") ;    self.fProgramSpiSequenceButton.SetMargins(10, 10, 1, 1)


		self.fSpiTabVerticalFrames[0].AddFrame(self.fSetSpiSerialOffsetButton, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5,  20, 0))
		self.fSpiTabVerticalFrames[0].AddFrame(self.fSendSpiFrameButton,       ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5,  35, 0))
		self.fSpiTabVerticalFrames[0].AddFrame(self.fReadSpiReplyButton,       ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5,  35, 0))
		self.fSpiTabVerticalFrames[0].AddFrame(self.fSetSpiRamAddress,         ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5,  40, 0))
		self.fSpiTabVerticalFrames[0].AddFrame(self.fWriteSpiCommandRamButton, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5,  40, 0))
		self.fSpiTabVerticalFrames[0].AddFrame(self.fRunSpiSequenceButton,     ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5,  40, 0))
		self.fSpiTabVerticalFrames[0].AddFrame(self.fReadSpiReplyRamButton,    ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 100, 0))
		self.fSpiTabVerticalFrames[0].AddFrame(self.fProgramSpiSequenceButton, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5,  40, 0))


		###########################
		##   middle-left frame   ##
		###########################

		self.fSpiSerialOffsetEnable = ROOT.TGCheckButton(self.fSpiTabVerticalFrames[1], "SPI serial offset")

		self.fSpiFrameLabel                   = ROOT.TGLabel(self.fSpiTabVerticalFrames[1], "SPI hex frame")
		self.fSpiReplyLabel                   = ROOT.TGLabel(self.fSpiTabVerticalFrames[1], "SPI reply frame")
		self.fSpiRamAddressLabel              = ROOT.TGLabel(self.fSpiTabVerticalFrames[1], "SPI RAM address")
		self.fSpiCommandRamDataLabel          = ROOT.TGLabel(self.fSpiTabVerticalFrames[1], "SPI frame RAM data")
		self.fSpiSequenceRamStartAddressLabel = ROOT.TGLabel(self.fSpiTabVerticalFrames[1], "SPI sequence RAM start-address")
		self.fSpiSequenceRamEndAddressLabel   = ROOT.TGLabel(self.fSpiTabVerticalFrames[1], "SPI sequence RAM end-address")
		self.fSpiReplyRamDataLabel            = ROOT.TGLabel(self.fSpiTabVerticalFrames[1], "SPI reply RAM data")
		self.fSpiSequenceLabel                = ROOT.TGLabel(self.fSpiTabVerticalFrames[1], "SPI sequence")

		self.fSpiFrameEntry = ROOT.TGNumberEntry(
			self.fSpiTabVerticalFrames[1], int(0xF0000), 9, -1,
			ROOT.TGNumberFormat.kNESHex,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**20 -1))

		self.fSpiRamAddressEntry = ROOT.TGNumberEntry(
			self.fSpiTabVerticalFrames[1], 0, 9, -1,
			ROOT.TGNumberFormat.kNESHex,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**20 -1))

		self.fSpiCommandRamDataEntry = ROOT.TGNumberEntry(
			self.fSpiTabVerticalFrames[1], 0, 9, -1,
			ROOT.TGNumberFormat.kNESHex,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**20 -1))

		self.fSpiSequenceRamStartAddressEntry = ROOT.TGNumberEntry(
			self.fSpiTabVerticalFrames[1], 0, 9, -1,
			ROOT.TGNumberFormat.kNESHex,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**20 -1))

		self.fSpiSequenceRamEndAddressEntry = ROOT.TGNumberEntry(
			self.fSpiTabVerticalFrames[1], 0, 9, -1,
			ROOT.TGNumberFormat.kNESHex,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**20 -1))

		self.fSpiSequenceEntry = []

		self.fSpiSequenceEntry.append(ROOT.TGNumberEntry(
			self.fSpiTabVerticalFrames[1], 0, 9, -1,
			ROOT.TGNumberFormat.kNESHex,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**20 -1)))

		self.fSpiSequenceEntry.append(ROOT.TGNumberEntry(
			self.fSpiTabVerticalFrames[1], 0, 9, -1,
			ROOT.TGNumberFormat.kNESHex,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**20 -1)))

		self.fSpiSequenceEntry.append(ROOT.TGNumberEntry(
			self.fSpiTabVerticalFrames[1], 0, 9, -1,
			ROOT.TGNumberFormat.kNESHex,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**20 -1)))

		self.fSpiSequenceEntry.append(ROOT.TGNumberEntry(
			self.fSpiTabVerticalFrames[1], 0, 9, -1,
			ROOT.TGNumberFormat.kNESHex,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**20 -1)))

		## by default, disable entries
		self.fSpiSequenceEntry[0].SetState(ROOT.kTRUE)
		self.fSpiSequenceEntry[1].SetState(ROOT.kFALSE)
		self.fSpiSequenceEntry[2].SetState(ROOT.kFALSE)
		self.fSpiSequenceEntry[3].SetState(ROOT.kFALSE)

		self.fSpiReplyText = ROOT.TGTextEntry(self.fSpiTabVerticalFrames[1])
		self.fSpiReplyRamDataText = ROOT.TGTextEntry(self.fSpiTabVerticalFrames[1])


		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiSerialOffsetEnable,           ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 22, 0))

		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiFrameLabel,                   ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 20, 0))
		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiFrameEntry,                   ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 50,  5, 0))

		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiReplyLabel,                   ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 20, 0))
		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiReplyText,                    ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 50,  5, 0))

		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiRamAddressLabel,              ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 20, 0))
		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiRamAddressEntry,              ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 50,  5, 0))

		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiCommandRamDataLabel,          ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 20, 0))
		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiCommandRamDataEntry,          ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 50,  5, 0))

		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiSequenceRamStartAddressLabel, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 20, 0))
		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiSequenceRamStartAddressEntry, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 50,  5, 0))

		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiSequenceRamEndAddressLabel,   ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 20, 0))
		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiSequenceRamEndAddressEntry,   ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 50,  5, 0))

		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiReplyRamDataLabel,            ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 20, 0))
		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiReplyRamDataText,             ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 50,  5, 0))

		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiSequenceLabel,                ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 20, 0))
		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiSequenceEntry[0],             ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 50,  5, 0))
		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiSequenceEntry[1],             ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 50,  5, 0))
		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiSequenceEntry[2],             ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 50,  5, 0))
		self.fSpiTabVerticalFrames[1].AddFrame(self.fSpiSequenceEntry[3],             ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 50,  5, 0))

		parent.AddFrame(self.fSpiTabVerticalFrames[0], ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 10, 10, 10, 10))
		parent.AddFrame(self.fSpiTabVerticalFrames[1], ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 30, 10, 10, 10))
		parent.AddFrame(self.fSpiTabVerticalFrames[2], ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 10, 10, 10, 10))
		parent.AddFrame(self.fSpiTabVerticalFrames[3], ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 10, 10, 10, 10))



##########################
##   GCR-tab subclass   ##
##########################

"""
Class Reference:

GcrTab(parent) - constructor
DoReadGcr()
DoWriteGcr()
DoWriteGcrDefaults()
"""

class GcrTab(ROOT.TGCompositeFrame) :

	##________________________________________________________________________________
	def __init__(self, parent) :

		parent.ChangeOptions(ROOT.kVerticalFrame)

		## "read" section
		self.fGcrReadButton = ROOT.TGTextButton(parent, "Read GCR") ;   self.fGcrReadButton.SetMargins(10, 10, 1, 1)
		self.fGcrReadFrame = GcrReadFrame(parent)

		## "write" section
		self.fGcrWriteButton = ROOT.TGTextButton(parent, "Write GCR") ;   self.fGcrWriteButton.SetMargins(11, 11, 1, 1)
		self.fGcrWriteFrame = GcrWriteFrame(parent)
		self.fGcrWriteDefaultsButton = ROOT.TGTextButton(parent, "Write GCR defaults") ;   self.fGcrWriteDefaultsButton.SetMargins(11, 11, 1, 1)

		## frame insertion
		parent.AddFrame(self.fGcrReadButton,          ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 20, 10,  40, 0))
		parent.AddFrame(self.fGcrReadFrame,           ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 20, 10,  10, 0))
		parent.AddFrame(self.fGcrWriteButton,         ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 20, 10,  40, 0))
		parent.AddFrame(self.fGcrWriteFrame,          ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 20, 10,  10, 0))
		parent.AddFrame(self.fGcrWriteDefaultsButton, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 20, 10,  40, 0))

		self.DoReadGcrDispatcher          = ROOT.TPyDispatcher(self.DoReadGcr)
		self.DoWriteGcrDispatcher         = ROOT.TPyDispatcher(self.DoWriteGcr)
		self.DoWriteGcrDefaultsDispatcher = ROOT.TPyDispatcher(self.DoWriteGcrDefaults)

		self.fGcrReadButton.Connect("Clicked()", "TPyDispatcher", self.DoReadGcrDispatcher, "Dispatch()")
		self.fGcrWriteButton.Connect("Clicked()", "TPyDispatcher", self.DoWriteGcrDispatcher, "Dispatch()")
		self.fGcrWriteDefaultsButton.Connect("Clicked()", "TPyDispatcher", self.DoWriteGcrDefaultsDispatcher, "Dispatch()")


	##________________________________________________________________________________
	def DoReadGcr(self) :
		if __debug__ :

			print "'Read GCR' button pressed"

		else :

			r = tasks.readGCR()
			r.PrintParameters()
			self.fGcrReadFrame.SetGcrValues(r)


	##________________________________________________________________________________
	def DoWriteGcr(self) :
		if __debug__ :

			print "'Write GCR' button pressed"
			print self.fGcrWriteFrame.GetGcrValues()

		else :

			## get GCR values from frame
			p = self.fGcrWriteFrame.GetGcrValues()

			## create GCR object
			r = GCR(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[13], p[14], p[15], p[16], p[17], p[18], p[19], p[20], p[21], p[22], p[23], p[24], p[25], p[26])

			## write GCR
			tasks.writeGCR(r)



	##________________________________________________________________________________
	def DoWriteGcrDefaults(self) :
		if __debug__ :
			print "'Write GCR defaults' button pressed"

		else :
			pass


###########################
##   ECCR-tab subclass   ##
###########################

"""
Class Reference:

EccrTab(parent) - constructor
DoReadEccr()
DoWriteEccr()
DoWriteEccrDefaults()
"""

class EccrTab(ROOT.TGCompositeFrame) :

	##________________________________________________________________________________
	def __init__(self, parent) :

		## "read" section
		self.fEccrReadButton = ROOT.TGTextButton(parent, "Read ECCR") ;   self.fEccrReadButton.SetMargins(10, 10, 1, 1)
		self.fEccrReadFrame = EccrReadFrame(parent)

		## "write" section
		self.fEccrWriteButton = ROOT.TGTextButton(parent, "Write ECCR") ;   self.fEccrWriteButton.SetMargins(11, 11, 1, 1)
		self.fEccrWriteFrame = EccrWriteFrame(parent)

		self.fEccrWriteDefaultsButton = ROOT.TGTextButton(parent, "Write ECCR defaults") ;   self.fEccrWriteDefaultsButton.SetMargins(11, 11, 1, 1)

		## tab frame insertion
		parent.AddFrame(self.fEccrReadButton,          ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 20, 10, 40,  0))
		parent.AddFrame(self.fEccrReadFrame,           ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 20, 10, 10,  0))
		parent.AddFrame(self.fEccrWriteButton,         ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 20, 10, 30, 10))
		parent.AddFrame(self.fEccrWriteFrame,          ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 20, 10, 10,  0))
		parent.AddFrame(self.fEccrWriteDefaultsButton, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 20, 10, 40,  0))


		self.DoReadEccrDispatcher          = ROOT.TPyDispatcher(self.DoReadEccr)
		self.DoWriteEccrDispatcher         = ROOT.TPyDispatcher(self.DoWriteEccr)
		self.DoWriteEccrDefaultsDispatcher = ROOT.TPyDispatcher(self.DoWriteEccrDefaults)

		self.fEccrReadButton.Connect("Clicked()", "TPyDispatcher", self.DoReadEccrDispatcher, "Dispatch()")
		self.fEccrWriteButton.Connect("Clicked()", "TPyDispatcher", self.DoWriteEccrDispatcher, "Dispatch()")
		self.fEccrWriteDefaultsButton.Connect("Clicked()", "TPyDispatcher", self.DoWriteEccrDefaultsDispatcher, "Dispatch()")


	##________________________________________________________________________________
	def DoReadEccr(self) :
		if __debug__ :
			print "'Read ECCR' button pressed"
			self.fEccrReadFrame.dbgSetEccrResetValues()

		else :
			pass


	##________________________________________________________________________________
	def DoWriteEccr(self) :
		if __debug__ :
			print "'Write ECCR' button pressed"
			print self.fEccrWriteFrame.GetEccrValues()

		else :

			## get ECCR values from frame
			self.fEccrWriteFrame.GetEccrValues()


	##________________________________________________________________________________
	def DoWriteEccrDefaults(self) :
		if __debug__ :
			print "'Write ECCR defaults' button pressed"

		else :
			pass


##########################
##   PCR-tab subclass   ##
##########################

"""
Class Reference:

PcrTab(parent) - constructor
DoReadPcr()
DoWritePcr()
DoWritePcrDefaults()
"""

class PcrTab(ROOT.TGCompositeFrame) :

	##________________________________________________________________________________
	def __init__(self, parent) :

		#parent.ChangeOptions(ROOT.kHorizontalFrame)

		## "read" section
		self.fPcrReadButton = ROOT.TGTextButton(parent, "Read PCR") ;   self.fPcrReadButton.SetMargins(10, 10, 1, 1)
		self.fPcrReadFrame = PcrReadFrame(parent)

		## "write" section
		self.fPcrWriteButton = ROOT.TGTextButton(parent, "Write PCR") ;   self.fPcrWriteButton.SetMargins(11, 11, 1, 1)
		self.fPcrWriteFrame = PcrWriteFrame(parent)

		self.fPcrWriteDefaultsButton = ROOT.TGTextButton(parent, "Write PCR defaults") ;   self.fPcrWriteDefaultsButton.SetMargins(11, 11, 1, 1)
		self.fPcrWriteDefaultsFrame = PcrWriteDefaultsFrame(parent)

		## tab frame insertion
		parent.AddFrame(self.fPcrReadButton,          ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 20, 10, 20, 0))
		parent.AddFrame(self.fPcrReadFrame,           ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 20, 10, 10, 0))
		parent.AddFrame(self.fPcrWriteButton,         ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 20, 10, 10, 0))
		parent.AddFrame(self.fPcrWriteFrame,          ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 20, 10, 10, 0))
		parent.AddFrame(self.fPcrWriteDefaultsButton, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 20, 10, 20, 0))
		parent.AddFrame(self.fPcrWriteDefaultsFrame,  ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 20, 10, 10, 0))

		self.DoReadPcrDispatcher  = ROOT.TPyDispatcher(self.DoReadPcr)
		self.DoWritePcrDispatcher = ROOT.TPyDispatcher(self.DoWritePcr)
		self.DoWritePcrDefaultsDispatcher = ROOT.TPyDispatcher(self.DoWritePcrDefaults)

		self.fPcrReadButton.Connect("Clicked()", "TPyDispatcher", self.DoReadPcrDispatcher, "Dispatch()")
		self.fPcrWriteButton.Connect("Clicked()", "TPyDispatcher", self.DoWritePcrDispatcher, "Dispatch()")
		self.fPcrWriteDefaultsButton.Connect("Clicked()", "TPyDispatcher", self.DoWritePcrDefaultsDispatcher, "Dispatch()")


	##________________________________________________________________________________
	def DoReadPcr(self) :
		if __debug__ :
			print "'Read PCR' button pressed"
		pass


	##________________________________________________________________________________
	def DoWritePcr(self) :
		if __debug__ :
			print "'Write PCR' button pressed"
		
		self.fPcrWriteFrame.GetPcrValues()


	##________________________________________________________________________________
	def DoWritePcrDefaults(self) :
		if __debug__ :
			print "'Write PCR defaults' button pressed"
		pass



##########################
##   ADC-tab subclass   ##
##########################

"""
Class Reference:

AdcTab(parent) - constructor
DoReadAdc()
DoDisplayAdcCode(id)
GetAdcEocDelay()
SetAdcCode()
"""

class AdcTab(ROOT.TGCompositeFrame) :

	##________________________________________________________________________________
	def __init__(self, parent) :

		parent.ChangeOptions(ROOT.kHorizontalFrame)

		self.fReadAdcButton = ROOT.TGTextButton(parent, "Read ADC")
		self.fReadAdcButton.SetMargins(10, 10, 1, 1)

		## ADC EOC delay in terms of FPGA clock cycles (uses a 20-bit internal counter)
		self.fAdcEocDelayLabel = ROOT.TGLabel(parent, "ADC EOC delay (clock cycles)")

		self.fAdcEocDelayEntry = ROOT.TGNumberEntry(
			parent, 99999, 10, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 2**20 -1)

		self.fAdcCodeLabel = ROOT.TGLabel(parent, "Returned ADC code")

		self.fAdcCodeText = ROOT.TGTextEntry(parent)
		#self.fAdcCodeText.SetEnabled(ROOT.kFALSE)
		self.fAdcCodeText.DrawBorder()
		self.fAdcCodeText.SetAlignment(ROOT.kTextRight)
		self.fAdcCodeText.SetMaxLength(6)

		self.fAdcCodeRadixFrame = ROOT.TGButtonGroup(parent, " Radix ", ROOT.kVerticalFrame)

		self.fAdcCodeFormatDec = ROOT.TGRadioButton(self.fAdcCodeRadixFrame, "Dec", 0)
		self.fAdcCodeFormatHex = ROOT.TGRadioButton(self.fAdcCodeRadixFrame, "Hex", 1)

		## default state
		#self.fAdcCodeFormatDec.SetState(ROOT.kButtonDown)
		self.fAdcCodeRadixFrame.SetButton(0)

		parent.AddFrame(self.fReadAdcButton,     ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 15,  50, 40,  0)) 
		parent.AddFrame(self.fAdcEocDelayLabel,  ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10,  10, 43,  0)) 
		parent.AddFrame(self.fAdcEocDelayEntry,  ROOT.TGLayoutHints(ROOT.kLHintsNoHints,  5,  10, 40,  0))
		parent.AddFrame(self.fAdcCodeLabel,      ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 35,  10, 43, 10))
		parent.AddFrame(self.fAdcCodeText,       ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10,  50, 40, 10))
		parent.AddFrame(self.fAdcCodeRadixFrame, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10,  50, 25, 10))


		##############################################
		##   map buttons to callbacks and actions   ##
		##############################################

		self.DoReadAdcDispatcher = ROOT.TPyDispatcher(self.DoReadAdc)
		self.fReadAdcButton.Connect("Clicked()", "TPyDispatcher", self.DoReadAdcDispatcher, "Dispatch()")

		self.DoDisplayAdcCodeDispatcher = ROOT.TPyDispatcher(self.DoDisplayAdcCode)
		self.fAdcCodeRadixFrame.Connect("Pressed(Int_t)", "TPyDispatcher", self.DoDisplayAdcCodeDispatcher, "Dispatch(Int_t)")


	##________________________________________________________________________________
	def DoReadAdc(self) :

		self.fAdcCodeRadix = ""

		if __debug__ :
			print "'Read ADC' button pressed"
			print "ADC EOC delay value is %d" % self.GetAdcEocDelay()
			self.fAdcCode = ROOT.gRandom.Integer(4096)
			self.SetAdcCode()

		else :

			## get EOC delay from number entry (FPGA clock cycles, 20-bit internal counter)
			self.fAdcCode = tasks.readADC(self.GetAdcEocDelay())

			if(self.fAdcCode != -1) :
				self.SetAdcCode()
			else :
				pass


	##________________________________________________________________________________
	def DoDisplayAdcCode(self, id) :

		s = self.fAdcCodeText.GetText()

		if(s != '') :
			if(id == 0) :
				if( self.fAdcCodeRadix == "hex") :
					self.fAdcCodeRadix = "dec"
					n = int(s, 16)
					self.fAdcCodeText.SetText(str(n))

			elif(id == 1) :
				if( self.fAdcCodeRadix == "dec") :
					self.fAdcCodeRadix = "hex"
					self.fAdcCodeText.SetText("0x" + format(self.fAdcCode, '03x').upper())

			else :
				print "Something wrong..."
		else :
			pass


	##________________________________________________________________________________
	def GetAdcEocDelay(self) :
		return int(self.fAdcEocDelayEntry.GetNumber())


	##________________________________________________________________________________
	def SetAdcCode(self) :

		if(self.fAdcCode != None) :

			## display ADC code according to dec/hex radio button
			if(self.fAdcCodeFormatDec.IsDown()) :
				self.fAdcCodeRadix = "dec"
				self.fAdcCodeText.SetText(str(self.fAdcCode))

			elif(self.fAdcCodeFormatHex.IsDown()) :
				self.fAdcCodeRadix = "hex"
				self.fAdcCodeText.SetText("0x" + format(self.fAdcCode, '03x').upper())

			else :
				print "Something wrong..."

		else :
			pass


#####################################
##   main TestCommands GUI class   ##
#####################################

class TestCommandsGui( ROOT.TGMainFrame ) :

	"""TestCommandsGui class. Used to debug all basic operations."""

	##________________________________________________________________________________
	def __init__( self, w=1600, h=950) :

		"""constructor"""

		## window size
		self.fWidth  = w
		self.fHeight = h

		## create a TGMainFrame top-level window
		ROOT.TGMainFrame.__init__( self, ROOT.gClient.GetRoot(), self.fWidth, self.fHeight, ROOT.kMainFrame|ROOT.kVerticalFrame)

		## turn on automatic cleanup in this frame and and all child frames (hierarchical)
		self.SetCleanup(ROOT.kDeepCleanup)

		## set top-level window name
		self.SetWindowName( "INFN Torino / CHIPIX DEMO - TestCommands" )

		## give the window manager minimum and maximum size hints
		self.SetWMSizeHints(self.fWidth, self.fHeight, self.fWidth, self.fHeight, 1, 1)   ## **NOTE: fixed-size hints

		## set the initial state of the window (either ROOT.kNormalState or ROOT.kIconicState)
		#self.SetWMState(ROOT.kIconicState)
		self.SetWMState(ROOT.kNormalState)

		## connect the 'X' window button to exit
		self.ExitDispatcher = ROOT.TPyDispatcher( self.ExitCallback )
		self.Connect( "CloseWindow()", "TPyDispatcher", self.ExitDispatcher, "Dispatch()" )

		#########################
		##   internal frames   ##
		#########################

		## insert menu bar and common frame (board number, firmware version, etc.)
		self.fMenuBar = MenuBar(self)
		self.fCommonFrame = ConnectionFrame(self)

		## create tabs
		self.fTabsFrame = ROOT.TGTab(self)
		self.fTabsFrame.DrawBorder()

		self.fFpgaTab = FpgaTab (self.fTabsFrame.AddTab("   FPGA   "))
		self.fSpiTab  = SpiTab  (self.fTabsFrame.AddTab("   SPI    "))
		self.fTPTab   =          self.fTabsFrame.AddTab("   TP     ") ;  #TODO
		self.fGcrTab  = GcrTab  (self.fTabsFrame.AddTab("   GCR    "))
		self.fEccrTab = EccrTab (self.fTabsFrame.AddTab("   ECCR   "))
		self.fPcrTab  = PcrTab  (self.fTabsFrame.AddTab("   PCR    "))
		self.fAdcTab  = AdcTab  (self.fTabsFrame.AddTab("   ADC    "))
		self.fPcbTab  =          self.fTabsFrame.AddTab("   PCB    ") ;  #TODO


		#########################################
		##   frame insertion and positioning   ##
		#########################################

		self.AddFrame(self.fMenuBar,     ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 10, 0))
		self.AddFrame(self.fCommonFrame, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 10, 0))
		self.AddFrame(self.fTabsFrame,   ROOT.TGLayoutHints(ROOT.kLHintsExpandX|ROOT.kLHintsExpandY, 10, 10, 15, 10))

		## populate the GUI
		self.MapSubwindows()

		## initialize the layout algorithm via Resize()
		self.Resize( self.GetDefaultSize() )
		
		## pop-up the main frame
		self.MapWindow()
		#self.Resize(self.fWidth, self.fHeight)

		## fixed size
		#self.SetWMSize( self.GetDefaultWidth(), self.GetDefaultHeight() )
		#self.SetWMSizeHints( self.GetDefaultWidth(), self.GetDefaultHeight(), self.GetDefaultWidth(), self.GetDefaultHeight(), 1, 1 )
		#self.SetWMSizeHints(self.fWidth, self.fHeight, self.fWidth, self.fHeight, 1, 1)


	##________________________________________________________________________________
	def __del__( self ) :
		"""destructor"""
		self.Cleanup()
		self.DeleteWindow()


	##________________________________________________________________________________
	def ExitCallback( self ) :
		ROOT.gApplication.Terminate(0)
		raise SystemExit


