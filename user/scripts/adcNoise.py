
#----------------------------------------------------------------------------------------------------
#                                        VLSI Design Laboratory
#                               Istituto Nazionale di Fisica Nucleare (INFN)
#                                   via Giuria 1 10125, Torino, Italy
#----------------------------------------------------------------------------------------------------
# {Trace}
# [Filename]      adcNoise.py
# [Project]       CHIPIX65 pixel ASIC demonstrator
# [Author]        Luca Pacher - pacher@to.infn.it
# [Version]       1.0
# [Language]      Python/ROOT
# [Created]       Oct 5, 2017
# [Description]   Noise acquisition script for internal-ADC testing. Edit the script
#                 and change user settings to fit board number, on-PCB resistance and
#                 MUX input from global DACs
#
# [Notes]         Usage:
#
#                 ./bin/lin/pychipix ./user/scripts/adcNoise.py
# {Trace}
#----------------------------------------------------------------------------------------------------


## STL components
import time


#######################
##   user settings   ##
#######################


## number of samples for each DAC code
Nsamples = int(1e3)
#Nsamples = int(1e4)

## additional software delay
cpuDelaySeconds = 0.0
#cpuDelaySeconds = 1.0/100.0
#cpuDelaySeconds = 1.0/1000.0

## board number
boardNumber = 4

## board status
#boardStatus = "never_irradiated"
boardStatus = "irradiated"


## DACs

## voltages
#monMuxInput =  0 ; par = 14 ; dac = "BgrTrim" 
#monMuxInput =  1 ; par = 18 ; dac = "VrefKrumPv"
#monMuxInput =  2 ; par = 22 ; dac = "CalHi"
#monMuxInput =  3 ;            dac = "CalLo"               **FIXED!
monMuxInput =  4 ; par =  5 ; dac = "VthDisc"
#monMuxInput =  5 ; par =  6 ; dac = "VblDisc"
#monMuxInput =  6 ; par = 11 ; dac = "VrefKrumTo"

#monMuxInput =  7  **FLOATING
#monMuxInput =  8
#monMuxInput =  9
#monMuxInput = 10
#monMuxInput = 11
#monMuxInput = 12
#monMuxInput = 13
#monMuxInput = 14
#monMuxInput = 15

## currents
#monMuxInput = 16 ; par = 13 ; dac = "IrefTrim"
#monMuxInput = 17 ; par =  7 ; dac = "IbiasP1"
#monMuxInput = 18 ; par =  8 ; dac = "IbiasP2"
#monMuxInput = 19 ; par =  9 ; dac = "IbiasDisc"
#monMuxInput = 20 ; par = 10 ; dac = "IbiasSf"
#monMuxInput = 21 ; par =  4 ; dac = "IctrlTot" ;  setMux(1,1)   ## **NOTE: set PCB mux resistance to 1 kohm !
#monMuxInput = 22 ; par = 12 ; dac = "IbiasFeed"
#monMuxInput = 23 ; par = 17 ; dac = "Igdac"
#monMuxInput = 24 ; par = 16 ; dac = "Ildac"
#monMuxInput = 25 ; par = 20 ; dac = "IfcBias"
#monMuxInput = 26 ; par = 19 ; dac = "Ikrum"
#monMuxInput = 27 ; par = 21 ; dac = "IpaInBias"

#monMuxInput = 28  **FLOATING
#monMuxInput = 29
#monMuxInput = 30
#monMuxInput = 31


#########################

## output files (.dat and .root are automatically appended)
fileName = "noise_" + "board" + str(boardNumber) + "_DAC_" + dac + "_cpuDelay_" + str(cpuDelaySeconds) + "sec"


## results directory
dataDir = "user/data/ADC/internal/"

## output files

dateAndTime = time.strftime("_%Y-%m-%d_%H-%M-%S") 

rootFileName = dataDir + fileName + dateAndTime + ".root"


ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat("ourmen")

if(Connection.isConnected) :
	pass
else :
	connect()
	reset()


## create a GCR object
r = GCR()

## connect ADC input according to monMuxInput
r.SetParameter(15, monMuxInput)
r.UpdateRegisters()
writeGCR(r)

## readback to check
readGCR().PrintParameters()


## pause to check, press RETURN to continue 
#raw_input()


## **NOTE: declare the histogram as global, otherwise it goes out of scope after script execution!
global c
global grNoise
global hCode

grNoise = ROOT.TGraph() 

hCode = ROOT.TH1F("hCode", "", 4096, -0.5, 4095.5) 


grNoise.SetMarkerStyle(21)
grNoise.SetMarkerSize(0.8)

c = ROOT.TCanvas("c", "", 2*ROOT.gStyle.GetCanvasDefW(), ROOT.gStyle.GetCanvasDefH())
c.Divide(2,1)

c.cd(1)
hCode.Draw()

hCode.GetXaxis().SetTitle("ADC code")

c.cd(2)
grNoise.Draw("ALP")
grNoise.GetXaxis().SetTitle("DAC code")
grNoise.GetYaxis().SetTitle("RMS noise [ADC code]")


point = 0


## main loop over DAC codes
for dacCode in range(0, 1023+1, 1) :

	try :

		## set ICTRL_TOT DAC code
		r.SetParameter(par, dacCode)
		r.UpdateRegisters()
		writeGCR(r)

		## reset the ADC histogram
		hCode.Reset()

		## repeat ADC reading several times
		for i in range(Nsamples) :

			## read ADC
			adcCode = readADC()

			## fill ADC histogram
			hCode.Fill(adcCode)

			## optionally, wait some time
			time.sleep(cpuDelaySeconds)

		c.cd(1)
		ROOT.gPad.Modified()
		ROOT.gPad.Update()

		## get mean and RMS values from distribution
		mean = hCode.GetMean()
		rms = hCode.GetRMS()

		#hNoise.SetBinContent(bin, mean)
		#hNoise.SetBinError(bin, rms)

		grNoise.SetPoint(point, dacCode, mean)
		#grNoise.SetPoint(point, dacCode, rms)

		c.cd(2)
		ROOT.gPad.Modified()
		ROOT.gPad.Update()

		point = point + 1

		## check that everything is OK inside the chip
		if(readGCR().fMonMux == monMuxInput) :
			pass
		else :
			time.sleep(0.5)
			print "Spurious reset detected!"

			## re-write GCR
			#writeGCR(r)
			disconnect()
			break

	except KeyboardInterrupt :

		time.sleep(0.5)

		disconnect()
		break


ROOT.gPad.Modified()
ROOT.gPad.Update()

## dump to ROOT file
rootFile = ROOT.TFile(rootFileName, "RECREATE")

#grNoise.Write()
#rootFile.Close()

raw_input()

