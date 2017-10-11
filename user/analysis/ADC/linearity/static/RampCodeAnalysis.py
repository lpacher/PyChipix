
#----------------------------------------------------------------------------------------------------
#                                        VLSI Design Laboratory
#                               Istituto Nazionale di Fisica Nucleare (INFN)
#                                   via Giuria 1 10125, Torino, Italy
#----------------------------------------------------------------------------------------------------
# {Trace}
# [Filename]      RampCodeAnalysis.py
# [Project]       CHIPIX65 pixel ASIC demonstrator
# [Author]        Luca Pacher - pacher@to.infn.it
# [Version]       1.0
# [Language]      Python/ROOT
# [Created]       Sep 3, 2017
# [Description]   Computes DNL/INL histograms from .root file containing ADC sampled data
#                 and assuming a triangular input waveform
#
# [Notes]         Usage:
#
#                 python -i RampCodeAnalysis.py /path/to/sample.root
# {Trace}
#----------------------------------------------------------------------------------------------------


## STL components
import sys
import math


## ROOT components
import ROOT
ROOT.gROOT.SetStyle("Plain")


#######################
##   user settings   ##
#######################

## number of bits
Nbits = 12
#Nbits = 16


## choose here which codes will be skipped from analysis
## **NOTE: codeMin and codeMax will be INCLUDED in the analysis
codeMin = 10
codeMax = (2**Nbits-1) -10



#########################
##   theoretical PDF   ##
#########################


## in case of a ramp/triangular input waveform the PDF of ADC codes is constant
def pdf(x, par) :

	const = par[0]
	return const


#################################
##   histograms and canvases   ##
#################################

## create here all histograms

global hCode, hNorm, hDNL, hINL

Nbins = 2**Nbits

hMin = -0.5
hMax =  0.5 + 2**Nbits -1

## raw-data code-density
hCode = ROOT.TH1F("hCode", "", Nbins, hMin, hMax)

## auxiliary histogram for unit-area normalization (a clone of hCode)
hNorm = hCode.Clone("hNorm")
hNorm.Reset()
hNorm.SetMaximum(-1111)
hNorm.SetMinimum(-1111)

## DNL histogram (a clone of hCode)
hDNL = hCode.Clone("hDNL")
hDNL.Reset()
hDNL.SetMaximum(0.5)
hDNL.SetMinimum(-0.5)


## INL histogram (a clone of hCode)
hINL = hCode.Clone("hINL")
hINL.Reset()
hINL.SetMaximum(-1111)
hINL.SetMinimum(-1111)


## ROOT input file-name
## **TODO: catch wrong user input

fileName = sys.argv[1]
#f = ROOT.TFile(fileName, "READ")
f = ROOT.TFile(fileName, "UPDATE")

## get code-density histogram from ROOT file
hCode = f.Get("hCode")

## canvases
cvs = []

cvs.append(ROOT.TCanvas("cvsCode", "Raw-data code density"))
cvs.append(ROOT.TCanvas("cvsNorm", "Selected-codes normalized code-density"))
cvs.append(ROOT.TCanvas("cvsDNL", "DNL"))
cvs.append(ROOT.TCanvas("cvsINL", "INL"))

cvs[0].cd()
hCode.Draw()



#####################################################
##   unit-area normalization with selected codes   ##
#####################################################


## **NOTE: loop over ALL ADC CODES !
for code in range(0, int(hMax)+1) :

	bin = code + 1

	if(codeMin + 1 <= bin <= codeMax + 1) :
		hNorm.SetBinContent(bin, hCode.GetBinContent(bin) )

	else :
		hNorm.SetBinContent(bin, 0)


## unit-area histogram
norm = hNorm.Integral()
hNorm.Scale(1.0/norm)

cvs[1].cd()
hNorm.Draw()


#############################################
##   comparison with the theoretical PDF   ##
#############################################

fPDF = ROOT.TF1("fPDF", pdf, hMin, hMax, 1)

## normalize to unit-area the PDF within [codeMin,codeMax]
fPDF.FixParameter(0, 1.0/(codeMax-codeMin))

fPDF.SetRange(codeMin-1, codeMax+1)
fPDF.SetLineColor(ROOT.kRed)


## superimpose the PDF to the normalized histogram
fPDF.Draw("same")



##########################################
##   compute and histogram DNL values   ##
##########################################

## loop over ALL ADC CODES and compare relative frequencies with the theoretical PDF
for code in range(0, (2**Nbits-1)+1) :

	bin = code + 1

	if(codeMin + 1 <= bin <= codeMax + 1) :

		## DNL
		DNL = hNorm.GetBinContent(bin)/fPDF.Eval(code) - 1.0
		hDNL.SetBinContent(bin, DNL)

		## DNL error from binomial distribution
		#hDNL.SetBinError(bin, eDNL)

		#word = format(code, '012b')
		#for b in range(11+1) :

		#	if(int(word[b]) == 1) :
		#		hBit.Fill(11-b, int(hNorm.GetBinContent(bin)))
		#print DNL

	else :

		## assume DNL = 0.0 for excluded codes
		hDNL.SetBinContent(bin, 0)
		#hDNL.SetBinError(bin, 0.0)


cvs[2].cd()
hDNL.Draw()


"""
## **TODO: histogram of single-bits
hBit = ROOT.TH1F("hBit", ... ) 

cvsBit = ROOT.TCanvas()
cvsBit.cd()
hBit.Draw()
"""


##########################################
##   compute and histogram INL values   ##
##########################################

## loop over ALL ADC CODES and compute cumulative values
for code in range(0, (2**Nbits-1)+1) :

	bin = code + 1

	INL = hDNL.Integral(1, bin)
	hINL.SetBinContent(bin, INL)
	#hINL.SetBinError(bin, INLe)


cvs[3].cd()
hINL.Draw()



###################
##   cosmetics   ##
###################

hCode.GetXaxis().SetTitle("ADC code")
hCode.GetYaxis().SetTitle("entries")
hCode.GetYaxis().CenterTitle()
hCode.SetFillColor(1)

hNorm.GetXaxis().SetTitle("ADC code")
hNorm.GetYaxis().SetTitle("normalized entries")
hNorm.GetYaxis().CenterTitle()

hDNL.GetXaxis().SetTitle("ADC code")
hDNL.GetYaxis().SetTitle("DNL [LSB]")
hDNL.GetYaxis().CenterTitle()

hINL.GetYaxis().SetTitle("INL [LSB]")
hINL.GetXaxis().SetTitle("ADC code")
hINL.GetYaxis().CenterTitle()


## update all canvases
for c in cvs :

	c.cd()
	ROOT.gPad.Modified()
	ROOT.gPad.Update()



###################################
##   save results on ROOT file   ##
###################################

## **NOTE: add hNorm, hDNL and hINL to the EXISTING ROOT file !
for h in [hCode, hNorm, hDNL, hINL] :
	h.Write("", ROOT.TObject.kOverwrite)


#raw_input()
#f.Close()


## **DEBUG
#print hNorm.Integral()
#print fPDF.Integral(codeMin, codeMax)


