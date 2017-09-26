
## **NOTE: nothing to set for the chip, just use the external ADC...


import time

## output files (.dat and .root are automatically appended)
fileName = "code_density_ramp_board1_never_irradiated"
#fileName = "code_density_sine_board1_never_irradiated"

## results directory
#dataDir = "user/data/"

## output files

dateAndTime = time.strftime("_%Y-%m-%d_%H:%M:%S") 

#textFileName = dataDir + fileName + dateAndTime + ".dat"
#rootFileName = dataDir + fileName + dateAndTime + ".root"

textFileName = fileName + dateAndTime + ".dat"
rootFileName = fileName + dateAndTime + ".root"


## number of entries (10'000'000)
Nentries = int(10e6)

ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat("ourmen")

if(Connection.isConnected) :
	pass
else :
	connect()
	reset()




## **NOTE: declare histogram as global, otherwise it goes out of scope after script execuption!

global h

h = ROOT.TH1F("hCode", "", 2**16, 0-0.5, (2**16-1)+0.5) 
h.Draw()

#textFile = open(textFileName, "w")

for i in range(Nentries) :

	try :

		## read ADC
		adcCode = readExtADC()

		## dump ADC code also to ASCII file
		#textFile.write("%d\n" % adcCode)

		## fill code density histogram
		h.Fill(adcCode)

		## wait some time (Bari)
		#time.sleep(0.2)

		if(i % 1000 == 0) :
			ROOT.gPad.Modified()
			ROOT.gPad.Update()


	except KeyboardInterrupt :

		time.sleep(0.5)

		disconnect()
		break


ROOT.gPad.Modified()
ROOT.gPad.Update()

#rootFile = ROOT.TFile(rootFileName, "RECREATE")

#h.Write()
#rootFile.Close()
#textFile.close()

#raw_input()

