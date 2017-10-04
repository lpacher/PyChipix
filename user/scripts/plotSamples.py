#!/usr/bin/env python

import ROOT
import sys

## choose here the number of samples to be plotted
Nsamples = int(1e4)


## input .dat
f = open(sys.argv[1], "r")

xdata = []

for line in f.readlines() :

	code = int(line.split()[0])
	xdata.append(code)


## check
if( Nsamples > len(xdata)) :
	Nsamples = len(xdata)
else :
	pass


f.close()

hSamples = ROOT.TH1F("hSamples", "", Nsamples, 0.5, Nsamples+0.5)

for i in range(Nsamples) :

	hSamples.SetBinContent(i+1, xdata[i])

hSamples.Draw()

hSamples.GetXaxis().SetTitle("samples")
hSamples.GetYaxis().SetTitle("ADC code")
hSamples.GetYaxis().CenterTitle()
hSamples.GetYaxis().SetTitleOffset(1.1)

raw_input()

