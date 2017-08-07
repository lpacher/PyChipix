
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

import ROOT

class TestCommandsGui( ROOT.TGMainFrame ) :

	## constructor
	def __init__( self, parent, width, height ) :

		mfr = ROOT.TGMainFrame.__init__( self, parent, width, height )

		## set window title
		self.SetWindowName( "CHIPIX DEMO - TestCommands" )

		## connect the 'X' window button to exit
		self.ExitDispatcher = ROOT.TPyDispatcher( self.ExitCallback )
		self.Connect( "CloseWindow()", "TPyDispatcher", self.ExitDispatcher, "Dispatch()" )

		## populate the GUI
		self.MapSubwindows()

		## initialize the layout algorithm via Resize()
		self.Resize( self.GetDefaultSize() )
		
		## pop-up the main frame
		self.MapWindow()
		self.Resize(width, height)

		## fixed size
		#self.SetWMSize( self.GetDefaultWidth(), self.GetDefaultHeight() )
		#self.SetWMSizeHints( self.GetDefaultWidth(), self.GetDefaultHeight(), self.GetDefaultWidth(), self.GetDefaultHeight(), 1, 1 )
		self.SetWMSizeHints( width, height, width, height, 1, 1 )

	##_________________________________________________________________


	## destructor
	def __del__( self ) :
		self.Cleanup()
		self.DeleteWindow()


	def ExitCallback( self ) :
		ROOT.gApplication.Terminate(0)
		raise SystemExit
