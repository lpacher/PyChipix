
#----------------------------------------------------------------------------------------------------
#                                        VLSI Design Laboratory
#                               Istituto Nazionale di Fisica Nucleare (INFN)
#                                   via Giuria 1 10125, Torino, Italy
#----------------------------------------------------------------------------------------------------
# {Trace}
# [Filename]      FFT.py
# [Project]       CHIPIX65 pixel ASIC demonstrator
# [Author]        Luca Pacher - pacher@to.infn.it
# [Version]       1.0
# [Language]      Python/ROOT
# [Created]       Oct 3, 2017
# [Description]   Computes FFT on sampled data from ADC to extract SINAD and ENOB figures of merit
#
# [Notes]         Usage:
#
#                 python -i FFT.py /path/to/sample.dat
# {Trace}
#----------------------------------------------------------------------------------------------------


## STL components
import array
import numpy
import sys
import math


## ROOT components
import ROOT
ROOT.gROOT.SetStyle("Plain")



#######################
##   user settings   ##
#######################

## enable/disable Blackman filtering on sampled data
applyWindowing = False
#applyWindowing = True

## input signal nominal frequency in Hz
fSignal = 0.3141592

## list of chunks for FFTs
Nentries       = int(1e7)
NsamplesForFFT = int(2**16)
Nchunks        = 150
skippedChunks  = []


## fit range for sampling-frequency extraction
fitMin = 100
fitMax = fitMin + 100

##########################
##   custom functions   ##
##########################

## parameterized sine fit function
def fit(x, par) :

	omega = par[0]
	phi   = par[1]

	sample = x[0]

	#return math.sin(omega*sample + phi)
	return math.cos(omega*sample + phi)


## user-defined dB() function
def dB(x) :

	if(x<=0) :
		return 0
	else :
		#return 10*math.log10(x)
		return 20*math.log10(x)






## .dat input file
fileName = sys.argv[1]
f = open(fileName, "r")

## build C-style array with selected codes
xdata = array.array('d', range(Nchunks*NsamplesForFFT))

i = 0

## catch user-input errors
Nchunks = min(Nchunks, int(Nentries/NsamplesForFFT))

## loop over text file entries
for line in f.readlines() :

	## do not read all lines, only first Nchunks of NpointsForFFT samples for each chunck
	if(i < Nchunks*NsamplesForFFT) :

		code = int(line.split()[0])

		## average invalid codes from SPI and zeroes
		if( code == 0xFFFF or code == 0) :
			xdata[i]= xdata[i-1]
		else :
			xdata[i] = code

		i = i + 1

	## exit from loop otherwise
	else :
		break


## close the file
f.close()





#########################################
##   draw raw data vs. sample number   ##
#########################################

## normalize the sine to unit-amplitude
sineMin = min(xdata)
sineMax = max(xdata)

sineAmpl = 0.5*(sineMax - sineMin)
sineOffset = sineMin + sineAmpl

## histogram of normalized sampled values

Nbins = len(xdata)

hSamples = ROOT.TH1F("hSamples", "", Nbins, 0.5, Nbins + 0.5)
hSamplesNorm = hSamples.Clone("hSamplesNorm")

for i in range(Nbins) :

	hSamples.SetBinContent(i+1, xdata[i])
	hSamplesNorm.SetBinContent(i+1, (xdata[i]-sineOffset)/sineAmpl)


#c1 = ROOT.TCanvas()
#c1.cd()
#hSamples.Draw()


########################################
##   extract the sampling frequency   ##
########################################


## fit function
ff = ROOT.TF1("ff", fit, 0, Nbins, 2) 


ff.SetNpx(int(1e5))

hSamples.Fit("ff", "N", "", fitMin, fitMax)


#ROOT.gPad.Modified()
#ROOT.gPad.Update()

## sampling frequency from fit
#Tint = int(2*3.141592/ff.GetParameter(0))
#fSampling = abs(Tint*fSignal)

fSampling = 69.0 

print "\nSampling frequency from fit: %f Hz" % fSampling



##########################
##   FFT on ADC codes   ##
##########################


## create a Blackman window array
w = numpy.blackman(NsamplesForFFT)

## run FFT on weighted data

xFFT = []


print "\nComputing FFT arrays..."
for k in range(Nchunks) :

	if( k+1 not in skippedChunks) : 

		if(applyWindowing == False) :

			xFFT.append(
				numpy.fft.fft(
					xdata[k*NsamplesForFFT:k*NsamplesForFFT+NsamplesForFFT]
				)
			)
		else :
			xFFT.append(
				numpy.fft.fft(
					xdata[k*NsamplesForFFT:k*NsamplesForFFT+NsamplesForFFT]*w
				)
			)


print "Done!"
print "Averaging FFT values..."

## array of frequencies
aFreq = array.array('d', range(NsamplesForFFT/2))


## array of averaged magnitudes
aMagn = array.array('d', range(NsamplesForFFT/2))


## compute FFT frequencies and average magnitudes
for i in range(NsamplesForFFT/2) :

	aFreq[i] = i*fSampling/NsamplesForFFT

	sum = 0.0

	## **NOTE: skip the first chunk
	for chunk in range(Nchunks-len(skippedChunks)) :

		sum = sum + abs(xFFT[chunk][i])/NsamplesForFFT

	aMagn[i] = sum/(Nchunks-len(skippedChunks))


print "Done!"

## search the signal amplitude
signalAmplitude = max(aMagn[5:])   # **NOTE: skip the DC component!

## draw the spectrum with proper normalization
grFFT = ROOT.TGraph()

for i in range(NsamplesForFFT/2) :

	grFFT.SetPoint(i+1, aFreq[i], dB(aMagn[i]/signalAmplitude))


c2 = ROOT.TCanvas()
c2.cd()
grFFT.Draw("AL")


###################
##   cosmetics   ##
###################

hSamples.SetXTitle("sample number")
hSamples.SetYTitle("ADC code")

hSamplesNorm.SetXTitle("sample number")
hSamplesNorm.SetYTitle("normalized ADC code")

grFFT.GetXaxis().SetTitle("frequency [Hz]")
grFFT.GetYaxis().SetTitle("normalized magnitude [dB]")


## dump FFT to ROOT file

f = ROOT.TFile("FFT.root", "RECREATE")

hSamples.Write()
hSamplesNorm.Write()
grFFT.Write()
f.Close()


###############################################
##   evaluate SNR and noise power from fit   ##
###############################################


## index of fundamental harmonic
indexSignalAmplitude = aMagn.index(signalAmplitude)


## signal frequency from FFT spectrum
signalFrequency = aFreq[indexSignalAmplitude]  


## fit the noise-floor with a constant value (assume to fit over last 20% frequencies)
fNoiseMax = max(aFreq)
fNoiseMin = 0.8*fNoiseMax

grFFT.Fit("pol0", "", "", fNoiseMin, fNoiseMax)


## Signal-to-Noise Ratio from fit
ff2 = grFFT.GetFunction("pol0")
ff2.SetRange(0.0, fNoiseMax) 
ff2.SetLineColor(ROOT.kRed)
SNR = ff2.GetParameter(0)


## noise-floor power
pwrNoise = (10**(SNR/10.0))*(0.5*fSampling) 

ROOT.gPad.Modified()
ROOT.gPad.Update()


##############################################################
##   find high-order harmonics to evaluate SINAD and ENOB   ##
##############################################################



freqHarmonics = []
magnHarmonics = []



## spurious-harmonics power
pwrHarmonics = 0.0


## search first spurious harmonics (k=2,3,4,5,6,7)
for k in range(2,8) :

	## index of maximum
	i = aMagn.index(max(aMagn[k*indexSignalAmplitude-5:k*indexSignalAmplitude+5]))

	## corresponding frequency
	freqHarmonics.append(i*fSampling/NsamplesForFFT)

	## corresponding magnitude
	magnHarmonics.append(dB(aMagn[i]/signalAmplitude))

	pwrHarmonics += 10**(dB(aMagn[i]/signalAmplitude)/10.0) 


## Signal to Noise and Distorsion ratio
SINAD = 10*math.log10(1.0/(pwrHarmonics + pwrNoise))


## Effective Number Of Bits
ENOB = (SINAD - 1.76)/6.02


## print summary results
print "\n--------------------------------------------------"
print "Signal frequency from FFT: %f Hz" % signalFrequency
print "SNR: %f dB" % SNR
print "SINAD: %f dB" % SINAD
print "ENOB: %f" % ENOB
print "--------------------------------------------------"


###################
##   cosmetics   ##
###################

ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()


grFFT.GetXaxis().SetRangeUser(0.0, 5.0)
grFFT.GetYaxis().SetRangeUser(1.2*SNR, 0.0)

grFFT.GetXaxis().SetTitle("frequency [Hz]")
grFFT.GetYaxis().SetTitle("normalized FFT magnitude [dB]")

grFFT.GetYaxis().CenterTitle()
grFFT.GetYaxis().SetTitleOffset(1.2)

ROOT.gPad.Modified()
ROOT.gPad.Update()
