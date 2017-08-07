
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

	##________________________________________________________________________________
	def __init__(self, parent, width, height) :

		## create a TGMainFrame top level window
		ROOT.TGMainFrame.__init__(self, parent, width, height)

		## use hierarchical cleaning
		self.SetCleanup(ROOT.kDeepCleanup)

		## set window title
		self.SetWindowName( "CHIPIX DEMO - PixelScan" )

		self.menuBar = ROOT.TGMenuBar(self, 1, 10, ROOT.kHorizontalFrame);
		self.menuBar.AddPopup("&File")
		self.menuBar.AddPopup("&Edit")
		self.menuBar.AddPopup("&View")
		self.menuBar.AddPopup("&Options")
		self.menuBar.AddPopup("&Tools")
		self.menuBar.AddPopup("&Help")
		self.AddFrame(self.menuBar, ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft, 5, 5, 10, 50) )



		self.popupMenuTools = ROOT.TGPopupMenu(ROOT.gClient.GetRoot());


		## frames
		#self.topFrame = ROOT.TGHorizontalFrame(self, width, height, ROOT.kHorizontalFrame )

		self.plotsCanvas = ROOT.TRootEmbeddedCanvas("cvs", self, 1200, 600)
		self.AddFrame(self.plotsCanvas, ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft, 50, 0, 180, 50) )

		self.plotsCanvas.GetCanvas().Divide(3,3)
		self.plotsCanvas.GetCanvas().SetGrid()
		#self.plotsCanvas.GetCanvas().SetFillColor(ROOT.kBlack)

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

		self.plotsCanvas.GetCanvas().cd(1) ; self.h1.Draw()
		self.plotsCanvas.GetCanvas().cd(2) ; self.h2.Draw()
		self.plotsCanvas.GetCanvas().cd(3) ; self.h3.Draw()
		self.plotsCanvas.GetCanvas().cd(4) ; self.h4.Draw()
		self.plotsCanvas.GetCanvas().cd(5) ; self.h5.Draw()
		self.plotsCanvas.GetCanvas().cd(6) ; self.h6.Draw()
		self.plotsCanvas.GetCanvas().cd(7) ; self.h7.Draw()
		self.plotsCanvas.GetCanvas().cd(8) ; self.h8.Draw()
		self.plotsCanvas.GetCanvas().cd(9) ; self.h9.Draw()


		#self.plotsCanvas.GetCanvas().ForceUpdate()


		#ROOT.gPad.Update()


		#self.topFrame.AddFrame(self.plotsCanvas, ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft, 500, 100, 100, 100))


		## dispatchers

		## connect the 'X' window button to exit
		self.ExitDispatcher = ROOT.TPyDispatcher( self.ExitCallback )



		## map dispatched callbacks to buttons etc.
		self.Connect( "CloseWindow()", "TPyDispatcher", self.ExitDispatcher, "Dispatch()" )


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
	def ExitCallback( self ) :

		## close the ROOT TApplication
		print "Bye!"
		ROOT.gApplication.Terminate(0)
		raise SystemExit
