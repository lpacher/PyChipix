
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


## GUI application components
from GUI import GUI
from tasks import showBar


##________________________________________________________________________________
def printCommandLineHelp() :

	print "\nCommand-line usage:\n"
	print "pychipix [--batchi | --gui | --info] [/path/to/script]\n"


##________________________________________________________________________________
def printCredits() :

	f = open("./doc/credits.txt")

	lines = f.read().splitlines()
	f.close()

	for line in lines :
		print line


##________________________________________________________________________________
def main() :

	"""main application entry point"""

	## show credits
	printCredits()


	## print hints
	print "Type man() for command-line help"
	print "Type root() to open a ROOT/CINT session"


	## set command prompt
	sys.ps1 = "pychipix/> "


	## parse command-line arguments
	if(len(sys.argv) > 1) :

		if(sys.argv[1] == "--gui") :
	
			## launch the control bar
			showBar()


			## a script is passed for execution
			if( len(sys.argv) == 3) :
				execfile(str(sys.argv[2]))


		## batch-mode selected, GUI will be not available
		elif( sys.argv[1] == "--batch") :

			ROOT.gROOT.SetBatch(ROOT.kTRUE)


			## a script is passed for execution
			if( len(sys.argv) == 3) :
				execfile(str(sys.argv[2]))


		## a script is passed as a unique argument
		else :
			execfile(str(sys.argv[1]))



	## default mode with both GUI and command-line available
	else :
		pass



##________________________________________________________________________________
if __name__ == "__main__" :

	## run the application
	main()

