
import time

## additional software delay
cpuDelaySeconds = 1.0/100.0

## board number
boardNumber = 4

## board status
#boardStatus = "never_irradiated"
boardStatus = "irradiated"


## input waveform
#inputWaveform = "ramp"
inputWaveform = "sine"


## input frequency [Hz]
inputFrequency = 0.314159

## output files (.dat and .root are automatically appended)
fileName = "code_density_" + "board" + str(boardNumber) + "_waveform_" + inputWaveform + "_frequency_" + str(inputFrequency) + "Hz_cpuDelay_" + str(cpuDelaySeconds) + "_sec"


## results directory
dataDir = "user/data/"

## output files

dateAndTime = time.strftime("_%Y-%m-%d_%H:%M:%S") 

textFileName = dataDir + fileName + dateAndTime + ".dat"
rootFileName = dataDir + fileName + dateAndTime + ".root"


## number of entries (10'000'000)
Nentries = int(10e6)

ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat("ourmen")

if(Connection.isConnected) :
	pass
else :
	connect()
	reset()


## create a GCR object
r = GCR()

## set MON_MUX to 31 (ADC input disconnected from global DACs, high-impedance input) 
r.SetParameter(15, 31)
r.UpdateRegisters()

writeGCR(r)

## readback to check
readGCR().PrintParameters()


## pause to check, press RETURN to continue 
#raw_input()


## **NOTE: declare histogram as global, otherwise it goes out of scope after script execuption!

global h

h = ROOT.TH1F("hCode", "", 4096, -0.5, 4095.5) 
h.Draw()

textFile = open(textFileName, "w")

for i in range(Nentries) :

	try :

		## read ADC
		adcCode = readADC()

		## dump ADC code also to ASCII file
		textFile.write("%d\n" % adcCode)

		## fill code density hostogram
		h.Fill(adcCode)

		## optionally, wait some time
		time.sleep(cpuDelaySeconds)

		if(i % 1000 == 0) :
			ROOT.gPad.Modified()
			ROOT.gPad.Update()

		## check that everything is OK inside the chip
		if(i % 10000 == 0) :

			if(readGCR().fMonMux == 31) :
				pass
			else :
				time.sleep(0.5)
				disconnect()
				break

	except KeyboardInterrupt :

		time.sleep(0.5)

		disconnect()
		break


ROOT.gPad.Modified()
ROOT.gPad.Update()

rootFile = ROOT.TFile(rootFileName, "RECREATE")

h.Write()
rootFile.Close()
textFile.close()

#raw_input()
