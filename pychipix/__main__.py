
#----------------------------------------------------------------------------------------------------
#                                        VLSI Design Laboratory
#                               Istituto Nazionale di Fisica Nucleare (INFN)
#                                   via Giuria 1 10125, Torino, Italy
#----------------------------------------------------------------------------------------------------
# {Trace}
# [Filename]      __main__.py
# [Project]       CHIPIX65 demonstrator PyROOT-based DAQ interface
# [Author]        Luca Pacher - pacher@to.infn.it
# [Version]       1.0
# [Language]      Python/ROOT
# [Created]       Aug 5, 2017
# [Modified]      Aug 7, 2017
# [Description]   Main application entry-point
#
# [Notes]         A new TPyROOTApplication (derived from TApplication) is automatically created
#                 for us after ROOT import and sys.argv command-line arguments have been already
#                 passed to its default constructor
# {Trace}
#----------------------------------------------------------------------------------------------------

## Python standard-library components
import sys
import os

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


## application components
from TestCommands import TestCommandsGui
from PixelScan import PixelScanGui
#from kc705 


##________________________________________________________________________________
def ShowHelp() :

	print "\nCommand-line usage:\n"
	print "% pychipix TestCommands"
	print "% pychipix PixelScan"


##________________________________________________________________________________
def main() :

	"""main application entry point"""

	a = ROOT.gApplication
	a.ExecuteFile("./lib/style.cxx")
	#ROOT.gROOT.ProcessLine("./lib/style.cxx")

	#try :

	if( sys.argv[1] == "TestCommands" ) :

		print "Starting TestCommands GUI..."

		w = TestCommandsGui( ROOT.gClient.GetRoot(), 900, 650 )

		## start the main event-looper
		a.Run()

	elif( sys.argv[1] == "PixelScan" ) :

		print "Starting PixelScan GUI..."
		w = PixelScanGui()

		print w.__doc__

		## start the main event-looper
		a.Run()

	else :
		print "Unknown option"


	#except :
	#	ShowHelp()
	#	raise SystemExit



##________________________________________________________________________________
if __name__ == "__main__" :

	## run the application
	main()
