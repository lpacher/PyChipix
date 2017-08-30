
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
# [Description]   Main application entry-point
#
# [Notes]         A new TPyROOTApplication (derived from TApplication) is automatically created
#                 for us after ROOT import and sys.argv command-line arguments have been already
#                 passed to its default constructor
# {Trace}
#----------------------------------------------------------------------------------------------------

## Python standard-library components
import sys

sys.path.append("./pychipix/core")
sys.path.append("./pychipix/gui")

from tasks import *

import os
import socket

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
from PixelScan    import PixelScanGui

##________________________________________________________________________________
def ShowHelp() :

	print "\nCommand-line usage:\n"
	print "% pychipix TestCommands"
	print "% pychipix PixelScan"
	print "% pychipix batch"


##________________________________________________________________________________
def Credits() :

	f = open("./doc/credits.txt")

	lines = f.read().splitlines()
	f.close()

	for line in lines :
		print line


##________________________________________________________________________________
def main() :

	"""main application entry point"""

	Credits()
	a = ROOT.gApplication
	a.ExecuteFile("./lib/style.cxx")
	#ROOT.gROOT.ProcessLine("./lib/style.cxx")

	#try :

	if( sys.argv[1] == "TestCommands" ) :

		print "Starting TestCommands GUI..."

		w = TestCommandsGui()
		print w.__doc__

		## start the main event-looper
		a.Run()

	elif( sys.argv[1] == "PixelScan" ) :

		print "Starting PixelScan GUI..."
		w = PixelScanGui()
		print w.__doc__

		## start the main event-looper
		a.Run()


	elif( sys.argv[1] == "batch") :

		## batch mode selected, change the prompt and pass
		print "Type man() for command-line help"
		sys.ps1 = "pychipix/> "
		#sys.ps1 = "pydaq/> "

		if( len(sys.argv) == 3) :
			execfile(str(sys.argv[2]))

		pass

	else :
		print "Unknown option"

	#except :
	#	ShowHelp()
	#	raise SystemExit

##________________________________________________________________________________
if __name__ == "__main__" :

	## run the application
	main()

