
import sys

import ROOT


#cvs.Divide(1,3)
#cvs.Divide(3,1)


fileName = sys.argv[1]

print fileName

f = ROOT.TFile(fileName, "READ")

hCode = f.Get("hCode")

#cvs.cd(1)
hCode.Draw()

cvsNorm = ROOT.TCanvas("Norm")
cvsDNL = ROOT.TCanvas("DNL")
cvsINL = ROOT.TCanvas("INL")



## second histogram with skipped bins
hNorm = ROOT.TH1F("hNorm", "hNorm", 4096, -0.5, 4095.5)


## **NOTE: range(a,b) =>   a <= i < b

## loop from bin 12 to bin 4094, exclude bins 1-7 and 4096

codeMin = 9 
codeMax = 4095


for code in range(0, 4095+1) :

	bin = code+1

	if( codeMin+1 < bin < codeMax+1) :
		hNorm.SetBinContent(bin, hCode.GetBinContent(bin) )

	else :
		hNorm.SetBinContent(bin, 0)


cvsNorm.cd()
hNorm.Draw()

#ROOT.gPad.SetGrid()
ROOT.gPad.Modified()
ROOT.gPad.Update()

## recompute entries
EffectiveNbins = codeMax -(codeMin+1)
EffectiveNentries = hNorm.Integral()

PDF = EffectiveNentries/EffectiveNbins 

print PDF

hDNL = ROOT.TH1F("hDNL", "CHIPIX DEMO - on-chip ADC DNL", 4096, -0.5, 4095.5)
hINL = ROOT.TH1F("hINL", "CHIPIX DEMO - on-chip ADC INL", 4096, -0.5, 4095.5)

for code in range(0, 4095+1) :

	bin = code + 1

	if( codeMin+1 < bin < codeMax+1) :

		DNL = ( hNorm.GetBinContent(bin) - PDF )/PDF
		hDNL.SetBinContent(bin, DNL)
		#print DNL

	else :

		hDNL.SetBinContent(bin, 0)


cvsDNL.cd()
hDNL.Draw()


#hDNL.SetLineColor(ROOT.kRed)
hDNL.SetStats(0)

#ROOT.gPad.SetGrid()
ROOT.gPad.Modified()
ROOT.gPad.Update()

for code in range(0, 4095+1) :

	bin = code + 1

	INL = hDNL.Integral(1, bin)
	#print code , INL
	hINL.SetBinContent(bin, INL)




cvsINL.cd()
hINL.Draw()

#ROOT.gPad.SetGrid()
ROOT.gPad.Modified()
ROOT.gPad.Update()



##############################
##   cosmetics for slides   ##
##############################

## hNorm


hNorm.SetTitle("")
hNorm.SetStats(0)

#hNorm.SetFillColor(ROOT.kBlue+2)
hNorm.SetFillColor(1)
hNorm.SetLineColor(1)

hNorm.GetXaxis().SetTitle("ADC code")
hNorm.GetYaxis().SetTitle("entries")
hNorm.GetYaxis().CenterTitle()
hNorm.GetYaxis().SetRangeUser(0.1, 3e3)

hNorm.GetXaxis().SetRangeUser(0, 4095)


hNorm.GetXaxis().SetTitleFont(132)
hNorm.GetXaxis().SetTitleSize(0.055)
hNorm.GetXaxis().SetTitleOffset(1.0)
hNorm.GetXaxis().SetLabelFont(132)
hNorm.GetXaxis().SetLabelSize(0.04)


hNorm.GetYaxis().SetTitleFont(132)
hNorm.GetYaxis().SetTitleSize(0.055)
hNorm.GetYaxis().SetTitleOffset(1.0)
hNorm.GetYaxis().SetLabelFont(132)
hNorm.GetYaxis().SetLabelSize(0.04)

## hDNL

hDNL.SetTitle("")

hDNL.GetXaxis().SetTitle("ADC code")
hDNL.GetYaxis().SetTitle("DNL [LSB]")
hDNL.GetYaxis().CenterTitle()
hDNL.GetXaxis().SetRangeUser(0, 4095)
hDNL.GetYaxis().SetRangeUser(-0.22, 0.22)

hDNL.SetLineColor(1)

hDNL.GetXaxis().SetTitleFont(132)
hDNL.GetXaxis().SetTitleSize(0.055)
hDNL.GetXaxis().SetTitleOffset(1.0)
hDNL.GetXaxis().SetLabelFont(132)
hDNL.GetXaxis().SetLabelSize(0.04)

hDNL.GetYaxis().SetTitleFont(132)
hDNL.GetYaxis().SetTitleSize(0.055)
hDNL.GetYaxis().SetTitleOffset(1.0)
hDNL.GetYaxis().SetLabelFont(132)
hDNL.GetYaxis().SetLabelSize(0.04)


## hINL

hINL.SetTitle("")

hINL.GetXaxis().SetTitle("ADC code")
hINL.GetYaxis().SetTitle("INL [LSB]")
hINL.GetYaxis().CenterTitle()
hINL.GetXaxis().SetRangeUser(0, 4095)
hINL.GetYaxis().SetRangeUser(-5.5, 5.5)

hINL.SetLineColor(1)
hINL.SetStats(0)


hINL.GetXaxis().SetTitleFont(132)
hINL.GetXaxis().SetTitleSize(0.055)
hINL.GetXaxis().SetTitleOffset(1.0)
hINL.GetXaxis().SetLabelFont(132)
hINL.GetXaxis().SetLabelSize(0.04)

hINL.GetYaxis().SetTitleFont(132)
hINL.GetYaxis().SetTitleSize(0.055)
hINL.GetYaxis().SetTitleOffset(0.7)
hINL.GetYaxis().SetLabelFont(132)
hINL.GetYaxis().SetLabelSize(0.04)


for c in [cvsNorm, cvsDNL, cvsINL] :

	c.cd()
	ROOT.gPad.Modified()
	ROOT.gPad.Update()
