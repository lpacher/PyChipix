
#----------------------------------------------------------------------------------------------------
#                                        VLSI Design Laboratory
#                               Istituto Nazionale di Fisica Nucleare (INFN)
#                                   via Giuria 1 10125, Torino, Italy
#----------------------------------------------------------------------------------------------------
# {Trace}
# [Filename]      PixelScan.py [CLASS]
# [Project]       CHIPIX65 demonstrator PyROOT-based DAQ
# [Author]        Luca Pacher - pacher@to.infn.it
# [Version]       1.0
# [Language]      Python/ROOT
# [Created]       Aug 5, 2017
# [Description]   PixelScan GUI class
# [Notes]         -
# {Trace}
#----------------------------------------------------------------------------------------------------

import ROOT

class PixelScanGui(ROOT.TGMainFrame) :

	"""PixelScanGui class. Used to perform either fixed-threshold\ncharge-scans or fixed-charge threshold scans."""

	##________________________________________________________________________________
	def __init__(self, w=1300, h=800) :

		## window size
		self.fWidth  = w
		self.fHeight = h

		## create a TGMainFrame top-level window
		ROOT.TGMainFrame.__init__(self, ROOT.gClient.GetRoot(), self.fWidth, self.fHeight, ROOT.kVerticalFrame)

		## turn on automatic cleanup in this frame and and all child frames (hierarchical)
		self.SetCleanup(ROOT.kDeepCleanup)

		## give a position hint at startup
		#xStart = 100
		#yStart = 100
		#self.SetWMPosition(xStart, yStart)

		## use INFN logo for window icon
		#self.SetIconPixmap("./INFN.gif")

		## set top-level window name
		self.SetWindowName("INFN Torino / CHIPIX DEMO - PixelScan")

		## give the window manager minimum and maximum size hints
		self.SetWMSizeHints(self.fWidth, self.fHeight, self.fWidth, self.fHeight, 1, 1)   ## **NOTE: fixed-size hints

		## set the initial state of the window (either kNormalState or kIconicState)
		#self.SetWMState(ROOT.kIconicState)
		self.SetWMState(ROOT.kNormalState)


		#########################
		##   internal frames   ##
		#########################

		## menu-bar frame (File Edit, etc.)
		self.fMenuBarFrame = ROOT.TGHorizontalFrame(self, self.fWidth, 10, ROOT.kHorizontalFrame, ROOT.kChildFrame)

		## common frame (board-number, timeout etc.)
		self.fCommonFrame = ROOT.TGHorizontalFrame(self, self.fWidth, 10, ROOT.kHorizontalFrame, ROOT.kChildFrame)

		## "Settings" and "Measurement" frames
		self.fTabsFrame = ROOT.TGTab(self, 650, 10)
		self.fTabsFrame.DrawBorder()

		self.settingsTab    = self.fTabsFrame.AddTab("Settings")
		self.measurementTab = self.fTabsFrame.AddTab("Measurement")


		self.AddFrame(self.fMenuBarFrame, ROOT.TGLayoutHints(ROOT.kLHintsExpandX|ROOT.kLHintsExpandY, 0, 0, 0, 0) )
		self.AddFrame(self.fCommonFrame,  ROOT.TGLayoutHints(ROOT.kLHintsExpandX|ROOT.kLHintsExpandY, 0, 0, 30, 0) )
		self.AddFrame(self.fTabsFrame,     ROOT.TGLayoutHints(ROOT.kLHintsExpandX|ROOT.kLHintsExpandY, 0, 0, 30, 0) )


		##############################################
		##   declare here all buttons and widgets   ##
		##############################################

		## add a menu-bar at the top of the window
		self.fMenuBar = ROOT.TGMenuBar(self.fMenuBarFrame, 1, 10, ROOT.kHorizontalFrame)

		self.fMenuBar.AddPopup("&File")
		self.fMenuBar.AddPopup("&Edit")
		self.fMenuBar.AddPopup("&View")
		self.fMenuBar.AddPopup("&Options")
		self.fMenuBar.AddPopup("&Tools")
		self.fMenuBar.AddPopup("&Help")

		#self.popupMenuTools = ROOT.TGPopupMenu(ROOT.gClient.GetRoot());

		## TGTextButtons
		self.exitButton       = ROOT.TGTextButton(self.fCommonFrame, "&Quit"      ) ;   self.exitButton.SetMargins       (10, 10, 1, 1)
		self.connectButton    = ROOT.TGTextButton(self.fCommonFrame, "&Connect"   ) ;   self.connectButton.SetMargins    (10, 10, 1, 1)
		self.disconnectButton = ROOT.TGTextButton(self.fCommonFrame, "&Disconnect") ;   self.disconnectButton.SetMargins (10, 10, 1, 1)
		#self.startScanButton
		#self.loadDataButton

		## TGlabels
		self.boardNumberLabel      = ROOT.TGLabel(self.fCommonFrame, "Board number")
		self.timeoutLabel          = ROOT.TGLabel(self.fCommonFrame, "Timeout (ms)")
		self.firmwareVersionLabel  = ROOT.TGLabel(self.fCommonFrame, "Firmware version")

		#self.TPmodeLabel
		#self.TPphaseLabel
		#self.TPframeDelayLabel
		#self.TPnumPulsesLabel
		#self.TPframeIntervalLabel
		#self.TPdebugWidthlabel

		#self.triggerDelayLabel
		#self.firstPixelLabel
		#self.lastPixelLabel
		#self.pixelStepLabel


		## TGNumberEntry
		self.boardNumberEntry = ROOT.TGNumberEntry(
			self.fCommonFrame, 0, 10, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 7)

		self.timeoutEntry = ROOT.TGNumberEntry(
			self.fCommonFrame, 1000, 10, -1,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 10000)

		self.firmwareVersionEntry = ROOT.TGNumberEntry(
			self.fCommonFrame, 0, 9, 999,
			ROOT.TGNumberFormat.kNESHex,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 65535)

		self.TPmodeEntry           = ROOT.TGNumberEntry(self.measurementTab, 0, 9, 999, ROOT.TGNumberFormat.kNESInteger, ROOT.TGNumberFormat.kNEANonNegative, ROOT.TGNumberFormat.kNELLimitMinMax, 0, 7      )
		self.TPphaseEntry          = ROOT.TGNumberEntry(self.measurementTab, 0, 9, 999, ROOT.TGNumberFormat.kNESInteger, ROOT.TGNumberFormat.kNEANonNegative, ROOT.TGNumberFormat.kNELLimitMinMax, 0, 7      )
		self.TPframeDelayEntry     = ROOT.TGNumberEntry(self.measurementTab, 0, 9, 999, ROOT.TGNumberFormat.kNESInteger, ROOT.TGNumberFormat.kNEANonNegative, ROOT.TGNumberFormat.kNELLimitMinMax, 0, 7      )
		self.TPnumPulsesEntry      = ROOT.TGNumberEntry(self.measurementTab, 0, 9, 999, ROOT.TGNumberFormat.kNESInteger, ROOT.TGNumberFormat.kNEANonNegative, ROOT.TGNumberFormat.kNELLimitMinMax, 0, 7      )
		self.TPframeIntervalEntry  = ROOT.TGNumberEntry(self.measurementTab, 0, 9, 999, ROOT.TGNumberFormat.kNESInteger, ROOT.TGNumberFormat.kNEANonNegative, ROOT.TGNumberFormat.kNELLimitMinMax, 0, 7      )
		self.TPdebugWidthEntry     = ROOT.TGNumberEntry(self.measurementTab, 0, 9, 999, ROOT.TGNumberFormat.kNESInteger, ROOT.TGNumberFormat.kNEANonNegative, ROOT.TGNumberFormat.kNELLimitMinMax, 0, 7      )

		## TRootEmbeddedCanvas
		self.rootEmbeddedCanvas = ROOT.TRootEmbeddedCanvas("cvs", self.measurementTab, 1200, 500)


		#########################################
		##   frame insertion and positioning   ##
		#########################################

		## menu bar
		self.AddFrame(self.fMenuBar, ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft, 5, 5, 10, 50) )


		## common frame

		self.fCommonFrame.AddFrame(self.boardNumberLabel,     ROOT.TGLayoutHints( ROOT.kLHintsTop,  20, 10, 0, 0) )
		self.fCommonFrame.AddFrame(self.boardNumberEntry,     ROOT.TGLayoutHints( ROOT.kLHintsTop,   0, 10, 0, 0) )
		self.fCommonFrame.AddFrame(self.timeoutLabel,         ROOT.TGLayoutHints( ROOT.kLHintsTop,  20, 10, 0, 0) )
		self.fCommonFrame.AddFrame(self.timeoutEntry,         ROOT.TGLayoutHints( ROOT.kLHintsTop,   0, 10, 0, 0) )
		self.fCommonFrame.AddFrame(self.firmwareVersionLabel, ROOT.TGLayoutHints( ROOT.kLHintsTop,  20, 10, 0, 0) )
		self.fCommonFrame.AddFrame(self.firmwareVersionEntry, ROOT.TGLayoutHints( ROOT.kLHintsTop,   0, 10, 0, 0) )
		self.fCommonFrame.AddFrame(self.connectButton,        ROOT.TGLayoutHints( ROOT.kLHintsTop,  20, 10, 0, 0) )
		self.fCommonFrame.AddFrame(self.disconnectButton,     ROOT.TGLayoutHints( ROOT.kLHintsTop,  20, 10, 0, 0) )
		self.fCommonFrame.AddFrame(self.exitButton,           ROOT.TGLayoutHints( ROOT.kLHintsTop, 200, 10, 0, 0) )

		self.measurementTab.AddFrame(self.rootEmbeddedCanvas, ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsBottom, 10, 0, 0, 15) )





		self.rootEmbeddedCanvas.GetCanvas().Divide(3,3)
		#self.rootEmbeddedCanvas.GetCanvas().SetGrid()
		#self.rootEmbeddedCanvas.GetCanvas().SetFillColor(ROOT.kBlack)

		#self.h = ROOT.TH1F()
		self.h1 = ROOT.TH1F("h1","h", 100, -5, 5) ; self.h1.FillRandom("gaus", 1000)
		self.h2 = ROOT.TH1F("h2","h", 100, -5, 5) ; self.h2.FillRandom("gaus", 1000)
		self.h3 = ROOT.TH1F("h3","h", 100, -5, 5) ; self.h3.FillRandom("gaus", 1000)
		self.h4 = ROOT.TH1F("h4","h", 100, -5, 5) ; self.h4.FillRandom("gaus", 1000)
		self.h5 = ROOT.TH1F("h5","h", 100, -5, 5) ; self.h5.FillRandom("gaus", 1000)
		self.h6 = ROOT.TH1F("h6","h", 100, -5, 5) ; self.h6.FillRandom("gaus", 1000)
		self.h7 = ROOT.TH1F("h7","h", 100, -5, 5) ; self.h7.FillRandom("gaus", 1000)
		self.h8 = ROOT.TH1F("h8","h", 100, -5, 5) ; self.h8.FillRandom("gaus", 1000)
		self.h9 = ROOT.TH1F("h9","h", 100, -5, 5) ; self.h9.FillRandom("gaus", 1000)

		self.rootEmbeddedCanvas.GetCanvas().cd(1) ; self.h1.Draw()
		self.rootEmbeddedCanvas.GetCanvas().cd(2) ; self.h2.Draw()
		self.rootEmbeddedCanvas.GetCanvas().cd(3) ; self.h3.Draw()
		self.rootEmbeddedCanvas.GetCanvas().cd(4) ; self.h4.Draw()
		self.rootEmbeddedCanvas.GetCanvas().cd(5) ; self.h5.Draw()
		self.rootEmbeddedCanvas.GetCanvas().cd(6) ; self.h6.Draw()
		self.rootEmbeddedCanvas.GetCanvas().cd(7) ; self.h7.Draw()
		self.rootEmbeddedCanvas.GetCanvas().cd(8) ; self.h8.Draw()
		self.rootEmbeddedCanvas.GetCanvas().cd(9) ; self.h9.Draw()


		#self.rootEmbeddedCanvas.GetCanvas().ForceUpdate()


		#ROOT.gPad.Update()


		#self.topFrame.AddFrame(self.rootEmbeddedCanvas, ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft, 500, 100, 100, 100))

		###############################
		##   callbacks dispatchers   ##
		###############################

		## connect the 'X' window button to exit
		self.ExitDispatcher = ROOT.TPyDispatcher( self.exitCallback )



		#########################################################
		##   map dispatched callbacks to buttons and widgets   ##
		#########################################################

		## exit/quit
		self.Connect            ("CloseWindow()", "TPyDispatcher", self.ExitDispatcher, "Dispatch()")
		self.exitButton.Connect ("Clicked()",     "TPyDispatcher", self.ExitDispatcher, "Dispatch()")



		## show the gui
		self.popup()


	##________________________________________________________________________________
	def __del__( self ) :
		self.Cleanup()
		self.DeleteWindow()

	##________________________________________________________________________________
	def popup(self) :

		## populate the GUI
		self.MapSubwindows()

		## initialize the layout algorithm via Resize()
		self.Resize( self.GetDefaultSize() )
		
		## pop-up the main frame
		self.MapWindow()
		#self.Resize( width, height )

		## fixed size
		#self.SetWMSize( self.GetDefaultWidth(), self.GetDefaultHeight() )
		#self.SetWMSizeHints( self.GetDefaultWidth(), self.GetDefaultHeight(), self.GetDefaultWidth(), self.GetDefaultHeight(), 1, 1 )
		#self.SetWMSizeHints( width, height, width, height, 1, 1 )

	##________________________________________________________________________________
	def exitCallback( self ) :

		## close the main ROOT TApplication event loop
		print "Bye!"
		self.SendCloseMessage()
		ROOT.gApplication.Terminate(0)
		raise SystemExit

	##________________________________________________________________________________
	def getBoardNumber(self) :
		self.BOARD_NUMBER = self.boardNumberEntry.GetNumberEntry().GetIntNumber()
		return self.BOARD_NUMBER
	##________________________________________________________________________________
	def getTimeout(self) :
		self.TIMEOUT = self.timeoutEntry.GetNumberEntry().GetIntNumber()
		return self.TIMEOUT

	##________________________________________________________________________________
	def getFirmwareVersion(self) :
		self.FIRMWARE_VERSION = self.firmwareVersionEntry.GetNumberEntry().GetHexNumber()
		return self.FIRMWARE_VERSION

