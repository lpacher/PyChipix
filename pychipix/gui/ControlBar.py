
#----------------------------------------------------------------------------------------------------
#                                        VLSI Design Laboratory
#                               Istituto Nazionale di Fisica Nucleare (INFN)
#                                   via Giuria 1 10125, Torino, Italy
#----------------------------------------------------------------------------------------------------
# {Trace}
# [Filename]      CommonFrame.py [CLASS]
# [Project]       CHIPIX65 demonstrator PyROOT-based DAQ
# [Author]        Luca Pacher - pacher@to.infn.it
# [Version]       1.0
# [Language]      Python/ROOT
# [Created]       Aug 31, 2017
# [Description]   Main control bar GUI class
# [Notes]         -
# {Trace}
#----------------------------------------------------------------------------------------------------


## ROOT components
try :
	import ROOT

except ImportError :

	print("\n**ERROR: ROOT components are required to run this application!\n")

	if( os.name == 'nt') :
		print("           call %ROOTSYS%\bin\thisroot.bat might solve this problem.\n")
	else :
		print("           source $ROOTSYS/bin/thisroot.(c)sh might solve this problem.\n")

	raise SystemExit



class ControlBar(ROOT.TControlBar) :

	def __init__(self) :

		ROOT.gStyle.SetScreenFactor(1.4)


		xStart = 1000   ## pixels from left of the screen
		yStart = 100    ## pixels from top of the screen

		ROOT.TControlBar.__init__(self, "vertical", "", xStart, yStart) 


		self.SetButtonWidth(150)

		self.AddButton("     Help     ", r'TPython::Exec(                                          ) ;', " Display detailed help      ") 
		self.AddButton(" ROOT browser ", r'TPython::Exec("b = ROOT.TBrowser()"                     ) ;', " Launch a TBrowser instance ")
		self.AddButton("   Connect    ", r'TPython::Exec("connect()"                               ) ;', " Connect to target FPGA     ")
		self.AddButton("  Disconnect  ", r'TPython::Exec("disconnect()"                            ) ;', " Disconnect from FPGA       ")
		self.AddButton("    Reset     ", r'TPython::Exec("reset()"                                 ) ;', " Reset the chip             ")
		self.AddButton("Test commands ", r'TPython::Exec("GUI.TestCommandsGui = TestCommandsGui()" ) ;', " Implements TestCommands.vi ")
		self.AddButton("  Pixel scan  ", r'TPython::Exec("GUI.PixelScanGui    = PixelScanGui()"    ) ;', " Implements PixelScan.vi    ")
		self.AddButton("Sensor readout", r'TPython::Exec(                                          ) ;', "                            ")
		self.AddButton("Remote control", r'TPython::Exec(                                          ) ;', "                            ") 
		self.AddButton("  Scan chain  ", r'TPython::Exec(                                          ) ;', "                            ")

		self.AddButton("    ...       ", "", "")
		self.AddButton("    ...       ", "", "")
		self.AddButton("    ...       ", "", "")
		self.AddButton("    ...       ", "", "")
		self.AddButton("    ...       ", "", "")
		self.AddButton("    ...       ", "", "")


		## **NOTE: not implemeted in PyROOT
		#self.AddSeparator()

		self.AddButton("  Close bar   ", r'TPython::Exec("closeBar()"            ) ;', " Close the control bar     ")
		self.AddButton("  Close all   ", r'TPython::Exec("quit()"                ) ;', " Quit the application      ")


		## **NOTE: object display implemeted into tasks::gui()
		self.Show()
		ROOT.gROOT.SaveContext()



	def __del__(self) :

		self.Delete()	

