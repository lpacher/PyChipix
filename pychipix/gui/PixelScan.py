
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

## import ROOT components
import ROOT

## custom classes
from CommonFrames import MenuBar, ConnectionFrame
from connection import Connection


class PixelScanGui(ROOT.TGMainFrame, Connection) :

	"""PixelScanGui class. Used to perform either fixed-threshold\ncharge-scans or fixed-charge threshold scans."""

	##________________________________________________________________________________
	def __init__(self, w=1600, h=950) :

		"""constructor"""

		## **DEBUG
		print "Starting PixelScan GUI..."


		## load GUI style
		ROOT.gApplication.ExecuteFile("./lib/style.cxx")
		#ROOT.gROOT.ProcessLine("./lib/style.cxx")


		## window size
		self.fWidth  = w
		self.fHeight = h

		## create a TGMainFrame top-level window
		ROOT.TGMainFrame.__init__(self, ROOT.gClient.GetRoot(), self.fWidth, self.fHeight, ROOT.kMainFrame|ROOT.kVerticalFrame)

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

		## set the initial state of the window (either ROOT.kNormalState or ROOT.kIconicState)
		#self.SetWMState(ROOT.kIconicState)
		self.SetWMState(ROOT.kNormalState)


		#########################
		##   internal frames   ##
		#########################

		## insert menu bar and common frame (board number, firmware version, etc.)
		self.fMenuBar = MenuBar(self)
		self.fConnectionFrame = ConnectionFrame(self)


		## create "Settings", "Measurement" and "Pixel map" tabs
		self.fTabsFrame = ROOT.TGTab(self)
		self.fTabsFrame.DrawBorder()

		self.fSettingsTab    = self.fTabsFrame.AddTab("   Settings   ")
		self.fMeasurementTab = self.fTabsFrame.AddTab("   Measurement   ")
		self.fPixelMapTab    = self.fTabsFrame.AddTab("   Pixel map    ")

		## build tabs using custom class methods
		self.buildSettingsTab()
		self.buildMeasurementTab()
		self.buildPixelMapTab()


		## TGlabels

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

		"""
		self.TPmodeEntry = ROOT.TGNumberEntry(
			self.measurementTab, 0, 9, 999,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 7)

		self.TPphaseEntry = ROOT.TGNumberEntry(
			self.measurementTab, 0, 9, 999,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 7)

		self.TPframeDelayEntry = ROOT.TGNumberEntry(
			self.measurementTab, 0, 9, 999,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 7)

		self.TPnumPulsesEntry = ROOT.TGNumberEntry(
			self.measurementTab, 0, 9, 999,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 7)

		self.TPframeIntervalEntry = ROOT.TGNumberEntry(
			self.measurementTab, 0, 9, 999,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 7)

		self.TPdebugWidthEntry = ROOT.TGNumberEntry(
			self.measurementTab, 0, 9, 999,
			ROOT.TGNumberFormat.kNESInteger,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 7)




		"""

		#########################################
		##   frame insertion and positioning   ##
		#########################################

		self.AddFrame(self.fMenuBar,         ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 10, 0))
		self.AddFrame(self.fConnectionFrame, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 5, 5, 10, 0))
		self.AddFrame(self.fTabsFrame,       ROOT.TGLayoutHints(ROOT.kLHintsExpandX|ROOT.kLHintsExpandY, 10, 10, 15, 10))


		"""
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
		"""
		###############################
		##   callbacks dispatchers   ##
		###############################

		## connect the 'X' window button to exit
		self.DoExitDispatcher = ROOT.TPyDispatcher( self.DoExitCallback )

		self.CloseWindowDispatcher = ROOT.TPyDispatcher(self.MyCloseWindow)



		#########################################################
		##   map dispatched callbacks to buttons and widgets   ##
		#########################################################

		## exit/quit
		self.Connect            ("CloseWindow()", "TPyDispatcher", self.CloseWindowDispatcher, "Dispatch()")
		#self.exitButton.Connect ("Clicked()",     "TPyDispatcher", self.DoExitDispatcher, "Dispatch()")


		#self.fFilePopupMenu.Connect()


		## show the gui
		self.popup()


	##________________________________________________________________________________
	def __del__( self ) :
		"""destructor"""
		self.Cleanup()
		self.DeleteWindow()




	##________________________________________________________________________________
	def MyCloseWindow( self ) :

		self.CloseWindow()

		ROOT.gROOT.SetStyle("Plain")
		ROOT.gROOT.Reset()


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
	def DoExitCallback( self ) :

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

	##________________________________________________________________________________
	def buildSettingsTab(self) :
			pass
			#print "Test passed"


	##________________________________________________________________________________
	def buildMeasurementTab(self) :

		## TGVerticalFrames
		#self.f


		## TRootEmbeddedCanvas
		self.fRootEmbeddedCanvas = ROOT.TRootEmbeddedCanvas("fRootEmbeddedCanvas", self.fMeasurementTab, 1200, 500)
		self.fMeasurementTab.AddFrame(self.fRootEmbeddedCanvas, ROOT.TGLayoutHints(ROOT.kLHintsExpandX, 10, 10, 100, 10))



	##________________________________________________________________________________
	def buildPixelMapTab(self) :
		pass
