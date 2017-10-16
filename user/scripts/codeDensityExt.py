
#----------------------------------------------------------------------------------------------------
#                                        VLSI Design Laboratory
#                               Istituto Nazionale di Fisica Nucleare (INFN)
#                                   via Giuria 1 10125, Torino, Italy
#----------------------------------------------------------------------------------------------------
# {Trace}
# [Filename]      codeDensity.py
# [Project]       CHIPIX65 pixel ASIC demonstrator
# [Author]        Luca Pacher - pacher@to.infn.it
# [Version]       1.0
# [Language]      Python/ROOT
# [Created]       Sep 21, 2017
# [Description]   Code-density acquisition script for external-ADC testing. Edit the script
#                 and change user settings to fit board number, input waveform, frequency etc.
#
# [Notes]         Usage:
#
#                 ./bin/lin/pychipix ./user/scripts/codeDensityExt.py
# {Trace}
#----------------------------------------------------------------------------------------------------


## STL components
import time


#######################
##   user settings   ##
#######################


## number of entries (100'000'000 for 16-bit ADC)
Nentries = int(100e6)

## additional software delay
#cpuDelaySeconds = 0.0                  # approx. 1000 samples/  1s = 1000 Hz sampling rate
#cpuDelaySeconds = 1.0/1000.0           # approx. 1000 samples/  3s =  300 Hz sampling rate
#cpuDelaySeconds = 1.0/100.0            # approx. 1000 samples/ 10s =  100 Hz sampling rate
#cpuDelaySeconds = 1.0/10.0             # approx  1000 samples/100s =   10 Hz sampling rate

cpuDelaySeconds = 1e-2
#cpuDelaySeconds = 0.0


## board number/board status

boardNumber = 1 ;   boardStatus = "never_irradiated"

#boardNumber = 2
#boardNumber = 3
#boardNumber = 4
#boardNumber = 5
#boardNumber = 6
#boardNumber = 7
#boardNumber = 8
#boardNumber = 9 ;   boardStatus = "irradiated"


## input waveform
inputWaveform = "ramp"
#inputWaveform = "sine"

## input frequency [Hz]
inputFrequency = 0.314159


#########################

## output files (.dat and .root are automatically appended)
fileName = "code_density_" + "board" + str(boardNumber) + "_waveform_" + inputWaveform + "_frequency_" + str(inputFrequency) + "Hz_cpuDelay_" + str(cpuDelaySeconds) + "sec"


## results directory

## **TODO: catch errors on paths and create directories otherwise
if(inputWaveform == "ramp") :
	dataDir = "user/data/ADC/external/linearity/static/"
else :
	dataDir = "user/data/ADC/external/linearity/dynamic/"


## output files

dateAndTime = time.strftime("_%Y-%m-%d_%H-%M-%S") 

textFileName = dataDir + fileName + dateAndTime + ".dat"
rootFileName = dataDir + fileName + dateAndTime + ".root"


ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat("ourmen")

if(Connection.isConnected) :
	pass
else :
	connect()
	reset()


## **NOTE: declare histograms as global, otherwise they go out of scope after script execuption!

global hCode, hSample

Nbits = 16
Nbins = 2**Nbits

hCode = ROOT.TH1F("hCode", "", Nbins, -0.5, Nbins + 0.5) 
hSample = ROOT.TH1F("hSample", "", Nentries, 0.5, Nentries + 0.5)

if(ROOT.gROOT.IsBatch() == False) :
	hCode.Draw()

textFile = open(textFileName, "w")
rootFile = ROOT.TFile(rootFileName, "RECREATE")

hCode.Write()
hSample.Write()

for i in range(Nentries) :

	try :

		## save on ROOT file each 1000 samples
		if(i % 1000 == 0 and i != 0) :
			print "Entries:" , int(hCode.GetEntries())
			hCode.Write("", ROOT.TObject.kOverwrite)
			hSample.Write("", ROOT.TObject.kOverwrite)

			if(ROOT.gROOT.IsBatch() == False) :
				ROOT.gPad.Modified()
				ROOT.gPad.Update()


		## nothing to set for the chip, just read the external ADC
		adcCode = readExtADC()

		## dump ADC code also to ASCII file
		textFile.write("%d\n" % adcCode)

		## fill code density hostogram
		hCode.Fill(adcCode)

		## fill samples histogram
		hSample.SetBinContent(i+1, adcCode)

		## optionally, wait some time
		time.sleep(cpuDelaySeconds)

		"""
		## **OBSOLETE: this introduced discontinuities in the sampled waveform!

		## check that everything is OK inside the chip
		if(i % 10000 == 0) :

			if(readGCR().fMonMux == 31) :
				pass
			else :
				time.sleep(0.5)
				print "Spurious reset detected!"

				## re-write GCR
				writeGCR(r)
				#disconnect()
				#break
		"""

	## catch Ctrl+C user input
	except KeyboardInterrupt :

		time.sleep(0.5)

		disconnect()
		break

if(ROOT.gROOT.IsBatch() == False) :
	ROOT.gPad.Modified()
	ROOT.gPad.Update()

hCode.Write("", ROOT.TObject.kOverwrite)
hSample.Write("", ROOT.TObject.kOverwrite)

rootFile.Close()
textFile.close()

#raw_input()

