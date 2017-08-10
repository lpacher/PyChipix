
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

## import ROOT components
import ROOT

## custom classes
from CommonFrame import MenuBar, CommonFrame

class TestCommandsGui( ROOT.TGMainFrame ) :

	"""TestCommandsGui class. Used to debug all basic operations."""

	##________________________________________________________________________________
	def __init__( self, w=1300, h=800) :

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
		self.fCommonFrame = CommonFrame(self)

		## create tabs
		self.fTabsFrame = ROOT.TGTab(self)
		self.fTabsFrame.DrawBorder()

		self.fFpgaTab = self.fTabsFrame.AddTab("   FPGA   ") ;   self.fFpgaTab.ChangeOptions(ROOT.kHorizontalFrame) ;   self.buildFpgaTab()
		self.fSpiTab  = self.fTabsFrame.AddTab("   SPI    ")
		self.fGcrTab  = self.fTabsFrame.AddTab("   GCR    ")
		self.fEccrTab = self.fTabsFrame.AddTab("   ECCR   ")
		self.fPcrTab  = self.fTabsFrame.AddTab("   PCR    ")
		self.fAdcTab  = self.fTabsFrame.AddTab("   ADC    ") ;   self.fAdcTab.ChangeOptions(ROOT.kHorizontalFrame) ;   self.buildAdcTab()


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
		raise SystemExi


	##________________________________________________________________________________
	def buildFpgaTab(self) :
	
		self.fFpgaTabVerticalFrames = [] 

		self.fFpgaTabVerticalFrames.append(ROOT.TGVerticalFrame(self.fFpgaTab, 0, 0, ROOT.kChildFrame))
		self.fFpgaTabVerticalFrames.append(ROOT.TGVerticalFrame(self.fFpgaTab, 0, 0, ROOT.kChildFrame))
		self.fFpgaTabVerticalFrames.append(ROOT.TGVerticalFrame(self.fFpgaTab, 0, 0, ROOT.kChildFrame))
		self.fFpgaTabVerticalFrames.append(ROOT.TGVerticalFrame(self.fFpgaTab, 0, 0, ROOT.kChildFrame))


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

		#self.fFpgaTabVerticalFrames[1].AddFrame(
		#self.fFpgaTabVerticalFrames[1].AddFrame(
		#self.fFpgaTabVerticalFrames[1].AddFrame(
		#self.fFpgaTabVerticalFrames[1].AddFrame(



		############################
		##   middle-right frame   ##
		############################

		self.fResetClkCountersButton     = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[2], "Reset clock counters")
		self.fSetBoardLinesButton        = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[2], "Set board lines")
		self.fWaitDelayButton            = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[2], "Wait delay")
		self.fReadTxFifoDataCountButton  = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[2], "Read TX data FIFO data count")
		self.fReadTxFifoButton           = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[2], "Read TX FIFO")
		self.fReadTxFifoCountMaxButton   = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[2], "Read TX FIFO count max.")
		self.fFlushTxFifoButton          = ROOT.TGTextButton(self.fFpgaTabVerticalFrames[2], "Fush TX FIFO")
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




		#self.fFpgaTabVerticalFrames[3].AddFrame(
		#self.fFpgaTabVerticalFrames[3].AddFrame(
		#self.fFpgaTabVerticalFrames[3].AddFrame(
		#self.fFpgaTabVerticalFrames[3].AddFrame(

		self.fFpgaTab.AddFrame(self.fFpgaTabVerticalFrames[0], ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 10, 10, 20, 10))
		self.fFpgaTab.AddFrame(self.fFpgaTabVerticalFrames[1], ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 10, 10, 20, 10))
		self.fFpgaTab.AddFrame(self.fFpgaTabVerticalFrames[2], ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 10, 10, 20, 10))
		self.fFpgaTab.AddFrame(self.fFpgaTabVerticalFrames[3], ROOT.TGLayoutHints(ROOT.kLHintsExpandY, 10, 10, 20, 10))

		print type(self.fFpgaTab)


	##________________________________________________________________________________
	def buildSpiTab(self) :
		pass

	##________________________________________________________________________________
	def buidGcrTab(self) :
		pass

	##________________________________________________________________________________
	def buildEccrTab(self) :
		pass

	##________________________________________________________________________________
	def buildGcrTab(self) :
		pass

	##________________________________________________________________________________
	def buildAdcTab(self) :

		self.fReadAdcButton = ROOT.TGTextButton(self.fAdcTab, "Read ADC")
		self.fReadAdcButton.SetMargins(10, 10, 1, 1)

		self.fAdcEocDelayLabel = ROOT.TGLabel(self.fAdcTab, "ADC EOC delay (ms)")

		self.fAdcEocDelayEntry = ROOT.TGNumberEntry(
			self.fAdcTab, 99999, 10, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 99999)

		self.fAdcCodeLabel = ROOT.TGLabel(self.fAdcTab, "Returned ADC code")
		self.fAdcCodeText  = ROOT.TGTextEntry(self.fAdcTab)


		#self.fAdcCodeFrame.AddFrame(self.fAdcCodeLabel, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 5, 0, 5, 5))

		self.fAdcTab.AddFrame(self.fReadAdcButton,    ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 15,  50, 30,  0)) 
		self.fAdcTab.AddFrame(self.fAdcEocDelayLabel, ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10,  10, 33,  0)) 
		self.fAdcTab.AddFrame(self.fAdcEocDelayEntry, ROOT.TGLayoutHints(ROOT.kLHintsNoHints,  5,  10, 30,  0))
		self.fAdcTab.AddFrame(self.fAdcCodeLabel,     ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 35,  10, 33, 10))
		self.fAdcTab.AddFrame(self.fAdcCodeText,      ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 10,  50, 30, 10))



