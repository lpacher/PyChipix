
import ROOT

## **NOTA! Potrebbe essere carino aggiungere anche due text entries per monitorare l'IP
##  della macchina e la porta 10000 da usare per la connessione UDP!
#
# socket.gethostbyname(socket.gethostname()) => cross-platform, ritorna l'IP della macchina!

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


class CommonFrame(ROOT.TGHorizontalFrame) :

	##________________________________________________________________________________
	def __init__(self, parent) :

		## create TGHorizontalFrame to contain board number, firmware version etc.

		if __debug__ :

			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame|ROOT.kRaisedFrame)
		else :
			ROOT.TGHorizontalFrame.__init__(self, parent, 0, 0, ROOT.kChildFrame)



		## TGTextButtons
		self.fExitButton       = ROOT.TGTextButton(self, "&Quit"      ) ;   self.fExitButton.SetMargins       (10, 10, 1, 1)
		self.fConnectButton    = ROOT.TGTextButton(self, "&Connect"   ) ;   self.fConnectButton.SetMargins    (10, 10, 1, 1)
		self.fDisconnectButton = ROOT.TGTextButton(self, "&Disconnect") ;   self.fDisconnectButton.SetMargins (10, 10, 1, 1)


		## TGlabels
		self.fBoardNumberLabel      = ROOT.TGLabel(self, "Board number")
		self.fTimeoutLabel          = ROOT.TGLabel(self, "Timeout (ms)")
		self.fFirmwareVersionLabel  = ROOT.TGLabel(self, "Firmware version")


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

		self.fFirmwareVersionEntry = ROOT.TGNumberEntry(
			self, 0, 9, 999,
			ROOT.TGNumberFormat.kNESHex,
			ROOT.TGNumberFormat.kNEANonNegative,
			ROOT.TGNumberFormat.kNELLimitMinMax, 0, 65535)

		self.AddFrame(self.fBoardNumberLabel,     ROOT.TGLayoutHints(ROOT.kLHintsNoHints,   5,  5, 8, 5))
		self.AddFrame(self.fBoardNumberEntry,     ROOT.TGLayoutHints(ROOT.kLHintsNoHints,   5, 15, 5, 5))
		self.AddFrame(self.fTimeoutLabel,         ROOT.TGLayoutHints(ROOT.kLHintsNoHints,   5,  5, 8, 5))
		self.AddFrame(self.fTimeoutEntry,         ROOT.TGLayoutHints(ROOT.kLHintsNoHints,   5, 15, 5, 5))
		self.AddFrame(self.fFirmwareVersionLabel, ROOT.TGLayoutHints(ROOT.kLHintsNoHints,   5,  5, 8, 5))
		self.AddFrame(self.fFirmwareVersionEntry, ROOT.TGLayoutHints(ROOT.kLHintsNoHints,   5, 15, 5, 5))
		self.AddFrame(self.fConnectButton,        ROOT.TGLayoutHints(ROOT.kLHintsNoHints,  50,  5, 5, 5))
		self.AddFrame(self.fDisconnectButton,     ROOT.TGLayoutHints(ROOT.kLHintsNoHints,   5,  5, 5, 5))
		self.AddFrame(self.fExitButton,           ROOT.TGLayoutHints(ROOT.kLHintsNoHints, 400,  5, 5, 5))


		self.DoExitDispatcher = ROOT.TPyDispatcher(self.DoExitCallback)
		self.fExitButton.Connect("Clicked()", "TPyDispatcher", self.DoExitDispatcher, "Dispatch()")


	##________________________________________________________________________________
	def DoExitCallback(self) :

		## close the main ROOT TApplication event loop
		print "Bye!"
		ROOT.gApplication.Terminate(0)
		raise SystemExit

