
import ROOT

class TestCommandsGui( ROOT.TGMainFrame ) :

	## constructor
	def __init__( self, parent, width, height ) :

		fr = ROOT.TGMainFrame.__init__( self, parent, width, height )



		## set window title
		self.SetWindowName( "CHIPIX DEMO - TestCommands" )

		## populate the GUI
		self.MapSubwindows()

		## initialize the layout algorithm via Resize()
		self.Resize( self.GetDefaultSize() )
		
		## pop-up the main frame
		self.MapWindow()
		self.Resize(width, height)

		self.CloseWindowDispatcher = ROOT.TPyDispatcher( self.CloseWindow )
                self.Connect( "CloseWindow()", "TPyDispatcher", self.CloseWindowDispatcher, "Dispatch()" )

	##_________________________________________________________________


	## destructor
	def __del__( self ) :
		self.Cleanup()


	def CloseWindow( self ) :
		ROOT.gApplication.Terminate(0)
		raise SystemExit
