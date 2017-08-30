
#----------------------------------------------------------------------------------------------------
#                                        VLSI Design Laboratory
#                               Istituto Nazionale di Fisica Nucleare (INFN)
#                                   via Giuria 1 10125, Torino, Italy
#----------------------------------------------------------------------------------------------------
# {Trace}
# [Filename]      CommonFrame.py [CLASS COLLECTION]
# [Project]       CHIPIX65 demonstrator PyROOT-based DAQ
# [Author]        Luca Pacher - pacher@to.infn.it
# [Version]       1.0
# [Language]      Python/ROOT
# [Created]       Aug 10, 2017
# [Description]   Collection of common GUI frames (menu bar, connection frame) into classes
# [Notes]         -
# {Trace}
#----------------------------------------------------------------------------------------------------

import os
import ROOT
import socket

import tasks

from GbPhy import *
from connection import Connection


########################
##   CLASS: MenuBar   ##
########################

"""
Class Reference:

MenuBar(parent) - constructor
"""

class MenuBar(ROOT.TGHorizontalFrame) :

	##________________________________________________________________________________
	def __init__(self, parent) :
	
		## create a TGHorizontalFrame to contain the menu bar

		if __debug__ :

			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame|ROOT.kRaisedFrame)
		else :
			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame)

		## menu bar
		self.fMenuBar = ROOT.TGMenuBar(self, 1, 1, ROOT.kChildFrame|ROOT.kHorizontalFrame)


		## "File" menu
		self.fFilePopupMenu    = ROOT.TGPopupMenu(ROOT.gClient.GetRoot())
		self.fEditPopupMenu    = ROOT.TGPopupMenu(ROOT.gClient.GetRoot())
		self.fViewPopupMenu    = ROOT.TGPopupMenu(ROOT.gClient.GetRoot())
		self.fOptionsPopupMenu = ROOT.TGPopupMenu(ROOT.gClient.GetRoot())
		self.fToolsPopupMenu   = ROOT.TGPopupMenu(ROOT.gClient.GetRoot())
		self.fHelpPopupMenu    = ROOT.TGPopupMenu(ROOT.gClient.GetRoot())

		## "Tools" menu
		self.fToolsPopupMenu.AddEntry("TBrowser", 0)
		self.fToolsPopupMenu.AddEntry("Terminal", 0)

		self.fFilePopupMenu.AddEntry("&Open...", 0)
		self.fFilePopupMenu.AddEntry("&Save", 0)
		self.fFilePopupMenu.AddEntry("S&ave as...", 0)
		self.fFilePopupMenu.AddSeparator()
		self.fFilePopupMenu.AddEntry("&Exit", 0)

		self.fMenuBar.AddPopup("&File",    self.fFilePopupMenu,    ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 0, 2, 0, 0))
		self.fMenuBar.AddPopup("&Edit",    self.fEditPopupMenu,    ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 2, 2, 0, 0))
		self.fMenuBar.AddPopup("&View",    self.fViewPopupMenu,    ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 2, 2, 0, 0))
		self.fMenuBar.AddPopup("&Options", self.fOptionsPopupMenu, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 2, 2, 0, 0))
		self.fMenuBar.AddPopup("&Tools",   self.fToolsPopupMenu,   ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 2, 2, 0, 0))
		self.fMenuBar.AddPopup("&Help",    self.fHelpPopupMenu,    ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 2, 2, 0, 0))

		self.AddFrame(self.fMenuBar, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 0, 5, 5, 5))



################################
##   CLASS: ConnectionFrame   ##
################################

"""
Class Reference:

ConnectionFrame(parent) - constructor
DoConnect()
DoDisconnect()
DoExit()
DoPing()
GetBoardNumber()
GetHostIpAddress()
GetTimeoutMilliSeconds()
SetFirmwareVersion()
"""

class ConnectionFrame(ROOT.TGHorizontalFrame) :

	## class-wide variables
	SOCKET = None


	##________________________________________________________________________________
	def __init__(self, parent) :

		## create TGHorizontalFrame to contain board number, firmware version etc.
		if __debug__ :

			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame|ROOT.kRaisedFrame)
		else :
			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame)



		## TGTextButtons
		self.fExitButton       = ROOT.TGTextButton(self, "&Quit"      ) ;   self.fExitButton.SetMargins       (10, 10, 1, 1)
		self.fConnectButton    = ROOT.TGTextButton(self, "&Connect"   ) ;   self.fConnectButton.SetMargins    (15, 15, 1, 1)
		self.fDisconnectButton = ROOT.TGTextButton(self, "&Disconnect") ;   self.fDisconnectButton.SetMargins (10, 10, 1, 1)
		self.fPingButton       = ROOT.TGTextButton(self, "&Ping FPGA" ) ;   self.fPingButton.SetMargins       (15, 15, 1, 1)


		## TGlabels
		self.fHostIpAddressLabel    = ROOT.TGLabel(self, "Host IP address")
		self.fBoardNumberLabel      = ROOT.TGLabel(self, "Board number")
		self.fTimeoutLabel          = ROOT.TGLabel(self, "Timeout (ms)")
		self.fFirmwareVersionLabel  = ROOT.TGLabel(self, "Firmware version")


		## TGTextEntry
		self.fHostIpAddressText = ROOT.TGTextEntry(self, "192.168.1.1")
		self.fHostIpAddressText.SetMaxLength(len("255.255.255.255"))
		self.fHostIpAddressText.SetAlignment(ROOT.kTextRight)

		#print self.fHostIpAddressText.GetDefaultSize().fHeight
		#print self.fHostIpAddressText.GetDefaultSize().fWidth
		self.fHostIpAddressText.SetDefaultSize(100,22)

		## TGNumberEntry
		self.fBoardNumberEntry = ROOT.TGNumberEntry(
			self, 0, 10, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 7)

		self.fTimeoutEntry = ROOT.TGNumberEntry(
			self, 1000, 10, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 10000)

		## **NOTE: the firware version is retrieved **FROM THE FPGA** when the connection is established!
		self.fFirmwareVersionText = ROOT.TGTextEntry(self)
		#self.fFirmwareVersionText.SetText("0") 
		self.fFirmwareVersionText.DrawBorder()
		self.fFirmwareVersionText.SetAlignment(ROOT.kTextRight)
		self.fFirmwareVersionText.SetMaxLength(6)


		self.AddFrame(self.fHostIpAddressLabel,   ROOT.TGLayoutHints(ROOT.kLHintsNoHints,  10,  5, 8, 5))
		self.AddFrame(self.fHostIpAddressText,    ROOT.TGLayoutHints(ROOT.kLHintsNoHints,   5, 15, 5, 5))
		self.AddFrame(self.fBoardNumberLabel,     ROOT.TGLayoutHints(ROOT.kLHintsNoHints,   5,  5, 8, 5))
		self.AddFrame(self.fBoardNumberEntry,     ROOT.TGLayoutHints(ROOT.kLHintsNoHints,   5, 15, 5, 5))
		self.AddFrame(self.fTimeoutLabel,         ROOT.TGLayoutHints(ROOT.kLHintsNoHints,   5,  5, 8, 5))
		self.AddFrame(self.fTimeoutEntry,         ROOT.TGLayoutHints(ROOT.kLHintsNoHints,   5, 15, 5, 5))
		self.AddFrame(self.fFirmwareVersionLabel, ROOT.TGLayoutHints(ROOT.kLHintsNoHints,   5,  5, 8, 5))
		self.AddFrame(self.fFirmwareVersionText,  ROOT.TGLayoutHints(ROOT.kLHintsNoHints,   5, 15, 5, 5))
		self.AddFrame(self.fConnectButton,        ROOT.TGLayoutHints(ROOT.kLHintsNoHints,  50, 10, 5, 5))
		self.AddFrame(self.fDisconnectButton,     ROOT.TGLayoutHints(ROOT.kLHintsNoHints,  10, 10, 5, 5))
		self.AddFrame(self.fPingButton,           ROOT.TGLayoutHints(ROOT.kLHintsNoHints,  10, 10, 5, 5))
		self.AddFrame(self.fExitButton,           ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 300, 10, 5, 5))

		self.DoExitDispatcher       = ROOT.TPyDispatcher(self.DoExit)
		self.DoConnectDispatcher    = ROOT.TPyDispatcher(self.DoConnect)
		self.DoDisconnectDispatcher = ROOT.TPyDispatcher(self.DoDisconnect)
		self.DoPingDispatcher       = ROOT.TPyDispatcher(self.DoPing)

		self.fExitButton.Connect("Clicked()", "TPyDispatcher", self.DoExitDispatcher, "Dispatch()")
		self.fConnectButton.Connect("Clicked()", "TPyDispatcher", self.DoConnectDispatcher, "Dispatch()")
		self.fDisconnectButton.Connect("Clicked()", "TPyDispatcher", self.DoDisconnectDispatcher, "Dispatch()")
		self.fPingButton.Connect("Clicked()", "TPyDispatcher", self.DoPingDispatcher, "Dispatch()")

		Connection.isConnected = 0



	##________________________________________________________________________________
	def DoConnect(self) :

		if __debug__ :
			print "**DEBUG: 'Connect' button pressed"
			self.SetFirmwareVersion("0x0000")
			self.fConnectButton.SetTextColor(250)
			self.fConnectButton.SetText("Connected")

		else :

			if(Connection.isConnected == False) :


				## try to connect
				l = tasks.connect(self.GetHostIpAddress(), self.GetBoardNumber(), self.GetTimeoutMilliSeconds())

				if(l[0] == 1) :

					## when connected, change the status of the button
					self.fConnectButton.SetTextColor(250)
					self.fConnectButton.SetText("Connected")

					## write firmware version as retrieved from FPGA
					self.SetFirmwareVersion(l[1])

				else :
					pass

			## connection already ongoing, do nothing
			else :
				pass


	##________________________________________________________________________________
	def DoDisconnect(self) :
		if __debug__ :
			print "**DEBUG: 'Disconnect' button pressed"

		if(tasks.disconnect()) :

			## clean firmware version entry
			self.fFirmwareVersionText.SetText("")

			## when disconnected, change the status of the button
			self.fConnectButton.SetTextColor(0)
			self.fConnectButton.SetText("Connect")

		else :
			pass


	##________________________________________________________________________________
	def DoExit(self) :
		if __debug__ :
			print "**DEBUG: 'Quit' button pressed"

		tasks.quit()


	##________________________________________________________________________________
	def DoPing(self) :

		if __debug__ :
			print "**DEBUG: 'Ping' button pressed"


		## create dummy connection for ping
		p = Connection(self.GetHostIpAddress(), self.GetBoardNumber(), self.GetTimeoutMilliSeconds())
		p.BoardMapping()

		if(os.name == "nt") :
			os.system("ping -n 4 " + p.fRemoteAddress)

		else :
			os.system("ping -c 4 " + p.fRemoteAddress)


	##________________________________________________________________________________
	def GetBoardNumber(self) :
		return int(self.fBoardNumberEntry.GetNumber())


	##________________________________________________________________________________
	def GetHostIpAddress(self) :
		return self.fHostIpAddressText.GetText()


	##________________________________________________________________________________
	def GetTimeoutMilliSeconds(self) :
		return self.fTimeoutEntry.GetNumber()


	##________________________________________________________________________________
	def SetFirmwareVersion(self, firmwareVersion) :
		self.fFirmwareVersionText.SetText(firmwareVersion)



#############################
##   CLASS: GcrReadFrame   ##
#############################

"""
Class Reference:

GcrReadFrame(parent) - constructor
SetGcrValues(data)
dbgSetGcrResetValues()
"""

class GcrReadFrame(ROOT.TGHorizontalFrame) :

	##________________________________________________________________________________
	def __init__(self, parent) :

		## create TGHorizontalFrame to contain board number, firmware version etc.
		if __debug__ :

			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame|ROOT.kRaisedFrame)
		else :
			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame)


		self.fGcrReadPix1Frame = ROOT.TGGroupFrame(self, " TO pixels bias and auto-zeroing ",    ROOT.kHorizontalFrame)
		self.fGcrReadPix2Frame = ROOT.TGGroupFrame(self, " BG/PV pixels bias ", ROOT.kHorizontalFrame)
		self.fGcrReadBiasFrame = ROOT.TGGroupFrame(self, " Global reference / charge injection",  ROOT.kHorizontalFrame)
		self.fGcrReadAdcFrame  = ROOT.TGGroupFrame(self, " Monitoring / ADC configuration ", ROOT.kHorizontalFrame)

		#################
		##   TO GCRs   ##
		#################
		self.fGcrReadPix1LabelFrameL = ROOT.TGVerticalFrame(self.fGcrReadPix1Frame)
		self.fGcrReadPix1LabelFrameR = ROOT.TGVerticalFrame(self.fGcrReadPix1Frame)

		self.fGcrReadPix1TextFrameL  = ROOT.TGVerticalFrame(self.fGcrReadPix1Frame) 
		self.fGcrReadPix1TextFrameR  = ROOT.TGVerticalFrame(self.fGcrReadPix1Frame)

		self.fGcrReadPix1Labels = []
		self.fGcrReadPix1Text = []

		self.fGcrReadPix1Labels.append(ROOT.TGLabel(self.fGcrReadPix1LabelFrameL, "IBIASP1")) ;     self.fGcrReadPix1Text.append(ROOT.TGTextEntry(self.fGcrReadPix1TextFrameL))
		self.fGcrReadPix1Labels.append(ROOT.TGLabel(self.fGcrReadPix1LabelFrameL, "IBIASP2")) ;     self.fGcrReadPix1Text.append(ROOT.TGTextEntry(self.fGcrReadPix1TextFrameL))
		self.fGcrReadPix1Labels.append(ROOT.TGLabel(self.fGcrReadPix1LabelFrameL, "IBIAS_SF")) ;    self.fGcrReadPix1Text.append(ROOT.TGTextEntry(self.fGcrReadPix1TextFrameL))
		self.fGcrReadPix1Labels.append(ROOT.TGLabel(self.fGcrReadPix1LabelFrameL, "VREF_KRUM")) ;   self.fGcrReadPix1Text.append(ROOT.TGTextEntry(self.fGcrReadPix1TextFrameL))
		self.fGcrReadPix1Labels.append(ROOT.TGLabel(self.fGcrReadPix1LabelFrameL, "IBIAS_FEED")) ;  self.fGcrReadPix1Text.append(ROOT.TGTextEntry(self.fGcrReadPix1TextFrameL))
		self.fGcrReadPix1Labels.append(ROOT.TGLabel(self.fGcrReadPix1LabelFrameL, "IBIAS_DISC")) ;  self.fGcrReadPix1Text.append(ROOT.TGTextEntry(self.fGcrReadPix1TextFrameL))

		self.fGcrReadPix1Labels.append(ROOT.TGLabel(self.fGcrReadPix1LabelFrameR, "VBL_DISC")) ;    self.fGcrReadPix1Text.append(ROOT.TGTextEntry(self.fGcrReadPix1TextFrameR))
		self.fGcrReadPix1Labels.append(ROOT.TGLabel(self.fGcrReadPix1LabelFrameR, "VTH_DISC")) ;    self.fGcrReadPix1Text.append(ROOT.TGTextEntry(self.fGcrReadPix1TextFrameR))
		self.fGcrReadPix1Labels.append(ROOT.TGLabel(self.fGcrReadPix1LabelFrameR, "ICTRL_TOT")) ;   self.fGcrReadPix1Text.append(ROOT.TGTextEntry(self.fGcrReadPix1TextFrameR))
		self.fGcrReadPix1Labels.append(ROOT.TGLabel(self.fGcrReadPix1LabelFrameR, "PWM delay")) ;   self.fGcrReadPix1Text.append(ROOT.TGTextEntry(self.fGcrReadPix1TextFrameR))
		self.fGcrReadPix1Labels.append(ROOT.TGLabel(self.fGcrReadPix1LabelFrameR, "PWM high")) ;    self.fGcrReadPix1Text.append(ROOT.TGTextEntry(self.fGcrReadPix1TextFrameR))
		self.fGcrReadPix1Labels.append(ROOT.TGLabel(self.fGcrReadPix1LabelFrameR, "PWM low")) ;     self.fGcrReadPix1Text.append(ROOT.TGTextEntry(self.fGcrReadPix1TextFrameR))


		for k in range(0, 6) :
			self.fGcrReadPix1Text[k].DrawBorder()
			self.fGcrReadPix1Text[k].SetAlignment(ROOT.kTextRight)
			self.fGcrReadPix1Text[k].SetMaxLength(4)

			self.fGcrReadPix1LabelFrameL.AddFrame(self.fGcrReadPix1Labels[k], ROOT.TGLayoutHints(ROOT.kLHintsLeft,  5, 5, 5, 1))
			self.fGcrReadPix1TextFrameL.AddFrame(self.fGcrReadPix1Text[k],    ROOT.TGLayoutHints(ROOT.kLHintsRight, 5, 5, 0, 0))


		for k in range(6, 12) :
			self.fGcrReadPix1Text[k].DrawBorder()
			self.fGcrReadPix1Text[k].SetAlignment(ROOT.kTextRight)
			self.fGcrReadPix1Text[k].SetMaxLength(4)

			self.fGcrReadPix1LabelFrameR.AddFrame(self.fGcrReadPix1Labels[k], ROOT.TGLayoutHints(ROOT.kLHintsLeft,  5, 5, 5, 1))
			self.fGcrReadPix1TextFrameR.AddFrame(self.fGcrReadPix1Text[k],    ROOT.TGLayoutHints(ROOT.kLHintsRight, 5, 5, 0, 0))


		self.fGcrReadPix1Frame.AddFrame(self.fGcrReadPix1LabelFrameL, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 10, 10, 13, 0))
		self.fGcrReadPix1Frame.AddFrame(self.fGcrReadPix1TextFrameL,  ROOT.TGLayoutHints(ROOT.kLHintsExpandX,  5, 10, 15, 0))
		self.fGcrReadPix1Frame.AddFrame(self.fGcrReadPix1LabelFrameR, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 20, 10, 13, 0))
		self.fGcrReadPix1Frame.AddFrame(self.fGcrReadPix1TextFrameR,  ROOT.TGLayoutHints(ROOT.kLHintsExpandX,  5, 10, 15, 0))


		####################
		##   BG/PV GCRs   ##
		####################

		self.fGcrReadPix2LabelFrame = ROOT.TGVerticalFrame(self.fGcrReadPix2Frame)
		self.fGcrReadPix2TextFrame  = ROOT.TGVerticalFrame(self.fGcrReadPix2Frame) 

		self.fGcrReadPix2Labels = []
		self.fGcrReadPix2Text = []

		self.fGcrReadPix2Labels.append(ROOT.TGLabel(self.fGcrReadPix2LabelFrame, "IPA_IN_BIAS")) ;   self.fGcrReadPix2Text.append(ROOT.TGTextEntry(self.fGcrReadPix2TextFrame))
		self.fGcrReadPix2Labels.append(ROOT.TGLabel(self.fGcrReadPix2LabelFrame, "IFC_BIAS")) ;      self.fGcrReadPix2Text.append(ROOT.TGTextEntry(self.fGcrReadPix2TextFrame))
		self.fGcrReadPix2Labels.append(ROOT.TGLabel(self.fGcrReadPix2LabelFrame, "VREF_KRUM")) ;     self.fGcrReadPix2Text.append(ROOT.TGTextEntry(self.fGcrReadPix2TextFrame))
		self.fGcrReadPix2Labels.append(ROOT.TGLabel(self.fGcrReadPix2LabelFrame, "IKRUM")) ;         self.fGcrReadPix2Text.append(ROOT.TGTextEntry(self.fGcrReadPix2TextFrame))
		self.fGcrReadPix2Labels.append(ROOT.TGLabel(self.fGcrReadPix2LabelFrame, "IGDAC")) ;         self.fGcrReadPix2Text.append(ROOT.TGTextEntry(self.fGcrReadPix2TextFrame))
		self.fGcrReadPix2Labels.append(ROOT.TGLabel(self.fGcrReadPix2LabelFrame, "ILDAC")) ;         self.fGcrReadPix2Text.append(ROOT.TGTextEntry(self.fGcrReadPix2TextFrame))

		for k in range(0, 6) :
			self.fGcrReadPix2Text[k].DrawBorder()
			self.fGcrReadPix2Text[k].SetAlignment(ROOT.kTextRight)
			self.fGcrReadPix2Text[k].SetMaxLength(4)

			self.fGcrReadPix2LabelFrame.AddFrame(self.fGcrReadPix2Labels[k], ROOT.TGLayoutHints(ROOT.kLHintsLeft,  5, 5, 5, 1))
			self.fGcrReadPix2TextFrame.AddFrame(self.fGcrReadPix2Text[k],    ROOT.TGLayoutHints(ROOT.kLHintsRight, 5, 5, 0, 0))

		self.fGcrReadPix2Frame.AddFrame(self.fGcrReadPix2LabelFrame, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 10, 10, 13, 0))
		self.fGcrReadPix2Frame.AddFrame(self.fGcrReadPix2TextFrame,  ROOT.TGLayoutHints(ROOT.kLHintsExpandX,  5, 10, 15, 0))


		#######################
		##   Bias/Cal GCRs   ##
		#######################

		self.fGcrReadBiasLabelFrame = ROOT.TGVerticalFrame(self.fGcrReadBiasFrame)
		self.fGcrReadBiasTextFrame  = ROOT.TGVerticalFrame(self.fGcrReadBiasFrame) 

		self.fGcrReadBiasLabels = []
		self.fGcrReadBiasText = []

		self.fGcrReadBiasLabels.append(ROOT.TGLabel(self.fGcrReadBiasLabelFrame, "Bandgap")) ;    self.fGcrReadBiasText.append(ROOT.TGTextEntry(self.fGcrReadBiasTextFrame))
		self.fGcrReadBiasLabels.append(ROOT.TGLabel(self.fGcrReadBiasLabelFrame, "IREF trim")) ;  self.fGcrReadBiasText.append(ROOT.TGTextEntry(self.fGcrReadBiasTextFrame))
		self.fGcrReadBiasLabels.append(ROOT.TGLabel(self.fGcrReadBiasLabelFrame, "CAL")) ;        self.fGcrReadBiasText.append(ROOT.TGTextEntry(self.fGcrReadBiasTextFrame))


		for k in range(0, 3) :
			self.fGcrReadBiasText[k].DrawBorder()
			self.fGcrReadBiasText[k].SetAlignment(ROOT.kTextRight)
			self.fGcrReadBiasText[k].SetMaxLength(4)

			self.fGcrReadBiasLabelFrame.AddFrame(self.fGcrReadBiasLabels[k], ROOT.TGLayoutHints(ROOT.kLHintsLeft,  5, 5, 5, 1))
			self.fGcrReadBiasTextFrame.AddFrame(self.fGcrReadBiasText[k],    ROOT.TGLayoutHints(ROOT.kLHintsRight, 0, 0, 0, 0))


		self.fGcrReadBiasFrame.AddFrame(self.fGcrReadBiasLabelFrame, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 10, 10, 13, 0))
		self.fGcrReadBiasFrame.AddFrame(self.fGcrReadBiasTextFrame,  ROOT.TGLayoutHints(ROOT.kLHintsExpandX,  5, 10, 15, 0))



		##################
		##   ADC GCRs   ##
		##################

		self.fGcrReadAdcLabelFrame = ROOT.TGVerticalFrame(self.fGcrReadAdcFrame)
		self.fGcrReadAdcTextFrame  = ROOT.TGVerticalFrame(self.fGcrReadAdcFrame) 

		self.fGcrReadAdcLabels = []
		self.fGcrReadAdcText = []

		self.fGcrReadAdcLabels.append(ROOT.TGLabel(self.fGcrReadAdcLabelFrame, "MON_MUX")) ;      self.fGcrReadAdcText.append(ROOT.TGTextEntry(self.fGcrReadAdcTextFrame))
		self.fGcrReadAdcLabels.append(ROOT.TGLabel(self.fGcrReadAdcLabelFrame, "MODE")) ;         self.fGcrReadAdcText.append(ROOT.TGTextEntry(self.fGcrReadAdcTextFrame))
		self.fGcrReadAdcLabels.append(ROOT.TGLabel(self.fGcrReadAdcLabelFrame, "gm gain")) ;      self.fGcrReadAdcText.append(ROOT.TGTextEntry(self.fGcrReadAdcTextFrame))
		self.fGcrReadAdcLabels.append(ROOT.TGLabel(self.fGcrReadAdcLabelFrame, "Icharge")) ;      self.fGcrReadAdcText.append(ROOT.TGTextEntry(self.fGcrReadAdcTextFrame))
		self.fGcrReadAdcLabels.append(ROOT.TGLabel(self.fGcrReadAdcLabelFrame, "Idischarge")) ;   self.fGcrReadAdcText.append(ROOT.TGTextEntry(self.fGcrReadAdcTextFrame))
		self.fGcrReadAdcLabels.append(ROOT.TGLabel(self.fGcrReadAdcLabelFrame, "VTH")) ;          self.fGcrReadAdcText.append(ROOT.TGTextEntry(self.fGcrReadAdcTextFrame))


		for k in range(0, 6) :
			self.fGcrReadAdcText[k].DrawBorder()
			self.fGcrReadAdcText[k].SetAlignment(ROOT.kTextRight)
			self.fGcrReadAdcText[k].SetMaxLength(4)

			self.fGcrReadAdcLabelFrame.AddFrame(self.fGcrReadAdcLabels[k], ROOT.TGLayoutHints(ROOT.kLHintsLeft,  5, 5, 5, 1))
			self.fGcrReadAdcTextFrame.AddFrame(self.fGcrReadAdcText[k],    ROOT.TGLayoutHints(ROOT.kLHintsRight, 5, 5, 0, 0))


		self.fGcrReadAdcFrame.AddFrame(self.fGcrReadAdcLabelFrame, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 10, 10, 13, 0))
		self.fGcrReadAdcFrame.AddFrame(self.fGcrReadAdcTextFrame,  ROOT.TGLayoutHints(ROOT.kLHintsExpandX,  5, 10, 15, 0))


		## final frame insertion
		self.AddFrame(self.fGcrReadPix1Frame, ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 10, 10, 20, 10))
		self.AddFrame(self.fGcrReadPix2Frame, ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 10, 10, 20, 10))
		self.AddFrame(self.fGcrReadBiasFrame, ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 10, 10, 20, 10))
		self.AddFrame(self.fGcrReadAdcFrame,  ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 10, 10, 20, 10))




	##________________________________________________________________________________
	def SetGcrValues(self, r) :

		l = r.GetParameters()

		## Torino pixels
		PwmDelayReset               = l[ 0] ;   self.fGcrReadPix1Text[9].SetText(str(PwmDelayReset))                # GCR_DATA[  4:  0]
		PwmHighReset                = l[ 1] ;   self.fGcrReadPix1Text[10].SetText(str(PwmHighReset))                # GCR_DATA[ 12:  5]
		PwmLowReset                 = l[ 2] ;   self.fGcrReadPix1Text[11].SetText(str(PwmLowReset))                 # GCR_DATA[ 26: 13]

		IctrlTotReset               = l[ 3] ;   self.fGcrReadPix1Text[8].SetText(str(IctrlTotReset))                # GCR_DATA[ 36: 27]
		VthDiscReset                = l[ 4] ;   self.fGcrReadPix1Text[7].SetText(str(VthDiscReset))                 # GCR_DATA[ 46: 37]
		VblDiscReset                = l[ 5] ;   self.fGcrReadPix1Text[6].SetText(str(VblDiscReset))                 # GCR_DATA[ 56: 47]
		IbiasP1Reset                = l[ 6] ;   self.fGcrReadPix1Text[0].SetText(str(IbiasP1Reset))                 # GCR_DATA[ 66: 57]
		IbiasP2Reset                = l[ 7] ;   self.fGcrReadPix1Text[1].SetText(str(IbiasP2Reset))                 # GCR_DATA[ 76: 67]
		IbiasDiscReset              = l[ 8] ;   self.fGcrReadPix1Text[5].SetText(str(IbiasDiscReset))               # GCR_DATA[ 86: 77]
		IbiasSFReset                = l[ 9] ;   self.fGcrReadPix1Text[2].SetText(str(IbiasSFReset))                 # GCR_DATA[ 96: 87]
		VrefKrum1Reset              = l[10] ;   self.fGcrReadPix1Text[3].SetText(str(VrefKrum1Reset))               # GCR_DATA[106: 97]
		IbiasFeedReset              = l[11] ;   self.fGcrReadPix1Text[4].SetText(str(IbiasFeedReset))               # GCR_DATA[116:107]

		## reference current
		IrefReset                   = l[12] ;   self.fGcrReadBiasText[1].SetText(str(IrefReset))                    # GCR_DATA[121:117]

		## bandgap reference
		BgrTrimReset                = l[13] ;   self.fGcrReadBiasText[0].SetText(str(BgrTrimReset))                 # GCR_DATA[126:122]

		## monitoring MUX
		MonMuxReset                 = l[14] ;   self.fGcrReadAdcText[0].SetText(str(MonMuxReset))                   # GCR_DATA[131:127]
 
		## Bergamo/Pavia pixels
		IldacReset                  = l[15] ;   self.fGcrReadPix2Text[5].SetText(str(IldacReset))                   # GCR_DATA[141:132]


		IgdacReset                  = l[16] ;   self.fGcrReadPix2Text[4].SetText(str(IgdacReset))                   # GCR_DATA[151:142]
		VrefKrum2Reset              = l[17] ;   self.fGcrReadPix2Text[2].SetText(str(VrefKrum2Reset))               # GCR_DATA[161:152]
		IkrumReset                  = l[18] ;   self.fGcrReadPix2Text[3].SetText(str(IkrumReset))                   # GCR_DATA[171:162]
		IfcBiasReset                = l[19] ;   self.fGcrReadPix2Text[1].SetText(str(IfcBiasReset))                 # GCR_DATA[181:172]
		IpaInBiasReset              = l[20] ;   self.fGcrReadPix2Text[0].SetText(str(IpaInBiasReset))               # GCR_DATA[191:182]

		## global cal level
		CalLevelReset               = l[21] ;   self.fGcrReadBiasText[2].SetText(str(CalLevelReset))                # GCR_DATA[201:192]

		## ADC configuration
		AdcOperatingModeReset       = l[22] ;   self.fGcrReadAdcText[1].SetText(str(AdcOperatingModeReset))         # GCR_DATA[    202]
		AdcTransconductorGainReset  = l[23] ;   self.fGcrReadAdcText[2].SetText(str(AdcTransconductorGainReset))    # GCR_DATA[206:203]
		AdcIdischargeReset          = l[24] ;   self.fGcrReadAdcText[4].SetText(str(AdcIdischargeReset))            # GCR_DATA[212:207]
		AdcIchargeReset             = l[25] ;   self.fGcrReadAdcText[3].SetText(str(AdcIchargeReset))               # GCR_DATA[218:213]
		AdcComparatorThresholdReset = l[26] ;   self.fGcrReadAdcText[5].SetText(str(AdcComparatorThresholdReset))   # GCR_DATA[223:219]





############################
## CLASS: GcrWriteFrame   ##
############################

class GcrWriteFrame(ROOT.TGHorizontalFrame) :

	##________________________________________________________________________________
	def __init__(self, parent) :

		## create TGHorizontalFrame to contain board number, firmware version etc.
		if __debug__ :

			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame|ROOT.kRaisedFrame)
		else :
			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame)

		self.fGcrWritePix1Frame = ROOT.TGGroupFrame(self, " TO pixels bias and auto-zeroing",    ROOT.kHorizontalFrame)
		self.fGcrWritePix2Frame = ROOT.TGGroupFrame(self, " BG/PV pixels bias ", ROOT.kHorizontalFrame)
		self.fGcrWriteBiasFrame = ROOT.TGGroupFrame(self, " Global reference / charge injection ",  ROOT.kHorizontalFrame)
		self.fGcrWriteAdcFrame  = ROOT.TGGroupFrame(self, " Monitoring / ADC configuration ", ROOT.kHorizontalFrame)

		#################
		##   TO GCRs   ##
		#################
		self.fGcrWritePix1LabelFrameL = ROOT.TGVerticalFrame(self.fGcrWritePix1Frame)
		self.fGcrWritePix1LabelFrameR = ROOT.TGVerticalFrame(self.fGcrWritePix1Frame)

		self.fGcrWritePix1EntryFrameL  = ROOT.TGVerticalFrame(self.fGcrWritePix1Frame) 
		self.fGcrWritePix1EntryFrameR  = ROOT.TGVerticalFrame(self.fGcrWritePix1Frame)

		self.fGcrWritePix1Labels = []
		self.fGcrWritePix1Entries = []

		self.fGcrWritePix1Labels.append(ROOT.TGLabel(self.fGcrWritePix1LabelFrameL, "IBIASP1"))
		self.fGcrWritePix1Labels.append(ROOT.TGLabel(self.fGcrWritePix1LabelFrameL, "IBIASP2"))
		self.fGcrWritePix1Labels.append(ROOT.TGLabel(self.fGcrWritePix1LabelFrameL, "IBIAS_SF"))
		self.fGcrWritePix1Labels.append(ROOT.TGLabel(self.fGcrWritePix1LabelFrameL, "VREF_KRUM"))
		self.fGcrWritePix1Labels.append(ROOT.TGLabel(self.fGcrWritePix1LabelFrameL, "IBIAS_FEED"))
		self.fGcrWritePix1Labels.append(ROOT.TGLabel(self.fGcrWritePix1LabelFrameL, "IBIAS_DISC"))

		self.fGcrWritePix1Labels.append(ROOT.TGLabel(self.fGcrWritePix1LabelFrameR, "VBL_DISC"))
		self.fGcrWritePix1Labels.append(ROOT.TGLabel(self.fGcrWritePix1LabelFrameR, "VTH_DISC"))
		self.fGcrWritePix1Labels.append(ROOT.TGLabel(self.fGcrWritePix1LabelFrameR, "ICTRL_TOT"))
		self.fGcrWritePix1Labels.append(ROOT.TGLabel(self.fGcrWritePix1LabelFrameR, "PWM delay"))
		self.fGcrWritePix1Labels.append(ROOT.TGLabel(self.fGcrWritePix1LabelFrameR, "PWM high"))
		self.fGcrWritePix1Labels.append(ROOT.TGLabel(self.fGcrWritePix1LabelFrameR, "PWM low"))


		## IBIASP1
		self.fGcrWritePix1Entries.append(ROOT.TGNumberEntry(
			self.fGcrWritePix1EntryFrameL, 100, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)

		## IBIASP2
		self.fGcrWritePix1Entries.append(ROOT.TGNumberEntry(
			self.fGcrWritePix1EntryFrameL, 150, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)

		## IBIAS_SF
		self.fGcrWritePix1Entries.append(ROOT.TGNumberEntry(
			self.fGcrWritePix1EntryFrameL, 100, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)

		## VREF_KRUM
		self.fGcrWritePix1Entries.append(ROOT.TGNumberEntry(
			self.fGcrWritePix1EntryFrameL, 490, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)

		## IBIAS_FEED
		self.fGcrWritePix1Entries.append(ROOT.TGNumberEntry(
			self.fGcrWritePix1EntryFrameL, 80, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)

		## IBIAS_DISC
		self.fGcrWritePix1Entries.append(ROOT.TGNumberEntry(
			self.fGcrWritePix1EntryFrameL, 200, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)

		## VBL_DISC
		self.fGcrWritePix1Entries.append(ROOT.TGNumberEntry(
			self.fGcrWritePix1EntryFrameR, 450, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)

		## VTH_DISC
		self.fGcrWritePix1Entries.append(ROOT.TGNumberEntry(
			self.fGcrWritePix1EntryFrameR, 1023, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)

		## ICTRL_TOT
		self.fGcrWritePix1Entries.append(ROOT.TGNumberEntry(
			self.fGcrWritePix1EntryFrameR, 100, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)

		## PWM delay
		self.fGcrWritePix1Entries.append(ROOT.TGNumberEntry(
			self.fGcrWritePix1EntryFrameR, 0, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**5 -1))		
			)

		## PWM high
		self.fGcrWritePix1Entries.append(ROOT.TGNumberEntry(
			self.fGcrWritePix1EntryFrameR, 20, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)

		## PWM low
		self.fGcrWritePix1Entries.append(ROOT.TGNumberEntry(
			self.fGcrWritePix1EntryFrameR, 3980, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)

		for k in range(0, 6) :
			self.fGcrWritePix1LabelFrameL.AddFrame(self.fGcrWritePix1Labels[k],  ROOT.TGLayoutHints(ROOT.kLHintsLeft,  5, 5, 5, 1))
			self.fGcrWritePix1EntryFrameL.AddFrame(self.fGcrWritePix1Entries[k], ROOT.TGLayoutHints(ROOT.kLHintsRight, 5, 5, 0, 0))


		for k in range(6, 12) :
			self.fGcrWritePix1LabelFrameR.AddFrame(self.fGcrWritePix1Labels[k],  ROOT.TGLayoutHints(ROOT.kLHintsLeft,  5, 5, 5, 1))
			self.fGcrWritePix1EntryFrameR.AddFrame(self.fGcrWritePix1Entries[k], ROOT.TGLayoutHints(ROOT.kLHintsRight, 5, 5, 0, 0))


		self.fGcrWritePix1Frame.AddFrame(self.fGcrWritePix1LabelFrameL, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 10, 10, 13, 0))
		self.fGcrWritePix1Frame.AddFrame(self.fGcrWritePix1EntryFrameL, ROOT.TGLayoutHints(ROOT.kLHintsExpandX,  5, 10, 15, 0))
		self.fGcrWritePix1Frame.AddFrame(self.fGcrWritePix1LabelFrameR, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 20, 10, 13, 0))
		self.fGcrWritePix1Frame.AddFrame(self.fGcrWritePix1EntryFrameR, ROOT.TGLayoutHints(ROOT.kLHintsExpandX,  5, 10, 15, 0))


		####################
		##   BG/PV GCRs   ##
		####################

		self.fGcrWritePix2LabelFrame = ROOT.TGVerticalFrame(self.fGcrWritePix2Frame)
		self.fGcrWritePix2EntryFrame = ROOT.TGVerticalFrame(self.fGcrWritePix2Frame) 

		self.fGcrWritePix2Labels = []
		self.fGcrWritePix2Entries = []

		self.fGcrWritePix2Labels.append(ROOT.TGLabel(self.fGcrWritePix2LabelFrame, "IPA_IN_BIAS"))
		self.fGcrWritePix2Labels.append(ROOT.TGLabel(self.fGcrWritePix2LabelFrame, "IFC_BIAS"))
		self.fGcrWritePix2Labels.append(ROOT.TGLabel(self.fGcrWritePix2LabelFrame, "VREF_KRUM"))
		self.fGcrWritePix2Labels.append(ROOT.TGLabel(self.fGcrWritePix2LabelFrame, "IKRUM"))
		self.fGcrWritePix2Labels.append(ROOT.TGLabel(self.fGcrWritePix2LabelFrame, "IGDAC"))
		self.fGcrWritePix2Labels.append(ROOT.TGLabel(self.fGcrWritePix2LabelFrame, "ILDAC"))


		## IPA_IN_BIAS
		self.fGcrWritePix2Entries.append(ROOT.TGNumberEntry(
			self.fGcrWritePix2EntryFrame, 300, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)

		## IFC_BIAS
		self.fGcrWritePix2Entries.append(ROOT.TGNumberEntry(
			self.fGcrWritePix2EntryFrame, 200, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)

		## VREF_KRUM
		self.fGcrWritePix2Entries.append(ROOT.TGNumberEntry(
			self.fGcrWritePix2EntryFrame, 300, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)

		## IKRUM
		self.fGcrWritePix2Entries.append(ROOT.TGNumberEntry(
			self.fGcrWritePix2EntryFrame, 50, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)

		## IGDAC
		self.fGcrWritePix2Entries.append(ROOT.TGNumberEntry(
			self.fGcrWritePix2EntryFrame, 1023, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)

		## ILDAC
		self.fGcrWritePix2Entries.append(ROOT.TGNumberEntry(
			self.fGcrWritePix2EntryFrame, 160, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)


		for k in range(0, 6) :
			self.fGcrWritePix2LabelFrame.AddFrame(self.fGcrWritePix2Labels[k],  ROOT.TGLayoutHints(ROOT.kLHintsLeft,  5, 5, 5, 1))
			self.fGcrWritePix2EntryFrame.AddFrame(self.fGcrWritePix2Entries[k], ROOT.TGLayoutHints(ROOT.kLHintsRight, 5, 5, 0, 0))

		self.fGcrWritePix2Frame.AddFrame(self.fGcrWritePix2LabelFrame, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 10, 10, 13, 0))
		self.fGcrWritePix2Frame.AddFrame(self.fGcrWritePix2EntryFrame, ROOT.TGLayoutHints(ROOT.kLHintsExpandX,  5, 10, 15, 0))


		#######################
		##   Bias/Cal GCRs   ##
		#######################

		self.fGcrWriteBiasLabelFrame = ROOT.TGVerticalFrame(self.fGcrWriteBiasFrame)
		self.fGcrWriteBiasEntryFrame = ROOT.TGVerticalFrame(self.fGcrWriteBiasFrame) 

		self.fGcrWriteBiasLabels = []
		self.fGcrWriteBiasEntries = []

		self.fGcrWriteBiasLabels.append(ROOT.TGLabel(self.fGcrWriteBiasLabelFrame, "Bandgap"))
		self.fGcrWriteBiasLabels.append(ROOT.TGLabel(self.fGcrWriteBiasLabelFrame, "IREF trim"))
		self.fGcrWriteBiasLabels.append(ROOT.TGLabel(self.fGcrWriteBiasLabelFrame, "CAL"))

		## BGR
		self.fGcrWriteBiasEntries.append(ROOT.TGNumberEntry(
			self.fGcrWriteBiasEntryFrame, 5, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**4 -1))
			)

		## IREF
		self.fGcrWriteBiasEntries.append(ROOT.TGNumberEntry(
			self.fGcrWriteBiasEntryFrame, 20, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**5 -1))
			)

		## CAL
		self.fGcrWriteBiasEntries.append(ROOT.TGNumberEntry(
			self.fGcrWriteBiasEntryFrame, 0, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)


		for k in range(0, 3) :
			self.fGcrWriteBiasLabelFrame.AddFrame(self.fGcrWriteBiasLabels[k],  ROOT.TGLayoutHints(ROOT.kLHintsLeft,  5, 5, 5, 1))
			self.fGcrWriteBiasEntryFrame.AddFrame(self.fGcrWriteBiasEntries[k], ROOT.TGLayoutHints(ROOT.kLHintsRight, 0, 0, 0, 0))


		self.fGcrWriteBiasFrame.AddFrame(self.fGcrWriteBiasLabelFrame, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 10, 10, 13, 0))
		self.fGcrWriteBiasFrame.AddFrame(self.fGcrWriteBiasEntryFrame, ROOT.TGLayoutHints(ROOT.kLHintsExpandX,  5, 10, 15, 0))


		##################
		##   ADC GCRs   ##
		##################

		self.fGcrWriteAdcLabelFrame = ROOT.TGVerticalFrame(self.fGcrWriteAdcFrame)
		self.fGcrWriteAdcEntryFrame = ROOT.TGVerticalFrame(self.fGcrWriteAdcFrame) 

		self.fGcrWriteAdcLabels = []
		self.fGcrWriteAdcEntries = []

		self.fGcrWriteAdcLabels.append(ROOT.TGLabel(self.fGcrWriteAdcLabelFrame, "MON_MUX"))
		self.fGcrWriteAdcLabels.append(ROOT.TGLabel(self.fGcrWriteAdcLabelFrame, "MODE"))
		self.fGcrWriteAdcLabels.append(ROOT.TGLabel(self.fGcrWriteAdcLabelFrame, "gm gain"))
		self.fGcrWriteAdcLabels.append(ROOT.TGLabel(self.fGcrWriteAdcLabelFrame, "Icharge"))
		self.fGcrWriteAdcLabels.append(ROOT.TGLabel(self.fGcrWriteAdcLabelFrame, "Idischarge"))
		self.fGcrWriteAdcLabels.append(ROOT.TGLabel(self.fGcrWriteAdcLabelFrame, "VTH"))


		## MON_MUX
		self.fGcrWriteAdcEntries.append(ROOT.TGNumberEntry(
			self.fGcrWriteAdcEntryFrame, 16, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 31)
			)

		## MODE
		self.fGcrWriteAdcEntries.append(ROOT.TGNumberEntry(
			self.fGcrWriteAdcEntryFrame, 0, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 1)
			)

		## gm-gain
		self.fGcrWriteAdcEntries.append(ROOT.TGNumberEntry(
			self.fGcrWriteAdcEntryFrame, 8, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 15)
			)

		## Icharge
		self.fGcrWriteAdcEntries.append(ROOT.TGNumberEntry(
			self.fGcrWriteAdcEntryFrame, 28, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)

		## Idischarge
		self.fGcrWriteAdcEntries.append(ROOT.TGNumberEntry(
			self.fGcrWriteAdcEntryFrame, 28, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))
			)

		## VTH
		self.fGcrWriteAdcEntries.append(ROOT.TGNumberEntry(
			self.fGcrWriteAdcEntryFrame, 16, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 31)
			)


		for k in range(0, 6) :
			self.fGcrWriteAdcLabelFrame.AddFrame(self.fGcrWriteAdcLabels[k],  ROOT.TGLayoutHints(ROOT.kLHintsLeft,  5, 5, 5, 1))
			self.fGcrWriteAdcEntryFrame.AddFrame(self.fGcrWriteAdcEntries[k], ROOT.TGLayoutHints(ROOT.kLHintsRight, 5, 5, 0, 0))


		self.fGcrWriteAdcFrame.AddFrame(self.fGcrWriteAdcLabelFrame, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 10, 10, 13, 0))
		self.fGcrWriteAdcFrame.AddFrame(self.fGcrWriteAdcEntryFrame, ROOT.TGLayoutHints(ROOT.kLHintsExpandX,  5, 10, 15, 0))




		self.AddFrame(self.fGcrWritePix1Frame, ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 10, 10, 20, 10))
		self.AddFrame(self.fGcrWritePix2Frame, ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 10, 10, 20, 10))
		self.AddFrame(self.fGcrWriteBiasFrame, ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 10, 10, 20, 10))
		self.AddFrame(self.fGcrWriteAdcFrame,  ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 10, 10, 20, 10))


	##________________________________________________________________________________
	def GetGcrValues(self) :

		## Torino pixels
		PwmDelay               = int(self.fGcrWritePix1Entries[9].GetNumber())              # GCR_DATA[  4:  0]
		PwmHigh                = int(self.fGcrWritePix1Entries[10].GetNumber())             # GCR_DATA[ 12:  5]
		PwmLow                 = int(self.fGcrWritePix1Entries[11].GetNumber())             # GCR_DATA[ 26: 13]

		IctrlTot               = int(self.fGcrWritePix1Entries[8].GetNumber())              # GCR_DATA[ 36: 27]
		VthDisc                = int(self.fGcrWritePix1Entries[7].GetNumber())              # GCR_DATA[ 46: 37]
		VblDisc                = int(self.fGcrWritePix1Entries[6].GetNumber())              # GCR_DATA[ 56: 47]
		IbiasP1                = int(self.fGcrWritePix1Entries[0].GetNumber())              # GCR_DATA[ 66: 57]
		IbiasP2                = int(self.fGcrWritePix1Entries[1].GetNumber())              # GCR_DATA[ 76: 67]
		IbiasDisc              = int(self.fGcrWritePix1Entries[5].GetNumber())              # GCR_DATA[ 86: 77]
		IbiasSF                = int(self.fGcrWritePix1Entries[2].GetNumber())              # GCR_DATA[ 96: 87]
		VrefKrum1              = int(self.fGcrWritePix1Entries[3].GetNumber())              # GCR_DATA[106: 97]
		IbiasFeed              = int(self.fGcrWritePix1Entries[4].GetNumber())              # GCR_DATA[116:107]

		## reference current
		Iref                   = int(self.fGcrWriteBiasEntries[1].GetNumber())              # GCR_DATA[121:117]

		## bandgap reference
		BgrTrim                = int(self.fGcrWriteBiasEntries[0].GetNumber())              # GCR_DATA[126:122]

		## monitoring MUX
		MonMux                 = int(self.fGcrWriteAdcEntries[0].GetNumber())               # GCR_DATA[131:127]
 
		## Bergamo/Pavia pixels
		Ildac                  = int(self.fGcrWritePix2Entries[5].GetNumber())              # GCR_DATA[141:132]
		Igdac                  = int(self.fGcrWritePix2Entries[4].GetNumber())              # GCR_DATA[151:142]
		VrefKrum2              = int(self.fGcrWritePix2Entries[2].GetNumber())              # GCR_DATA[161:152]
		Ikrum                  = int(self.fGcrWritePix2Entries[3].GetNumber())              # GCR_DATA[171:162]
		IfcBias                = int(self.fGcrWritePix2Entries[1].GetNumber())              # GCR_DATA[181:172]
		IpaInBias              = int(self.fGcrWritePix2Entries[0].GetNumber())              # GCR_DATA[191:182]

		## global cal level
		CalLevel               = int(self.fGcrWriteBiasEntries[2].GetNumber())              # GCR_DATA[201:192]

		## ADC configuration
		AdcOperatingMode       = int(self.fGcrWriteAdcEntries[1].GetNumber())               # GCR_DATA[    202]
		AdcTransconductorGain  = int(self.fGcrWriteAdcEntries[2].GetNumber())               # GCR_DATA[206:203]
		AdcIdischarge          = int(self.fGcrWriteAdcEntries[4].GetNumber())               # GCR_DATA[212:207]
		AdcIcharge             = int(self.fGcrWriteAdcEntries[3].GetNumber())               # GCR_DATA[218:213]
		AdcComparatorThreshold = int(self.fGcrWriteAdcEntries[5].GetNumber())               # GCR_DATA[223:219]

		parameters = []

		parameters.append(PwmDelay)
		parameters.append(PwmHigh)
		parameters.append(PwmLow)
		parameters.append(IctrlTot)
		parameters.append(VthDisc)
		parameters.append(VblDisc)
		parameters.append(IbiasP1)
		parameters.append(IbiasP2)
		parameters.append(IbiasDisc)
		parameters.append(IbiasSF)
		parameters.append(VrefKrum1)
		parameters.append(IbiasFeed)
		parameters.append(Iref)
		parameters.append(BgrTrim)
		parameters.append(MonMux)
		parameters.append(Ildac)
		parameters.append(Igdac)
		parameters.append(VrefKrum2)
		parameters.append(Ikrum)
		parameters.append(IfcBias)
		parameters.append(IpaInBias)
		parameters.append(CalLevel)
		parameters.append(AdcOperatingMode)
		parameters.append(AdcTransconductorGain)
		parameters.append(AdcIdischarge)
		parameters.append(AdcIcharge)
		parameters.append(AdcComparatorThreshold)

		return parameters 




##############################
##   CLASS: EccrReadFrame   ##
##############################

class EccrReadFrame(ROOT.TGHorizontalFrame) :

	##________________________________________________________________________________
	def __init__(self, parent) :

		## create TGHorizontalFrame to contain board number, firmware version etc.
		if __debug__ :
			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame|ROOT.kRaisedFrame)
		else :
			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame)

		self.fEccrReadReadoutFrame = ROOT.TGGroupFrame(self, " Readout configuration ", ROOT.kVerticalFrame)

		self.fEccrReadTriggerLatencyFrame = ROOT.TGHorizontalFrame(self.fEccrReadReadoutFrame, 0, 0, ROOT.kChildFrame)

		self.fEccrReadTriggerLatencyLabel = ROOT.TGLabel(self.fEccrReadTriggerLatencyFrame, "Trigger latency")

		self.fEccrReadTriggerLatencyText = ROOT.TGTextEntry(self.fEccrReadTriggerLatencyFrame)
		self.fEccrReadTriggerLatencyText.SetAlignment(ROOT.kTextRight)

		self.fEccrReadTriggerLatencyFrame.AddFrame(self.fEccrReadTriggerLatencyLabel, ROOT.TGLayoutHints(ROOT.kLHintsNoHints,  0, 10, 2, 0))
		self.fEccrReadTriggerLatencyFrame.AddFrame(self.fEccrReadTriggerLatencyText,  ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10, 0, 0))

		self.fEccrReadTriggerModeEnable     = ROOT.TGCheckButton(self.fEccrReadReadoutFrame, "Trigger mode")
		self.fEccrReadTotModeEnable         = ROOT.TGCheckButton(self.fEccrReadReadoutFrame, "ToT mode")
		self.fEccrReadHighDeadtimeEnable    = ROOT.TGCheckButton(self.fEccrReadReadoutFrame, "High-deadtime mode")
		self.fEccrReadBinaryTimestampEnable = ROOT.TGCheckButton(self.fEccrReadReadoutFrame, "Binary timestamp")
		self.fEccrRead8b10bDisable          = ROOT.TGCheckButton(self.fEccrReadReadoutFrame, "Disable 8b/10b")

		self.fEccrReadReadoutFrame.AddFrame(self.fEccrReadTriggerLatencyFrame,   ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10, 20,  5))
		self.fEccrReadReadoutFrame.AddFrame(self.fEccrReadTriggerModeEnable,     ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10,  5,  5))
		self.fEccrReadReadoutFrame.AddFrame(self.fEccrReadTotModeEnable,         ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10,  5,  5))
		self.fEccrReadReadoutFrame.AddFrame(self.fEccrReadHighDeadtimeEnable,    ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10,  5,  5))
		self.fEccrReadReadoutFrame.AddFrame(self.fEccrReadBinaryTimestampEnable, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10,  5,  5))
		self.fEccrReadReadoutFrame.AddFrame(self.fEccrRead8b10bDisable,          ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10,  5, 10))


		self.fEccrReadMaskFrame = ROOT.TGGroupFrame(self, " Masking configuration ", ROOT.kHorizontalFrame)

		self.fGcrReadMcdMaskLabel = ROOT.TGLabel(self.fEccrReadMaskFrame, "MCD MASK")

		self.fEccrReadMcdMaskText = ROOT.TGTextEntry(self.fEccrReadMaskFrame)
		self.fEccrReadMcdMaskText.SetMaxLength(16)
		self.fEccrReadMcdMaskText.SetAlignment(ROOT.kTextRight)
		self.fEccrReadMcdMaskText.SetDefaultSize(100,22)


		self.fEccrReadMaskFrame.AddFrame(self.fGcrReadMcdMaskLabel, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10, 22, 10))
		self.fEccrReadMaskFrame.AddFrame(self.fEccrReadMcdMaskText, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10, 20, 10))

		self.AddFrame(self.fEccrReadReadoutFrame, ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 10, 10, 20, 10))
		self.AddFrame(self.fEccrReadMaskFrame,    ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 40, 40, 20, 10))


	##________________________________________________________________________________
	def SetEccrValues(self) :
		pass



	##________________________________________________________________________________
	def SetEccrResetValues(self) :

		triggerLatency          = 0                  ;   self.fEccrReadTriggerLatencyText.SetText(str(triggerLatency))
		triggeredOperations     = ROOT.kFALSE        ;   self.fEccrReadTriggerModeEnable.SetState(ROOT.kButtonUp)
		totMode                 = ROOT.kFALSE        ;   self.fEccrReadTotModeEnable.SetState(ROOT.kButtonUp)
		highDeadtimeMode        = ROOT.kFALSE        ;   self.fEccrReadHighDeadtimeEnable.SetState(ROOT.kButtonUp)
		binaryTimestampEncoding = ROOT.kFALSE        ;   self.fEccrReadBinaryTimestampEnable.SetState(ROOT.kButtonUp)
		disable8b10bEncoding    = ROOT.kFALSE        ;   self.fEccrRead8b10bDisable.SetState(ROOT.kButtonUp)
		mcdMask                 = 0b0000000000000000 ;   self.fEccrReadMcdMaskText.SetText("0x" + format(mcdMask, '04x'))


###############################
##   CLASS: EccrWriteFrame   ##
###############################

class EccrWriteFrame(ROOT.TGHorizontalFrame) :

	##________________________________________________________________________________
	def __init__(self, parent) :

		## create TGHorizontalFrame to contain board number, firmware version etc.
		if __debug__ :

			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame|ROOT.kRaisedFrame)
		else :
			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame)

		self.fEccrWriteReadoutFrame = ROOT.TGGroupFrame(self, " Readout configuration ", ROOT.kVerticalFrame)

		self.fEccrWriteTriggerLatencyFrame = ROOT.TGHorizontalFrame(self.fEccrWriteReadoutFrame, 0, 0, ROOT.kChildFrame)

		self.fEccrWriteTriggerLatencyLabel = ROOT.TGLabel(self.fEccrWriteTriggerLatencyFrame, "Trigger latency")

		self.fEccrWriteTriggerLatencyEntry = ROOT.TGNumberEntry(
			self.fEccrWriteTriggerLatencyFrame, 0, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**10 -1))

		self.fEccrWriteTriggerLatencyFrame.AddFrame(self.fEccrWriteTriggerLatencyLabel, ROOT.TGLayoutHints(ROOT.kLHintsNoHints,  0, 10, 2, 0))
		self.fEccrWriteTriggerLatencyFrame.AddFrame(self.fEccrWriteTriggerLatencyEntry, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10, 0, 0))

		self.fEccrWriteTriggerModeEnable     = ROOT.TGCheckButton(self.fEccrWriteReadoutFrame, "Trigger mode")
		self.fEccrWriteTotModeEnable         = ROOT.TGCheckButton(self.fEccrWriteReadoutFrame, "ToT mode")
		self.fEccrWriteHighDeadtimeEnable    = ROOT.TGCheckButton(self.fEccrWriteReadoutFrame, "High-deadtime mode")
		self.fEccrWriteBinaryTimestampEnable = ROOT.TGCheckButton(self.fEccrWriteReadoutFrame, "Binary timestamp")
		self.fEccrWrite8b10bDisable          = ROOT.TGCheckButton(self.fEccrWriteReadoutFrame, "Disable 8b/10b")

		self.fEccrWriteReadoutFrame.AddFrame(self.fEccrWriteTriggerLatencyFrame,   ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10, 20,  5))
		self.fEccrWriteReadoutFrame.AddFrame(self.fEccrWriteTriggerModeEnable,     ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10,  5,  5))
		self.fEccrWriteReadoutFrame.AddFrame(self.fEccrWriteTotModeEnable,         ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10,  5,  5))
		self.fEccrWriteReadoutFrame.AddFrame(self.fEccrWriteHighDeadtimeEnable,    ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10,  5,  5))
		self.fEccrWriteReadoutFrame.AddFrame(self.fEccrWriteBinaryTimestampEnable, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10,  5,  5))
		self.fEccrWriteReadoutFrame.AddFrame(self.fEccrWrite8b10bDisable,          ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10,  5, 10))


		self.fEccrWriteMaskFrame = ROOT.TGGroupFrame(self, " Masking configuration ", ROOT.kHorizontalFrame)

		self.fGcrWriteMcdMaskLabel = ROOT.TGLabel(self.fEccrWriteMaskFrame, "MCD MASK")

		self.fEccrWriteMcdMaskEntry = ROOT.TGNumberEntry(
			self.fEccrWriteMaskFrame, 0, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**16 -1))

		self.fEccrWriteMaskFrame.AddFrame(self.fGcrWriteMcdMaskLabel,  ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10, 22, 10))
		self.fEccrWriteMaskFrame.AddFrame(self.fEccrWriteMcdMaskEntry, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10, 20, 10))

		self.AddFrame(self.fEccrWriteReadoutFrame, ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 10, 10, 20, 10))
		self.AddFrame(self.fEccrWriteMaskFrame,    ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 40, 40, 20, 10))

	##________________________________________________________________________________
	def GetEccrValues(self) :

		triggerLatency = int(self.fEccrWriteTriggerLatencyEntry.GetNumber())
		mcdMask = int(self.fEccrWriteMcdMaskEntry.GetNumber())

		triggeredOperations     = int(self.fEccrWriteTriggerModeEnable.IsOn())
		totMode                 = int(self.fEccrWriteTotModeEnable.IsOn())
		highDeadtimeMode        = int(self.fEccrWriteHighDeadtimeEnable.IsOn())
		binaryTimestampEncoding = int(self.fEccrWriteBinaryTimestampEnable.IsOn())
		disable8b10bEncoding    = int(self.fEccrWrite8b10bDisable.IsOn())

		ECCR_DATA = []

		ECCR_DATA.append(triggerLatency)
		ECCR_DATA.append(triggeredOperations)
		ECCR_DATA.append(totMode)
		ECCR_DATA.append(highDeadtimeMode)
		ECCR_DATA.append(binaryTimestampEncoding)
		ECCR_DATA.append(disable8b10bEncoding)
		ECCR_DATA.append(mcdMask)

		return ECCR_DATA



#############################
##   CLASS: PcrReadFrame   ##
#############################

class PcrReadFrame(ROOT.TGHorizontalFrame) :

	##________________________________________________________________________________
	def __init__(self, parent) :

		## create TGHorizontalFrame to contain board number, firmware version etc.
		if __debug__ :

			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame|ROOT.kRaisedFrame)
		else :
			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame)

		self.fPcrReadPix1Frame = ROOT.TGGroupFrame(self, " TO pixel ",      ROOT.kHorizontalFrame)
		self.fPcrReadPix2Frame = ROOT.TGGroupFrame(self, " BG/PV pixel ",   ROOT.kHorizontalFrame)



		#######################
		##   "read" PCR TO   ##
		#######################
		self.fPcrReadPix1FrameL = ROOT.TGGroupFrame(self.fPcrReadPix1Frame, " LEFT ", ROOT.kVerticalFrame)
		self.fPcrReadPix1FrameR = ROOT.TGGroupFrame(self.fPcrReadPix1Frame, " RIGHT ", ROOT.kVerticalFrame)

		self.fPcrReadPix1EnableL = []
		self.fPcrReadPix1EnableR = []

		self.fPcrReadPix1EnableL.append(ROOT.TGCheckButton(self.fPcrReadPix1FrameL, "MASK"))
		self.fPcrReadPix1EnableL.append(ROOT.TGCheckButton(self.fPcrReadPix1FrameL, "CAL_EN"))
		self.fPcrReadPix1EnableL.append(ROOT.TGCheckButton(self.fPcrReadPix1FrameL, "FAST_MODE"))
		self.fPcrReadPix1EnableL.append(ROOT.TGCheckButton(self.fPcrReadPix1FrameL, "SEL_C2F"))
		self.fPcrReadPix1EnableL.append(ROOT.TGCheckButton(self.fPcrReadPix1FrameL, "SEL_C4F"))

		self.fPcrReadPix1EnableR.append(ROOT.TGCheckButton(self.fPcrReadPix1FrameR, "MASK"))
		self.fPcrReadPix1EnableR.append(ROOT.TGCheckButton(self.fPcrReadPix1FrameR, "CAL_EN"))
		self.fPcrReadPix1EnableR.append(ROOT.TGCheckButton(self.fPcrReadPix1FrameR, "FAST_MODE"))
		self.fPcrReadPix1EnableR.append(ROOT.TGCheckButton(self.fPcrReadPix1FrameR, "SEL_C2F"))
		self.fPcrReadPix1EnableR.append(ROOT.TGCheckButton(self.fPcrReadPix1FrameR, "SEL_C4F"))

		self.fPcrReadPix1FrameL.AddFrame(self.fPcrReadPix1EnableL[0], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 20, 3))
		self.fPcrReadPix1FrameL.AddFrame(self.fPcrReadPix1EnableL[1], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrReadPix1FrameL.AddFrame(self.fPcrReadPix1EnableL[2], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrReadPix1FrameL.AddFrame(self.fPcrReadPix1EnableL[3], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrReadPix1FrameL.AddFrame(self.fPcrReadPix1EnableL[4], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))

		self.fPcrReadPix1FrameR.AddFrame(self.fPcrReadPix1EnableR[0], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 20, 3))
		self.fPcrReadPix1FrameR.AddFrame(self.fPcrReadPix1EnableR[1], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrReadPix1FrameR.AddFrame(self.fPcrReadPix1EnableR[2], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrReadPix1FrameR.AddFrame(self.fPcrReadPix1EnableR[3], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrReadPix1FrameR.AddFrame(self.fPcrReadPix1EnableR[4], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))

		self.fPcrReadPix1Frame.AddFrame(self.fPcrReadPix1FrameL, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10, 10, 0))
		self.fPcrReadPix1Frame.AddFrame(self.fPcrReadPix1FrameR, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10, 10, 0))


		##########################
		##   "read" PCR BG/PV   ##
		##########################
		self.fPcrReadPix2FrameL = ROOT.TGGroupFrame(self.fPcrReadPix2Frame, " LEFT ",  ROOT.kVerticalFrame)
		self.fPcrReadPix2FrameR = ROOT.TGGroupFrame(self.fPcrReadPix2Frame, " RIGHT ", ROOT.kVerticalFrame)

		self.fPcrReadPix2EnableL = []
		self.fPcrReadPix2EnableR = []

		self.fPcrReadPix2EnableL.append(ROOT.TGCheckButton(self.fPcrReadPix2FrameL, "MASK"))
		self.fPcrReadPix2EnableL.append(ROOT.TGCheckButton(self.fPcrReadPix2FrameL, "CAL_EN"))
		self.fPcrReadPix2EnableL.append(ROOT.TGCheckButton(self.fPcrReadPix2FrameL, "GAIN"))
		self.fPcrReadPix2EnableL.append(ROOT.TGCheckButton(self.fPcrReadPix2FrameL, "POWER_DWN"))

		self.fPcrReadPix2EnableR.append(ROOT.TGCheckButton(self.fPcrReadPix2FrameR, "MASK"))
		self.fPcrReadPix2EnableR.append(ROOT.TGCheckButton(self.fPcrReadPix2FrameR, "CAL_EN"))
		self.fPcrReadPix2EnableR.append(ROOT.TGCheckButton(self.fPcrReadPix2FrameR, "GAIN"))
		self.fPcrReadPix2EnableR.append(ROOT.TGCheckButton(self.fPcrReadPix2FrameR, "POWER_DWN"))

		self.fPcrReadVthFrameL = ROOT.TGHorizontalFrame(self.fPcrReadPix2FrameL, ROOT.kChildFrame)
		self.fPcrReadVthFrameR = ROOT.TGHorizontalFrame(self.fPcrReadPix2FrameR, ROOT.kChildFrame)

		self.fPcrReadVthLabelL = ROOT.TGLabel(self.fPcrReadVthFrameL, "VTH_DAC")
		self.fPcrReadVthLabelR = ROOT.TGLabel(self.fPcrReadVthFrameR, "VTH_DAC")

		self.fPcrReadVthTextL = ROOT.TGTextEntry(self.fPcrReadVthFrameL)
		self.fPcrReadVthTextR = ROOT.TGTextEntry(self.fPcrReadVthFrameR)

		self.fPcrReadVthFrameL.AddFrame(self.fPcrReadVthLabelL, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  2,  0))
		self.fPcrReadVthFrameL.AddFrame(self.fPcrReadVthTextL,  ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  0,  0))

		self.fPcrReadVthFrameR.AddFrame(self.fPcrReadVthLabelR, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  2,  0))
		self.fPcrReadVthFrameR.AddFrame(self.fPcrReadVthTextR,  ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  0,  0))

		self.fPcrReadPix2FrameL.AddFrame(self.fPcrReadPix2EnableL[0], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 20, 3))
		self.fPcrReadPix2FrameL.AddFrame(self.fPcrReadPix2EnableL[1], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrReadPix2FrameL.AddFrame(self.fPcrReadPix2EnableL[2], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrReadPix2FrameL.AddFrame(self.fPcrReadPix2EnableL[3], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrReadPix2FrameL.AddFrame(self.fPcrReadVthFrameL,      ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))

		self.fPcrReadPix2FrameR.AddFrame(self.fPcrReadPix2EnableR[0], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 20, 3))
		self.fPcrReadPix2FrameR.AddFrame(self.fPcrReadPix2EnableR[1], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrReadPix2FrameR.AddFrame(self.fPcrReadPix2EnableR[2], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrReadPix2FrameR.AddFrame(self.fPcrReadPix2EnableR[3], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrReadPix2FrameR.AddFrame(self.fPcrReadVthFrameR,      ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))


		self.fPcrReadPix2Frame.AddFrame(self.fPcrReadPix2FrameL, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10, 10, 0))
		self.fPcrReadPix2Frame.AddFrame(self.fPcrReadPix2FrameR, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10, 10, 0))


		self.AddFrame(self.fPcrReadPix1Frame, ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 20, 10, 20, 10))
		self.AddFrame(self.fPcrReadPix2Frame, ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 20, 10, 20, 10))


	##________________________________________________________________________________
	def SetPcrValues(self) :
		pass



##############################
##   CLASS: PcrWriteFrame   ##
##############################

class PcrWriteFrame(ROOT.TGHorizontalFrame) :

	##________________________________________________________________________________
	def __init__(self, parent) :

		## create TGHorizontalFrame to contain board number, firmware version etc.
		if __debug__ :

			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame|ROOT.kRaisedFrame)
		else :
			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame)

		self.fPcrWriteAddrFrame = ROOT.TGGroupFrame(self, " Pixel address ", ROOT.kHorizontalFrame)
		self.fPcrWritePix1Frame = ROOT.TGGroupFrame(self, " TO pixel ",      ROOT.kHorizontalFrame)
		self.fPcrWritePix2Frame = ROOT.TGGroupFrame(self, " BP/PV pixel ",   ROOT.kHorizontalFrame)


		#############################
		##   "write" PCR address   ##
		#############################
		self.fPcrWriteAddrLabelFrame = ROOT.TGVerticalFrame(self.fPcrWriteAddrFrame)
		self.fPcrWriteAddrEntryFrame = ROOT.TGVerticalFrame(self.fPcrWriteAddrFrame)

		self.fPcrWriteAddrLabels = []
		self.fPcrWriteAddrEntries = []

		self.fPcrWriteAddrLabels.append(ROOT.TGLabel(self.fPcrWriteAddrLabelFrame, "PCR"))
		self.fPcrWriteAddrLabels.append(ROOT.TGLabel(self.fPcrWriteAddrLabelFrame, "PR"))
		self.fPcrWriteAddrLabels.append(ROOT.TGLabel(self.fPcrWriteAddrLabelFrame, "DC"))

		self.fPcrWriteAddrLabelFrame.AddFrame(self.fPcrWriteAddrLabels[0], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 0, 0, 5, 0))
		self.fPcrWriteAddrLabelFrame.AddFrame(self.fPcrWriteAddrLabels[1], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 0, 0, 5, 0))
		self.fPcrWriteAddrLabelFrame.AddFrame(self.fPcrWriteAddrLabels[2], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 0, 0, 5, 0))


		## PCR
		self.fPcrWriteAddrEntries.append(ROOT.TGNumberEntry(
			self.fPcrWriteAddrEntryFrame, 0, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 3)
			)

		## PR
		self.fPcrWriteAddrEntries.append(ROOT.TGNumberEntry(
			self.fPcrWriteAddrEntryFrame, 0, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 15)
			)

		## DC
		self.fPcrWriteAddrEntries.append(ROOT.TGNumberEntry(
			self.fPcrWriteAddrEntryFrame, 0, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 31)
			)


		self.fPcrWriteAddrEntryFrame.AddFrame(self.fPcrWriteAddrEntries[0], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 0, 0, 0, 0))
		self.fPcrWriteAddrEntryFrame.AddFrame(self.fPcrWriteAddrEntries[1], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 0, 0, 0, 0))
		self.fPcrWriteAddrEntryFrame.AddFrame(self.fPcrWriteAddrEntries[2], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 0, 0, 0, 0))

		self.fPcrWriteAddrFrame.AddFrame(self.fPcrWriteAddrLabelFrame, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 20, 10, 20, 10))
		self.fPcrWriteAddrFrame.AddFrame(self.fPcrWriteAddrEntryFrame, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 20, 10, 20, 10))

		########################
		##   "write" PCR TO   ##
		########################
		self.fPcrWritePix1FrameL = ROOT.TGGroupFrame(self.fPcrWritePix1Frame, " LEFT ", ROOT.kVerticalFrame)
		self.fPcrWritePix1FrameR = ROOT.TGGroupFrame(self.fPcrWritePix1Frame, " RIGHT ", ROOT.kVerticalFrame)

		self.fPcrWritePix1EnableL = []
		self.fPcrWritePix1EnableR = []

		self.fPcrWritePix1EnableL.append(ROOT.TGCheckButton(self.fPcrWritePix1FrameL, "MASK"))
		self.fPcrWritePix1EnableL.append(ROOT.TGCheckButton(self.fPcrWritePix1FrameL, "CAL_EN"))
		self.fPcrWritePix1EnableL.append(ROOT.TGCheckButton(self.fPcrWritePix1FrameL, "FAST_MODE"))
		self.fPcrWritePix1EnableL.append(ROOT.TGCheckButton(self.fPcrWritePix1FrameL, "SEL_C2F"))
		self.fPcrWritePix1EnableL.append(ROOT.TGCheckButton(self.fPcrWritePix1FrameL, "SEL_C4F"))

		self.fPcrWritePix1EnableR.append(ROOT.TGCheckButton(self.fPcrWritePix1FrameR, "MASK"))
		self.fPcrWritePix1EnableR.append(ROOT.TGCheckButton(self.fPcrWritePix1FrameR, "CAL_EN"))
		self.fPcrWritePix1EnableR.append(ROOT.TGCheckButton(self.fPcrWritePix1FrameR, "FAST_MODE"))
		self.fPcrWritePix1EnableR.append(ROOT.TGCheckButton(self.fPcrWritePix1FrameR, "SEL_C2F"))
		self.fPcrWritePix1EnableR.append(ROOT.TGCheckButton(self.fPcrWritePix1FrameR, "SEL_C4F"))

		self.fPcrWritePix1EnableL[4].SetOn()
		self.fPcrWritePix1EnableR[4].SetOn()

		self.fPcrWritePix1FrameL.AddFrame(self.fPcrWritePix1EnableL[0], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 20, 3))
		self.fPcrWritePix1FrameL.AddFrame(self.fPcrWritePix1EnableL[1], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWritePix1FrameL.AddFrame(self.fPcrWritePix1EnableL[2], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWritePix1FrameL.AddFrame(self.fPcrWritePix1EnableL[3], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWritePix1FrameL.AddFrame(self.fPcrWritePix1EnableL[4], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))

		self.fPcrWritePix1FrameR.AddFrame(self.fPcrWritePix1EnableR[0], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 20, 3))
		self.fPcrWritePix1FrameR.AddFrame(self.fPcrWritePix1EnableR[1], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWritePix1FrameR.AddFrame(self.fPcrWritePix1EnableR[2], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWritePix1FrameR.AddFrame(self.fPcrWritePix1EnableR[3], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWritePix1FrameR.AddFrame(self.fPcrWritePix1EnableR[4], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))



		self.fPcrWritePix1Frame.AddFrame(self.fPcrWritePix1FrameL, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10, 10, 0))
		self.fPcrWritePix1Frame.AddFrame(self.fPcrWritePix1FrameR, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10, 10, 0))


		###########################
		##   "write" PCR BG/PV   ##
		###########################
		self.fPcrWritePix2FrameL = ROOT.TGGroupFrame(self.fPcrWritePix2Frame, " LEFT ", ROOT.kVerticalFrame)
		self.fPcrWritePix2FrameR = ROOT.TGGroupFrame(self.fPcrWritePix2Frame, " RIGHT ", ROOT.kVerticalFrame)

		self.fPcrWritePix2EnableL = []
		self.fPcrWritePix2EnableR = []

		self.fPcrWritePix2EnableL.append(ROOT.TGCheckButton(self.fPcrWritePix2FrameL, "MASK"))
		self.fPcrWritePix2EnableL.append(ROOT.TGCheckButton(self.fPcrWritePix2FrameL, "CAL_EN"))
		self.fPcrWritePix2EnableL.append(ROOT.TGCheckButton(self.fPcrWritePix2FrameL, "GAIN"))
		self.fPcrWritePix2EnableL.append(ROOT.TGCheckButton(self.fPcrWritePix2FrameL, "POWER_DWN"))

		self.fPcrWritePix2EnableR.append(ROOT.TGCheckButton(self.fPcrWritePix2FrameR, "MASK"))
		self.fPcrWritePix2EnableR.append(ROOT.TGCheckButton(self.fPcrWritePix2FrameR, "CAL_EN"))
		self.fPcrWritePix2EnableR.append(ROOT.TGCheckButton(self.fPcrWritePix2FrameR, "GAIN"))
		self.fPcrWritePix2EnableR.append(ROOT.TGCheckButton(self.fPcrWritePix2FrameR, "POWER_DWN"))

		self.fPcrWriteVthFrameL = ROOT.TGHorizontalFrame(self.fPcrWritePix2FrameL, ROOT.kChildFrame)
		self.fPcrWriteVthFrameR = ROOT.TGHorizontalFrame(self.fPcrWritePix2FrameR, ROOT.kChildFrame)

		self.fPcrWriteVthLabelL = ROOT.TGLabel(self.fPcrWriteVthFrameL, "VTH_DAC")
		self.fPcrWriteVthLabelR = ROOT.TGLabel(self.fPcrWriteVthFrameR, "VTH_DAC")

		self.fPcrWriteVthEntryL = ROOT.TGNumberEntry(
			self.fPcrWriteVthFrameL, 8, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**4 -1))

		self.fPcrWriteVthEntryR = ROOT.TGNumberEntry(
			self.fPcrWriteVthFrameR, 8, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**4 -1))


		self.fPcrWriteVthFrameL.AddFrame(self.fPcrWriteVthLabelL, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  2,  0))
		self.fPcrWriteVthFrameL.AddFrame(self.fPcrWriteVthEntryL, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  0,  0))

		self.fPcrWriteVthFrameR.AddFrame(self.fPcrWriteVthLabelR, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  2,  0))
		self.fPcrWriteVthFrameR.AddFrame(self.fPcrWriteVthEntryR, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  0,  0))

		self.fPcrWritePix2FrameL.AddFrame(self.fPcrWritePix2EnableL[0], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 20, 3))
		self.fPcrWritePix2FrameL.AddFrame(self.fPcrWritePix2EnableL[1], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWritePix2FrameL.AddFrame(self.fPcrWritePix2EnableL[2], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWritePix2FrameL.AddFrame(self.fPcrWritePix2EnableL[3], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWritePix2FrameL.AddFrame(self.fPcrWriteVthFrameL,      ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))

		self.fPcrWritePix2FrameR.AddFrame(self.fPcrWritePix2EnableR[0], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 20, 3))
		self.fPcrWritePix2FrameR.AddFrame(self.fPcrWritePix2EnableR[1], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWritePix2FrameR.AddFrame(self.fPcrWritePix2EnableR[2], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWritePix2FrameR.AddFrame(self.fPcrWritePix2EnableR[3], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWritePix2FrameR.AddFrame(self.fPcrWriteVthFrameR,      ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))


		self.fPcrWritePix2Frame.AddFrame(self.fPcrWritePix2FrameL, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10, 10, 0))
		self.fPcrWritePix2Frame.AddFrame(self.fPcrWritePix2FrameR, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10, 10, 10, 0))


		self.AddFrame(self.fPcrWriteAddrFrame, ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 20, 10, 10, 0))
		self.AddFrame(self.fPcrWritePix1Frame, ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 20, 10, 10, 0))
		self.AddFrame(self.fPcrWritePix2Frame, ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 20, 10, 10, 0))


	##________________________________________________________________________________
	def GetPcrValues(self) :
	

		## pixel address
		pixelRegisterAddress = int(self.fPcrWriteAddrEntries[0].GetNumber())
		pixelRegionAddress   = int(self.fPcrWriteAddrEntries[1].GetNumber())
		doubleColumnAddress  = int(self.fPcrWriteAddrEntries[2].GetNumber())

		## TO pixels
		pix1MaskL      = int(self.fPcrWritePix1EnableL[0].IsOn())
		pix1CalEnableL = int(self.fPcrWritePix1EnableL[1].IsOn())
		pix1FastModeL  = int(self.fPcrWritePix1EnableL[2].IsOn())
		pix1SelC2fL    = int(self.fPcrWritePix1EnableL[3].IsOn())
		pix1SelC4fL    = int(self.fPcrWritePix1EnableL[4].IsOn())

		pix1MaskR      = int(self.fPcrWritePix1EnableR[0].IsOn())
		pix1CalEnableR = int(self.fPcrWritePix1EnableR[1].IsOn())
		pix1FastModeR  = int(self.fPcrWritePix1EnableR[2].IsOn())
		pix1SelC2fR    = int(self.fPcrWritePix1EnableR[3].IsOn())
		pix1SelC4fR    = int(self.fPcrWritePix1EnableR[4].IsOn())


		## BG/PV pixels
		pix2MaskL         = int(self.fPcrWritePix2EnableL[0].IsOn())
		pix2CalEnableL    = int(self.fPcrWritePix2EnableL[1].IsOn())
		pix2GainL         = int(self.fPcrWritePix2EnableL[2].IsOn())
		pix2PowerDownL    = int(self.fPcrWritePix2EnableL[3].IsOn())
		pix2ThresholdDacL = int(self.fPcrWriteVthEntryL.GetNumber())
		
		pix2MaskR         = int(self.fPcrWritePix2EnableR[0].IsOn())
		pix2CalEnableR    = int(self.fPcrWritePix2EnableR[1].IsOn())
		pix2GainR         = int(self.fPcrWritePix2EnableR[2].IsOn())
		pix2PowerDownR    = int(self.fPcrWritePix2EnableR[3].IsOn())
		pix2ThresholdDacR = int(self.fPcrWriteVthEntryR.GetNumber())

		PCR_DATA = []

		PCR_DATA.append(pixelRegisterAddress)
		PCR_DATA.append(pixelRegionAddress)
		PCR_DATA.append(doubleColumnAddress)

		PCR_DATA.append(pix1MaskL)
		PCR_DATA.append(pix1CalEnableL)
		PCR_DATA.append(pix1FastModeL)
		PCR_DATA.append(pix1SelC2fL)
		PCR_DATA.append(pix1SelC4fL)

		PCR_DATA.append(pix1MaskR)
		PCR_DATA.append(pix1CalEnableR)
		PCR_DATA.append(pix1FastModeR)
		PCR_DATA.append(pix1SelC2fR)
		PCR_DATA.append(pix1SelC4fR)

		PCR_DATA.append(pix2MaskL)
		PCR_DATA.append(pix2CalEnableL)
		PCR_DATA.append(pix2GainL)
		PCR_DATA.append(pix2PowerDownL)
		PCR_DATA.append(pix2ThresholdDacL)

		PCR_DATA.append(pix2MaskR)
		PCR_DATA.append(pix2CalEnableR)
		PCR_DATA.append(pix2GainR)
		PCR_DATA.append(pix2PowerDownR)
		PCR_DATA.append(pix2ThresholdDacR)

		print PCR_DATA
		#return PCR_DATA



######################################
##   CLASS: PcrWriteDefaultsFrame   ##
######################################

class PcrWriteDefaultsFrame(ROOT.TGHorizontalFrame) :

	##________________________________________________________________________________
	def __init__(self, parent) :

		## create TGHorizontalFrame to contain board number, firmware version etc.
		if __debug__ :

			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame|ROOT.kRaisedFrame)
		else :
			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame)

		self.fPcrWriteDefaultsFrames = []

		self.fPcrWriteDefaultsFrames.append(ROOT.TGGroupFrame(self, " PCR TO1 default ",   ROOT.kVerticalFrame))
		self.fPcrWriteDefaultsFrames.append(ROOT.TGGroupFrame(self, " PCR TO2 default ",   ROOT.kVerticalFrame))
		self.fPcrWriteDefaultsFrames.append(ROOT.TGGroupFrame(self, " PCR BP/PV default ", ROOT.kVerticalFrame))


		self.fPcrWriteTO1DefaultsEnable = []

		self.fPcrWriteTO1DefaultsEnable.append(ROOT.TGCheckButton(self.fPcrWriteDefaultsFrames[0], "MASK"))
		self.fPcrWriteTO1DefaultsEnable.append(ROOT.TGCheckButton(self.fPcrWriteDefaultsFrames[0], "CAL_EN"))
		self.fPcrWriteTO1DefaultsEnable.append(ROOT.TGCheckButton(self.fPcrWriteDefaultsFrames[0], "FAST_MODE"))
		self.fPcrWriteTO1DefaultsEnable.append(ROOT.TGCheckButton(self.fPcrWriteDefaultsFrames[0], "SEL_C2F"))
		self.fPcrWriteTO1DefaultsEnable.append(ROOT.TGCheckButton(self.fPcrWriteDefaultsFrames[0], "SEL_C4F"))

		self.fPcrWriteDefaultsFrames[0].AddFrame(self.fPcrWriteTO1DefaultsEnable[0], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 20, 3))
		self.fPcrWriteDefaultsFrames[0].AddFrame(self.fPcrWriteTO1DefaultsEnable[1], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWriteDefaultsFrames[0].AddFrame(self.fPcrWriteTO1DefaultsEnable[2], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWriteDefaultsFrames[0].AddFrame(self.fPcrWriteTO1DefaultsEnable[3], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWriteDefaultsFrames[0].AddFrame(self.fPcrWriteTO1DefaultsEnable[4], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))

		self.fPcrWriteTO1DefaultsEnable[4].SetOn()


		self.fPcrWriteTO2DefaultsEnable = []

		self.fPcrWriteTO2DefaultsEnable.append(ROOT.TGCheckButton(self.fPcrWriteDefaultsFrames[1], "MASK"))
		self.fPcrWriteTO2DefaultsEnable.append(ROOT.TGCheckButton(self.fPcrWriteDefaultsFrames[1], "CAL_EN"))
		self.fPcrWriteTO2DefaultsEnable.append(ROOT.TGCheckButton(self.fPcrWriteDefaultsFrames[1], "FAST_MODE"))
		self.fPcrWriteTO2DefaultsEnable.append(ROOT.TGCheckButton(self.fPcrWriteDefaultsFrames[1], "SEL_C2F"))
		self.fPcrWriteTO2DefaultsEnable.append(ROOT.TGCheckButton(self.fPcrWriteDefaultsFrames[1], "SEL_C4F"))

		self.fPcrWriteDefaultsFrames[1].AddFrame(self.fPcrWriteTO2DefaultsEnable[0], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 20, 3))
		self.fPcrWriteDefaultsFrames[1].AddFrame(self.fPcrWriteTO2DefaultsEnable[1], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWriteDefaultsFrames[1].AddFrame(self.fPcrWriteTO2DefaultsEnable[2], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWriteDefaultsFrames[1].AddFrame(self.fPcrWriteTO2DefaultsEnable[3], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWriteDefaultsFrames[1].AddFrame(self.fPcrWriteTO2DefaultsEnable[4], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))

		self.fPcrWriteTO2DefaultsEnable[4].SetOn()


		self.fPcrWritePvDefaultsEnable = []

		self.fPcrWritePvDefaultsEnable.append(ROOT.TGCheckButton(self.fPcrWriteDefaultsFrames[2], "MASK"))
		self.fPcrWritePvDefaultsEnable.append(ROOT.TGCheckButton(self.fPcrWriteDefaultsFrames[2], "CAL_EN"))
		self.fPcrWritePvDefaultsEnable.append(ROOT.TGCheckButton(self.fPcrWriteDefaultsFrames[2], "GAIN"))
		self.fPcrWritePvDefaultsEnable.append(ROOT.TGCheckButton(self.fPcrWriteDefaultsFrames[2], "POWER_DWN"))

		self.fPcrWritePvDefaultsVthFrame = ROOT.TGHorizontalFrame(self.fPcrWriteDefaultsFrames[2], ROOT.kChildFrame)

		self.fPcrWritePvDefaultsVthLabel = ROOT.TGLabel(self.fPcrWritePvDefaultsVthFrame, "VTH_DAC")

		self.fPcrWritePvDefaultsVthEntry = ROOT.TGNumberEntry(
			self.fPcrWritePvDefaultsVthFrame, 8, 12, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, (2**4 -1))

		self.fPcrWritePvDefaultsVthFrame.AddFrame(self.fPcrWritePvDefaultsVthLabel, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  2,  0))
		self.fPcrWritePvDefaultsVthFrame.AddFrame(self.fPcrWritePvDefaultsVthEntry, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  0,  0))

		self.fPcrWriteDefaultsFrames[2].AddFrame(self.fPcrWritePvDefaultsEnable[0], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5, 20, 3))
		self.fPcrWriteDefaultsFrames[2].AddFrame(self.fPcrWritePvDefaultsEnable[1], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWriteDefaultsFrames[2].AddFrame(self.fPcrWritePvDefaultsEnable[2], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWriteDefaultsFrames[2].AddFrame(self.fPcrWritePvDefaultsEnable[3], ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))
		self.fPcrWriteDefaultsFrames[2].AddFrame(self.fPcrWritePvDefaultsVthFrame,  ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 5,  3, 3))

		self.AddFrame(self.fPcrWriteDefaultsFrames[0], ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 20, 10, 10, 0))
		self.AddFrame(self.fPcrWriteDefaultsFrames[1], ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 20, 10, 10, 0))
		self.AddFrame(self.fPcrWriteDefaultsFrames[2], ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 20, 10, 10, 0))
