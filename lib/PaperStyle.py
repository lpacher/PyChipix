
## usage: from PaperStyle import *

from ROOT import gStyle

def SetPaperStyle() :


	## histograms lines
	gStyle.SetHistFillColor(0)
	gStyle.SetHistFillStyle(0)

	gStyle.SetHistLineColor(1)
	gStyle.SetHistLineStyle(0)
	gStyle.SetHistLineWidth(1)

	## suppress plot titles and fit box
	gStyle.SetOptTitle(0)
	gStyle.SetOptFit(0)

	## axis settings
	gStyle.SetLabelFont(142, "xyz")
	gStyle.SetLabelSize(0.04, "xyz")

	gStyle.SetTitleFont(142, "xyz")
	gStyle.SetTitleOffset(1.2, "xyz")
	gStyle.SetTitleSize(0.05, "xyz")


	## stat box
	gStyle.SetOptStat(0)         # suppress the stats box
	#gStyle.SetOptStat("emr")    # display Entries, Mean and RMS
	#gStyle.SetStatFont(142)
	#gStyle.SetStatFontSize(0.05)
	#gStyle.SetStatBorderSize(0)

