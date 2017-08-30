
#----------------------------------------------------------------------------------------------------
#                                        VLSI Design Laboratory
#                               Istituto Nazionale di Fisica Nucleare (INFN)
#                                   via Giuria 1 10125, Torino, Italy
#----------------------------------------------------------------------------------------------------
# {Trace}
# [Filename]      types.py [CLASS COLLECTION]
# [Project]       CHIPIX65 demonstrator PyROOT-based DAQ
# [Author]        Luca Pacher - pacher@to.infn.it
# [Version]       1.0
# [Language]      Python/ROOT
# [Created]       Aug 27, 2017
# [Description]   Reusable DAQ objects, mainly used as namespaces and C-style structs
# [Notes]         -
# {Trace}
#----------------------------------------------------------------------------------------------------


import collections   ## to use ordered dictionaries

import ROOT


####################
##   CLASS: GCR   ##
####################

"""
Class Reference:

GCR() - constructor
"""

class GCR(object) :

	def __init__(self, 

		## Torino pixels
		PwmDelay=0,                     # GCR_DATA[  4:  0]
		PwmHigh=20,                     # GCR_DATA[ 12:  5]
		PwmLow=3980,                    # GCR_DATA[ 26: 13]

		IctrlTot=100,                   # GCR_DATA[ 36: 27]
		VthDisc=1023,                   # GCR_DATA[ 46: 37]
		VblDisc=450,                    # GCR_DATA[ 56: 47]
		IbiasP1=100,                    # GCR_DATA[ 66: 57]
		IbiasP2=150,                    # GCR_DATA[ 76: 67]
		IbiasDisc=200,                  # GCR_DATA[ 86: 77]
		IbiasSF=100,                    # GCR_DATA[ 96: 87]
		VrefKrum1=490,                  # GCR_DATA[106: 97]
		IbiasFeed=80,                   # GCR_DATA[116:107]

		## reference current
		IrefTrim=20,                    # GCR_DATA[121:117]

		## bandgap reference
		BgrTrim=5,                      # GCR_DATA[126:122]

		## monitoring MUX
		MonMux=16,                      # GCR_DATA[131:127]

		## Bergamo/Pavia pixels
		Ildac=160,                      # GCR_DATA[141:132]
		Igdac=1023,                     # GCR_DATA[151:142]
		VrefKrum2=300,                  # GCR_DATA[161:152]
		Ikrum=50,                       # GCR_DATA[171:162]
		IfcBias=200,                    # GCR_DATA[181:172]
		IpaInBias=300,                  # GCR_DATA[191:182]

		## global cal level
		CalLevel=0,                     # GCR_DATA[201:192]

		## ADC configuration
		AdcMode=0,                      # GCR_DATA[    202]
		AdcGain=8,                      # GCR_DATA[206:203]
		AdcIdischarge=28,               # GCR_DATA[212:207]
		AdcIcharge=28,                  # GCR_DATA[218:213]
		AdcThreshold=16) :              # GCR_DATA[223:219]


		## assign binary parameters (strings) from constructor
		self.fPwmDelay      = PwmDelay
		self.fPwmHigh       = PwmHigh
		self.fPwmLow        = PwmLow
		self.fIctrlTot      = IctrlTot
		self.fVthDisc       = VthDisc
		self.fVblDisc       = VblDisc
		self.fIbiasP1       = IbiasP1
		self.fIbiasP2       = IbiasP2
		self.fIbiasDisc     = IbiasDisc
		self.fIbiasSF       = IbiasSF
		self.fVrefKrum1     = VrefKrum1
		self.fIbiasFeed     = IbiasFeed
		self.fIrefTrim      = IrefTrim
		self.fBgrTrim       = BgrTrim
		self.fMonMux        = MonMux
		self.fIldac         = Ildac
		self.fIgdac         = Igdac
		self.fVrefKrum2     = VrefKrum2
		self.fIkrum         = Ikrum
		self.fIfcBias       = IfcBias
		self.fIpaInBias     = IpaInBias
		self.fCalLevel      = CalLevel
		self.fAdcMode       = AdcMode
		self.fAdcGain       = AdcGain
		self.fAdcIdischarge = AdcIdischarge
		self.fAdcIcharge    = AdcIcharge
		self.fAdcThreshold  = AdcThreshold


		## ordered dictionary of all parameter/value keys, used to return a single list for readback and for printing information
		self.fParameters = collections.OrderedDict()
	
		self.fParameters[" 1) TO:  PWM delay  "] = self.fPwmDelay
		self.fParameters[" 2) TO:  PWM high   "] = self.fPwmHigh
		self.fParameters[" 3) TO:  PWM low    "] = self.fPwmLow
		self.fParameters[" 4) TO:  ICTRL_TOT  "] = self.fIctrlTot
		self.fParameters[" 5) TO:  VTH_DISC   "] = self.fVthDisc
		self.fParameters[" 6) TO:  VBL_DISC   "] = self.fVblDisc
		self.fParameters[" 7) TO:  IBIASP1    "] = self.fIbiasP1
		self.fParameters[" 8) TO:  IBIASP2    "] = self.fIbiasP2
		self.fParameters[" 9) TO:  IBIAS_DISC "] = self.fIbiasDisc
		self.fParameters["10) TO:  IBIAS_SF   "] = self.fIbiasSF
		self.fParameters["11) TO:  VREF_KRUM  "] = self.fVrefKrum1
		self.fParameters["12) TO:  IBIAS_FEED "] = self.fIbiasFeed
		self.fParameters["13) GBL: IREF_TRIM  "] = self.fIrefTrim
		self.fParameters["14) GBL: BGR_TRIM   "] = self.fBgrTrim
		self.fParameters["15) ADC: MON_MUX    "] = self.fMonMux
		self.fParameters["16) PV:  ILDAC      "] = self.fIldac
		self.fParameters["17) PV:  IGDAC      "] = self.fIgdac
		self.fParameters["18) PV:  VREF_FRUM  "] = self.fVrefKrum2
		self.fParameters["19) PV:  IKRUM      "] = self.fIkrum
		self.fParameters["20) PV:  IFC_BIAS   "] = self.fIfcBias
		self.fParameters["21) PV:  IPA_IN_BIAS"] = self.fIpaInBias
		self.fParameters["22) GBL: CAL_LEVEL  "] = self.fCalLevel
		self.fParameters["23) ADC: MODE       "] = self.fAdcMode
		self.fParameters["24) ADC: GAIN       "] = self.fAdcGain
		self.fParameters["25) ADC: IDISCH     "] = self.fAdcIdischarge
		self.fParameters["26) ADC: ICH        "] = self.fAdcIcharge
		self.fParameters["27) ADC: VTH        "] = self.fAdcThreshold


		## registers reset values
		self.fResetValues = []
		
		## **NOTE: copy and paste "as it is" from RTL source code!
		self.fResetValues.append(0b1000001010000000)
		self.fResetValues.append(0b0010000111110001)
		self.fResetValues.append(0b0111111111100011)
		self.fResetValues.append(0b1100100011100001)
		self.fResetValues.append(0b0000010010110000)
		self.fResetValues.append(0b0011001000011001)
		self.fResetValues.append(0b1000001111010100)
		self.fResetValues.append(0b0001011010000010)
		self.fResetValues.append(0b1100101000001000)
		self.fResetValues.append(0b0010110011111111)
		self.fResetValues.append(0b1000000011001001)
		self.fResetValues.append(0b0100101100001100)
		self.fResetValues.append(0b0100000000000000)
		self.fResetValues.append(0b1000001110001110)


		## extract register words from parameters and fill the 14 registers GCR_0, ... GCR_13
		self.fRegister = self.GetRegistersFromParameters()



	##________________________________________________________________________________
	def GetRegisterContent(self, index) :

		return self.fRegister[index]



	##________________________________________________________________________________
	def GetRegisterValues(self) :

		data = []

		for i in range(14) :
			data.append(self.fRegister[i])

		return data


	##________________________________________________________________________________
	def GetRegisterResetValue(self, index) :
		return self.fResetValues[index]



	##________________________________________________________________________________
	def GetRegisterResetValues(self) :
		return self.fResetValues



	##________________________________________________________________________________
	def GetRegisterBinWord(self, index) :
		return "0b" + format(self.fRegister[index], "016b")



	##________________________________________________________________________________
	def GetRegisterHexWord(self, index) :
		return "0x" + format(self.fRegister[index], "04x").upper()



	##________________________________________________________________________________
	def GetRegistersFromParameters(self) :

		"""extract register words from parameters and fill the 14 registers GCR_0, ... GCR_13"""


		## **NOTE: long int to store all 224-bits at once as a single number

		"""
		word = long(self.fPwmDelay) 

		word = word | self.fPwmHigh       << 5
		word = word | self.fPwmLow        << 5+8
		word = word | self.fIctrlTot      << 5+8+14
		word = word | self.fVthDisc       << 5+8+14+10
		word = word | self.fVblDisc       << 5+8+14+10+10
		word = word | self.fIbiasP1       << 5+8+14+10+10+10
		word = word | self.fIbiasP2       << 5+8+14+10+10+10+10
		word = word | self.fIbiasDisc     << 5+8+14+10+10+10+10+10
		word = word | self.fIbiasSF       << 5+8+14+10+10+10+10+10+10
		word = word | self.fVrefKrum1     << 5+8+14+10+10+10+10+10+10+10
		word = word | self.fIbiasFeed     << 5+8+14+10+10+10+10+10+10+10+10
		word = word | self.fIrefTrim      << 5+8+14+10+10+10+10+10+10+10+10+10
		word = word | self.fBgrTrim       << 5+8+14+10+10+10+10+10+10+10+10+10+5
		word = word | self.fMonMux        << 5+8+14+10+10+10+10+10+10+10+10+10+5+5
		word = word | self.fIldac         << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5
		word = word | self.fIgdac         << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10
		word = word | self.fVrefKrum2     << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10
		word = word | self.fIkrum         << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10+10
		word = word | self.fIfcBias       << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10+10+10
		word = word | self.fIpaInBias     << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10+10+10+10
		word = word | self.fCalLevel      << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10+10+10+10+10
		word = word | self.fAdcMode       << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10+10+10+10+10+10
		word = word | self.fAdcGain       << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10+10+10+10+10+10+1
		word = word | self.fAdcIcharge    << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10+10+10+10+10+10+1+4
		word = word | self.fAdcIdischarge << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10+10+10+10+10+10+1+4+6 
		word = word | self.fAdcThreshold  << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10+10+10+10+10+10+1+4+6+6
		"""

		word = long(self.fParameters.values()[0])

		word = word | self.fParameters.values()[ 1] << 5
		word = word | self.fParameters.values()[ 2] << 5+8
		word = word | self.fParameters.values()[ 3] << 5+8+14
		word = word | self.fParameters.values()[ 4] << 5+8+14+10
		word = word | self.fParameters.values()[ 5] << 5+8+14+10+10
		word = word | self.fParameters.values()[ 6] << 5+8+14+10+10+10
		word = word | self.fParameters.values()[ 7] << 5+8+14+10+10+10+10
		word = word | self.fParameters.values()[ 8] << 5+8+14+10+10+10+10+10
		word = word | self.fParameters.values()[ 9] << 5+8+14+10+10+10+10+10+10
		word = word | self.fParameters.values()[10] << 5+8+14+10+10+10+10+10+10+10
		word = word | self.fParameters.values()[11] << 5+8+14+10+10+10+10+10+10+10+10
		word = word | self.fParameters.values()[12] << 5+8+14+10+10+10+10+10+10+10+10+10
		word = word | self.fParameters.values()[13] << 5+8+14+10+10+10+10+10+10+10+10+10+5
		word = word | self.fParameters.values()[14] << 5+8+14+10+10+10+10+10+10+10+10+10+5+5
		word = word | self.fParameters.values()[15] << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5
		word = word | self.fParameters.values()[16] << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10
		word = word | self.fParameters.values()[17] << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10
		word = word | self.fParameters.values()[18] << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10+10
		word = word | self.fParameters.values()[19] << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10+10+10
		word = word | self.fParameters.values()[20] << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10+10+10+10
		word = word | self.fParameters.values()[21] << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10+10+10+10+10
		word = word | self.fParameters.values()[22] << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10+10+10+10+10+10
		word = word | self.fParameters.values()[23] << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10+10+10+10+10+10+1
		word = word | self.fParameters.values()[24] << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10+10+10+10+10+10+1+4
		word = word | self.fParameters.values()[25] << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10+10+10+10+10+10+1+4+6 
		word = word | self.fParameters.values()[26] << 5+8+14+10+10+10+10+10+10+10+10+10+5+5+5+10+10+10+10+10+10+10+1+4+6+6

		## the easy part, each register is 16-bit wide
		registersList = []

		for i in range(14) :

			registersList.append( int(word >> i*16  & 0x0FFFF))


		return registersList



	##________________________________________________________________________________
	def GetParameter(self, index) :
		return int(self.fParameters.values()[index])


	##________________________________________________________________________________
	def GetParameters(self) :

		parametersList = []

		for i in range(len(self.fParameters)) :
			parametersList.append(self.GetParameter(i))

		return parametersList 


	##________________________________________________________________________________
	def PrintParameters(self) :

		print "\n**INFO: GCR parameters:"
		print "\n--------------------------------"
		for i in range(len(self.fParameters)) :
			print " %s value = %d" % (self.fParameters.keys()[i], self.fParameters.values()[i])
		print "--------------------------------\n"


	##________________________________________________________________________________
	def Reset(self) :
		## just an alias
		self.SetResetValues()


	##________________________________________________________________________________
	def SetParameter(self, index, value) :

		self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 


	##________________________________________________________________________________
	def SetRegisterContent(self, index, data) :

		self.fRegister[index] = data



	##________________________________________________________________________________
	def SetResetValues(self) :

		for i in range(14) :
			self.fRegister[i] = format(self.fResetValues[i], "016b")



	##________________________________________________________________________________
	def UpdateParameters(self) :


		## after any modification to register contents, repack the word
		word = 0L

		for i in range(14) :
			word = word | self.fRegister[i] << 16*i 


		## **DEBUG
		#print word

		self.fPwmDelay      = int(word & 0x01F  ) ;  word = (word >>  5)
		self.fPwmHigh       = int(word & 0x0FF  ) ;  word = (word >>  8)
		self.fPwmLow        = int(word & 0x03FFF) ;  word = (word >> 14)
		self.fIctrlTot      = int(word & 0x03FF ) ;  word = (word >> 10)
		self.fVthDisc       = int(word & 0x03FF ) ;  word = (word >> 10)
		self.fVblDisc       = int(word & 0x03FF ) ;  word = (word >> 10)
		self.fIbiasP1       = int(word & 0x03FF ) ;  word = (word >> 10)
		self.fIbiasP2       = int(word & 0x03FF ) ;  word = (word >> 10)
		self.fIbiasDisc     = int(word & 0x03FF ) ;  word = (word >> 10)
		self.fIbiasSF       = int(word & 0x03FF ) ;  word = (word >> 10)
		self.fVrefKrum1     = int(word & 0x03FF ) ;  word = (word >> 10)
		self.fIbiasFeed     = int(word & 0x03FF ) ;  word = (word >> 10)
		self.fIrefTrim      = int(word & 0x01F  ) ;  word = (word >>  5)
		self.fBgrTrim       = int(word & 0x01F  ) ;  word = (word >>  5)
		self.fMonMux        = int(word & 0x01F  ) ;  word = (word >>  5)
		self.fIldac         = int(word & 0x03FF ) ;  word = (word >> 10)
		self.fIgdac         = int(word & 0x03FF ) ;  word = (word >> 10)
		self.fVrefKrum2     = int(word & 0x03FF ) ;  word = (word >> 10)
		self.fIkrum         = int(word & 0x03FF ) ;  word = (word >> 10)
		self.fIfcBias       = int(word & 0x03FF ) ;  word = (word >> 10)
		self.fIpaInBias     = int(word & 0x03FF ) ;  word = (word >> 10)
		self.fCalLevel      = int(word & 0x03FF ) ;  word = (word >> 10)
		self.fAdcMode       = int(word & 0x01   ) ;  word = (word >>  1)
		self.fAdcGain       = int(word & 0x0F   ) ;  word = (word >>  4)
		self.fAdcIdischarge = int(word & 0x03F  ) ;  word = (word >>  6)
		self.fAdcIcharge    = int(word & 0x03F  ) ;  word = (word >>  6)
		self.fAdcThreshold  = int(word & 0x01F  )


		## update also dictionary values
		self.fParameters.clear()

		self.fParameters[" 1) TO:  PWM delay  "] = self.fPwmDelay
		self.fParameters[" 2) TO:  PWM high   "] = self.fPwmHigh
		self.fParameters[" 3) TO:  PWM low    "] = self.fPwmLow
		self.fParameters[" 4) TO:  ICTRL_TOT  "] = self.fIctrlTot
		self.fParameters[" 5) TO:  VTH_DISC   "] = self.fVthDisc
		self.fParameters[" 6) TO:  VBL_DISC   "] = self.fVblDisc
		self.fParameters[" 7) TO:  IBIASP1    "] = self.fIbiasP1
		self.fParameters[" 8) TO:  IBIASP2    "] = self.fIbiasP2
		self.fParameters[" 9) TO:  IBIAS_DISC "] = self.fIbiasDisc
		self.fParameters["10) TO:  IBIAS_SF   "] = self.fIbiasSF
		self.fParameters["11) TO:  VREF_KRUM  "] = self.fVrefKrum1
		self.fParameters["12) TO:  IBIAS_FEED "] = self.fIbiasFeed
		self.fParameters["13) GBL: IREF_TRIM  "] = self.fIrefTrim
		self.fParameters["14) GBL: BGR_TRIM   "] = self.fBgrTrim
		self.fParameters["15) ADC: MON_MUX    "] = self.fMonMux
		self.fParameters["16) PV:  ILDAC      "] = self.fIldac
		self.fParameters["17) PV:  IGDAC      "] = self.fIgdac
		self.fParameters["18) PV:  VREF_FRUM  "] = self.fVrefKrum2
		self.fParameters["19) PV:  IKRUM      "] = self.fIkrum
		self.fParameters["20) PV:  IFC_BIAS   "] = self.fIfcBias
		self.fParameters["21) PV:  IPA_IN_BIAS"] = self.fIpaInBias
		self.fParameters["22) GBL: CAL_LEVEL  "] = self.fCalLevel
		self.fParameters["23) ADC: MODE       "] = self.fAdcMode
		self.fParameters["24) ADC: GAIN       "] = self.fAdcGain
		self.fParameters["25) ADC: IDISCH     "] = self.fAdcIdischarge
		self.fParameters["26) ADC: ICH        "] = self.fAdcIcharge
		self.fParameters["27) ADC: VTH        "] = self.fAdcThreshold



	##________________________________________________________________________________
	def UpdateRegisters(self) :
		self.fRegister = self.GetRegistersFromParameters()
		


#####################
##   CLASS: ECCR   ##
#####################

class ECCR(object) :


	def __init__(self) :
		pass


	def GetDefaults(self) :
		pass

		#return []


	"""
	triggerLatency = int(self.fEccrWriteTriggerLatencyEntry.GetNumber())
	mcdMask = int(self.fEccrWriteMcdMaskEntry.GetNumber())

	triggeredOperations     = int(self.fEccrWriteTriggerModeEnable.IsOn())
	totMode                 = int(self.fEccrWriteTotModeEnable.IsOn())
	highDeadtimeMode        = int(self.fEccrWriteHighDeadtimeEnable.IsOn())
	binaryTimestampEncoding = int(self.fEccrWriteBinaryTimestampEnable.IsOn())
	disable8b10bEncoding    = int(self.fEccrWrite8b10bDisable.IsOn())

	ECCR_DATA = []

	ECCR_DATA.append(triggerLatency)
	ECCR_DATA.append(triggeredOperations)
	ECCR_DATA.append(totMode)
	ECCR_DATA.append(highDeadtimeMode)
	ECCR_DATA.append(binaryTimestampEncoding)
	ECCR_DATA.append(disable8b10bEncoding)
	ECCR_DATA.append(mcdMask)
	"""

class PCRTO(object) :
	pass


class PCRPV(object) :
	pass



#########################
##   CLASS: PixelMap   ##
#########################


class PixelMap(ROOT.TH2F) : 

	def __init__(self) :

		ROOT.TH2F.__init__(self, "pixelMap", "Pixel Map", 64, -0.05, 63.5, 64, -0.5, 63.5)

		ROOT.gStyle.SetOptStat(0)


		## test
		self.Fill(30, 30, 1)
		self.Fill(20, 40, 10)


		## **NOTE: per ottenere poi graficamente una vera matrice devo:

		# 1. GetXaxis().SetNdivisions(64, ROOT.kFALSE)   => divido gli assi esattamente in 64
		# 2. GetYaxis().SetNdivisions(64, ROOT.kFALSE)
		# ROOT.gStyle.SetGridStyle(0)  => linea continua


