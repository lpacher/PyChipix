
import sys

import ROOT


#argv = sys.argv
#argc = len(argv)

#print argc


#a = ROOT.TApplication("a", len(sys.argv), sys.argv)

a = ROOT.TRint("a", len(sys.argv), sys.argv, 0, 0, ROOT.kTRUE)

a.Run(ROOT.kFALSE)

