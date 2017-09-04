
import sys

import ROOT


#cvs.Divide(1,3)
#cvs.Divide(3,1)


fileName = sys.argv[1]

print fileName

f = ROOT.TFile(fileName, "READ")

h = f.Get("hCode")

#cvs.cd(1)
h.Draw()

cvsDNL = ROOT.TCanvas("DNL")
cvsINL = ROOT.TCanvas("INL")


h2 = ROOT.TH1F("h2", "h2", 4096, -0.5, 4095.5)


## **NOTE: range(a,b) =>   a <= i < b

## loop from bin 12 to bin 4094, exclude bins 1-7 and 4096

start_code = 20

for code in range(start_code, 4095) :

        bin = code + 1

	h2.Fill(code, h.GetBinContent(bin) )

#cvs.cd(2)
#h2.Draw()


## recompute
EffectiveNbins = 4096 -1 -(start_code + 1)

EffectiveNentries = h2.Integral()

PDF = EffectiveNentries/EffectiveNbins 

hDNL = ROOT.TH1F("hDNL", "CHIPIX DEMO - on-chip ADC DNL", 4096, -0.5, 4095.5)
hINL = ROOT.TH1F("hINL", "CHIPIX DEMO - on-chip ADC INL", 4096, -0.5, 4095.5)

for code in range(start_code, 4095) :

	bin = code + 1

	DNL = ( h2.GetBinContent(bin) - PDF )/PDF
	hDNL.Fill(code, DNL)

cvsDNL.cd()
hDNL.Draw()

hDNL.GetXaxis().SetTitle("ADC code")
hDNL.GetYaxis().SetTitle("DNL [LSB]")
hDNL.GetYaxis().CenterTitle()
hDNL.GetXaxis().SetRangeUser(0, 4095)
hDNL.GetYaxis().SetRangeUser(-0.2, 0.2)

#hDNL.SetLineColor(ROOT.kRed)
hDNL.SetStats(0)

ROOT.gPad.SetGrid()
ROOT.gPad.Modified()
ROOT.gPad.Update()

for code in range(0, 4095) :

	bin = code + 1

	INL = hDNL.Integral(1, bin)
	print code , INL
	hINL.Fill(code, INL)



hINL.GetXaxis().SetTitle("ADC code")
hINL.GetYaxis().SetTitle("INL [LSB]")
hINL.GetYaxis().CenterTitle()
hINL.GetXaxis().SetRangeUser(0, 4095)
hINL.GetYaxis().SetRangeUser(-15, 2.5)

#hINL.SetLineColor(ROOT.kRed)
hINL.SetStats(0)

cvsINL.cd()
hINL.Draw()

ROOT.gPad.SetGrid()
ROOT.gPad.Modified()
ROOT.gPad.Update()

