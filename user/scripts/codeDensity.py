
import time

Nentries = int(1e7)

ROOT.gROOT.SetStyle("Plain")

if(Connection.isConnected == False) :

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

for i in range(Nentries) :

	try :

		h.Fill(readADC())

		if(i % 1000 == 0) :
			ROOT.gPad.Modified()
			ROOT.gPad.Update()

	except KeyboardInterrupt :

		time.sleep(0.5)

		disconnect()
		break


ROOT.gPad.Modified()
ROOT.gPad.Update()

f = ROOT.TFile("code_density_ramp.root", "RECREATE")

h.Write()

f.Close()

#raw_input()

