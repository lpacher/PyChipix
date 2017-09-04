
#----------------------------------------------------------------------------------------------------
#                                        VLSI Design Laboratory
#                               Istituto Nazionale di Fisica Nucleare (INFN)
#                                   via Giuria 1 10125, Torino, Italy
#----------------------------------------------------------------------------------------------------
# {Trace}
# [Filename]      registers.py [CLASS COLLECTION]
# [Project]       CHIPIX65 demonstrator PyROOT-based DAQ
# [Author]        Luca Pacher - pacher@to.infn.it
# [Version]       1.0
# [Language]      Python/ROOT
# [Created]       Aug 27, 2017
# [Description]   Implements classes for ECCR, GCR and PCR registers 
# [Notes]         -
# {Trace}
#----------------------------------------------------------------------------------------------------


## standard-library components
import collections   ## to use ordered dictionaries



## ROOT components
try :
	import ROOT

except ImportError :

	print("\n**ERROR: ROOT components are required to run this application!\n")

	if( os.name == 'nt') :
		print("           call %ROOTSYS%\bin\thisroot.bat might solve this problem.\n")
	else :
		print("           source $ROOTSYS/bin/thisroot.(c)sh might solve this problem.\n")

	raise SystemExit


## custom components
from utils import *





#####################
##   CLASS: ECCR   ##
#####################

"""
Class Reference:

ECCR() - constructor
"""


class ECCR(object) :


	def __init__(self,

		## readout parameters
		TriggerLatency=0b0000000000,    # ECCR_DATA[9:0]
		TriggeredOperations=0,          # ECCR_DATA[0]
		TotMode=0,                      # ECCR_DATA[0]
		HighDeadtimeMode=0,             # ECCR_DATA[0]
		BinaryTimestampEncoding=0,      # ECCR_DATA[0]
		Disable8b10bEncoding=0,			  # ECCR_DATA[31:16]

		## 16-bit MCD mask word
		McdMask=0x0000) :               # ECCR_DATA[:]


		## assign parameters from constructor and check limits
		self.fTriggerLatency          = clamp(TriggerLatency, 0, 2**10-1)
		self.fTriggeredOperations     = clamp(TriggeredOperations, 0, 1)
		self.fTotMode                 = clamp(TotMode, 0, 1)
		self.fHighDeadtimeMode        = clamp(HighDeadtimeMode, 0, 1)
		self.fBinaryTimestampEncoding = clamp(BinaryTimestampEncoding, 0, 1)
		self.fDisable8b10bEncoding    = clamp(Disable8b10bEncoding, 0, 1)
		self.fMcdMask                 = clamp(McdMask, 0, 2**16-1)

		## ordered dictionary of all parameter/value keys, used to return a single list for readback and for printing information
		self.fParameters = collections.OrderedDict()

		self.fParameters["Trigger latency           "] = self.fTriggerLatency          
		self.fParameters["Triggered operations      "] = self.fTriggeredOperations    
		self.fParameters["TOT mode                  "] = self.fTotMode                
		self.fParameters["High-deadtime mode        "] = self.fHighDeadtimeMode       
		self.fParameters["Binary timestamp encoding "] = self.fBinaryTimestampEncoding
		self.fParameters["Disable 88/10b encoding   "] = self.fDisable8b10bEncoding   
		self.fParameters["MCD mask                  "] = self.fMcdMask                


		## registers reset values
		self.fResetValues = []
		
		self.fResetValues.append(0b0000000000)
		self.fResetValues.append(0)
		self.fResetValues.append(0)
		self.fResetValues.append(0)
		self.fResetValues.append(0)
		self.fResetValues.append(0)
		self.fResetValues.append(0x0000)


		## extract register words from parameters and fill registers ECCR_0, ECCR_1
		self.fRegister = self.GetRegistersFromParameters()


	##________________________________________________________________________________
	def GetRegisterContent(self, index) :

		return self.fRegister[index]



	##________________________________________________________________________________
	def GetRegisterValues(self) :

		data = []

		for i in range(2) :
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

		"""extract register words from parameters and fill ECCR_0, ECCR_1"""


		"""
		word = int(self.fTriggerLatency)

		word = word | self.fTriggeredOperations     << 10 
		word = word | self.fTotMode                 << 10+1
		word = word | self.fHighDeadtimeMode        << 10+1+1
		word = word | self.fBinaryTimestampEncoding << 10+1+1+1
		word = word | self.fDisable8b10bEncoding    << 10+1+1+1+1 
		word = word | self.fMcdMask                 << 10+1+1+1+1+2
		"""

		word = int(self.fParameters.values()[0])

		word = word | self.fParameters.values()[ 1] << 10 
		word = word | self.fParameters.values()[ 2] << 10+1
		word = word | self.fParameters.values()[ 3] << 10+1+1
		word = word | self.fParameters.values()[ 4] << 10+1+1+1
		word = word | self.fParameters.values()[ 5] << 10+1+1+1+1 
		word = word | self.fParameters.values()[ 6] << 10+1+1+1+1+2 ;   ## **WARN: ECCR_DATA[15] is UNUSED! Skip one bit in the last left-shift


		## the easy part, each register is 16-bit wide
		registersList = []

		for i in range(2) :

			registersList.append(int(word >> i*16  & 0x0FFFF))

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

		print "\n**INFO: ECCR parameters:"
		print "\n"
		print "--------------------------------------------"
		for i in range(len(self.fParameters)) :
			print "%2d. %s value = %d" % (i+1, self.fParameters.keys()[i], self.fParameters.values()[i])
		print "--------------------------------------------\n"



	##________________________________________________________________________________
	def Reset(self) :

		## just an alias
		self.SetResetValues()



	##________________________________________________________________________________
	def SetParameter(self, index, value) :

		if(index ==0) :
			print "**WARN: Parameters are indexed from 1!"

		elif(index==1) :
			value = clamp(value, 0, 0x3FF)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==2) :
			value = clamp(value, 0, 1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==3) :
			value = clamp(value, 0, 1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==4) :
			value = clamp(value, 0, 1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==5) :
			value = clamp(value, 0, 1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==6) :
			value = clamp(value, 0, 1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==7) :
			value = clamp(value, 0, 0xFFFF)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		else :
			print "**ERROR: index out of range"""




	##________________________________________________________________________________
	def SetRegisterContent(self, index, data) :

		self.fRegister[index] = clamp(data, 0, 0xFFFF)



	##________________________________________________________________________________
	def SetResetValues(self) :
		"""Set ECCR reset values"""

		for i in range(2) :
			self.fRegister[i] = self.fResetValues[i]



	##________________________________________________________________________________
	def UpdateParameters(self) :


		## after any modification to ECCR register contents, repack the word
		word = 0

		for i in range(2) :
			word = word | self.GetRegisterContent(i) << 16*i 


		## **DEBUG
		#print word

		self.fTriggerLatency          = int(word & 0x03FF) ;   word = (word >> 10)
		self.fTriggeredOperations     = int(word & 0x0001) ;   word = (word >>  1)
		self.fTotMode                 = int(word & 0x0001) ;   word = (word >>  1)
		self.fHighDeadtimeMode        = int(word & 0x0001) ;   word = (word >>  1)
		self.fBinaryTimestampEncoding = int(word & 0x0001) ;   word = (word >>  1)
		self.fDisable8b10bEncoding    = int(word & 0x0001) ;   word = (word >>  2) ;   ## **WARN: ECCR_DATA[15] is UNUSED! Skip one bit in the last left-shift
		self.fMcdMask                 = int(word & 0xFFFF)


		## update also dictionary values
		self.fParameters.clear()

		self.fParameters["Trigger latency           "] = self.fTriggerLatency          
		self.fParameters["Triggered operations      "] = self.fTriggeredOperations    
		self.fParameters["TOT mode                  "] = self.fTotMode                
		self.fParameters["High-deadtime mode        "] = self.fHighDeadtimeMode       
		self.fParameters["Binary timestamp encoding "] = self.fBinaryTimestampEncoding
		self.fParameters["Disable 88/10b encoding   "] = self.fDisable8b10bEncoding   
		self.fParameters["MCD mask                  "] = self.fMcdMask                



	##________________________________________________________________________________
	def UpdateRegisters(self) :
		self.fRegister = self.GetRegistersFromParameters()





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
		AdcGain=7,                      # GCR_DATA[206:203]
		AdcIdischarge=28,               # GCR_DATA[212:207]
		AdcIcharge=28,                  # GCR_DATA[218:213]
		AdcThreshold=16) :              # GCR_DATA[223:219]


		## assign parameters from constructor and check limits
		self.fPwmDelay      = clamp(PwmDelay, 0, 2**5-1)
		self.fPwmHigh       = clamp(PwmHigh, 0, 2**8-1)
		self.fPwmLow        = clamp(PwmLow,0, 2**14-1)
		self.fIctrlTot      = clamp(IctrlTot, 0, 2**10-1)
		self.fVthDisc       = clamp(VthDisc, 0, 2**10-1)
		self.fVblDisc       = clamp(VblDisc, 0, 2**10-1)
		self.fIbiasP1       = clamp(IbiasP1, 0, 2**10-1)
		self.fIbiasP2       = clamp(IbiasP2, 0, 2**10-1)
		self.fIbiasDisc     = clamp(IbiasDisc, 0, 2**10-1)
		self.fIbiasSF       = clamp(IbiasSF, 0, 2**10-1)
		self.fVrefKrum1     = clamp(VrefKrum1, 0, 2**10-1)
		self.fIbiasFeed     = clamp(IbiasFeed, 0, 2**10-1)
		self.fIrefTrim      = clamp(IrefTrim, 0, 2**5-1)
		self.fBgrTrim       = clamp(BgrTrim, 0, 2**5-1)
		self.fMonMux        = clamp(MonMux, 0, 2**5-1)
		self.fIldac         = clamp(Ildac, 0, 2**10-1)
		self.fIgdac         = clamp(Igdac, 0, 2**10-1)
		self.fVrefKrum2     = clamp(VrefKrum2, 0, 2**10-1)
		self.fIkrum         = clamp(Ikrum, 0, 2**10-1)
		self.fIfcBias       = clamp(IfcBias, 0, 2**10-1)
		self.fIpaInBias     = clamp(IpaInBias, 0, 2**10-1)
		self.fCalLevel      = clamp(CalLevel, 0, 2**10-1)
		self.fAdcMode       = clamp(AdcMode, 0, 1)
		self.fAdcGain       = clamp(AdcGain, 0, 2**4-1) 
		self.fAdcIdischarge = clamp(AdcIdischarge, 0, 2**6-1)
		self.fAdcIcharge    = clamp(AdcIcharge, 0, 2**6-1)
		self.fAdcThreshold  = clamp(AdcThreshold, 0, 2**5-1)


		## ordered dictionary of all parameter/value keys, used to return a single list for readback and for printing information
		self.fParameters = collections.OrderedDict()
	
		self.fParameters["TO:  PWM delay  "] = self.fPwmDelay
		self.fParameters["TO:  PWM high   "] = self.fPwmHigh
		self.fParameters["TO:  PWM low    "] = self.fPwmLow
		self.fParameters["TO:  ICTRL_TOT  "] = self.fIctrlTot
		self.fParameters["TO:  VTH_DISC   "] = self.fVthDisc
		self.fParameters["TO:  VBL_DISC   "] = self.fVblDisc
		self.fParameters["TO:  IBIASP1    "] = self.fIbiasP1
		self.fParameters["TO:  IBIASP2    "] = self.fIbiasP2
		self.fParameters["TO:  IBIAS_DISC "] = self.fIbiasDisc
		self.fParameters["TO:  IBIAS_SF   "] = self.fIbiasSF
		self.fParameters["TO:  VREF_KRUM  "] = self.fVrefKrum1
		self.fParameters["TO:  IBIAS_FEED "] = self.fIbiasFeed
		self.fParameters["GBL: IREF_TRIM  "] = self.fIrefTrim
		self.fParameters["GBL: BGR_TRIM   "] = self.fBgrTrim
		self.fParameters["ADC: MON_MUX    "] = self.fMonMux
		self.fParameters["PV:  ILDAC      "] = self.fIldac
		self.fParameters["PV:  IGDAC      "] = self.fIgdac
		self.fParameters["PV:  VREF_FRUM  "] = self.fVrefKrum2
		self.fParameters["PV:  IKRUM      "] = self.fIkrum
		self.fParameters["PV:  IFC_BIAS   "] = self.fIfcBias
		self.fParameters["PV:  IPA_IN_BIAS"] = self.fIpaInBias
		self.fParameters["GBL: CAL_LEVEL  "] = self.fCalLevel
		self.fParameters["ADC: MODE       "] = self.fAdcMode
		self.fParameters["ADC: GAIN       "] = self.fAdcGain
		self.fParameters["ADC: IDISCH     "] = self.fAdcIdischarge
		self.fParameters["ADC: ICH        "] = self.fAdcIcharge
		self.fParameters["ADC: VTH        "] = self.fAdcThreshold


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
		return int(self.fParameters.values()[index-1])


	##________________________________________________________________________________
	def GetParameters(self) :

		parametersList = []

		for i in range(len(self.fParameters)) :
			parametersList.append(self.GetParameter(i+1))

		return parametersList 


	##________________________________________________________________________________
	def PrintParameters(self) :

		print "\n**INFO: GCR parameters:"
		print "\n"
		print "----------------------------------"
		for i in range(len(self.fParameters)) :
			print "%2d. %s value = %d" % (i+1, self.fParameters.keys()[i], self.fParameters.values()[i])
		print "----------------------------------\n"


	##________________________________________________________________________________
	def Reset(self) :
		## just an alias
		self.SetResetValues()


	##________________________________________________________________________________
	def SetParameter(self, index, value) :


		if(index ==0) :
			print "**WARN: Parameters are indexed from 1!"

		elif(index==1) :
			value = clamp(value, 0, 2**5-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==2) :
			value = clamp(value, 0, 2**8-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==3) :
			value = clamp(value, 0, 2**14-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==4) :
			value = clamp(value, 0, 2**10-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==5) :
			value = clamp(value, 0, 2**10-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==6) :
			value = clamp(value, 0, 2**10-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==7) :
			value = clamp(value, 0, 2**10-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==8) :
			value = clamp(value, 0, 2**10-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==9) :
			value = clamp(value, 0, 2**10-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==10) :
			value = clamp(value, 0, 2**10-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==11) :
			value = clamp(value, 0, 2**10-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==12) :
			value = clamp(value, 0, 2**10-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==13) :
			value = clamp(value, 0, 2**5-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==14) :
			value = clamp(value, 0, 2**5-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==15) :
			value = clamp(value, 0, 2**5-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==16) :
			value = clamp(value, 0, 2**10-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==17) :
			value = clamp(value, 0, 2**10-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==18) :
			value = clamp(value, 0, 2**10-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==19) :
			value = clamp(value, 0, 2**10-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==20) :
			value = clamp(value, 0, 2**10-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==21) :
			value = clamp(value, 0, 2**10-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==22) :
			value = clamp(value, 0, 2**10-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==23) :
			value = clamp(value, 0, 1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==24) :
			value = clamp(value, 0, 2**5-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==25) :
			value = clamp(value, 0, 2**6-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==26) :
			value = clamp(value, 0, 2**6-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		elif(index==27) :
			value = clamp(value, 0, 2**5-1)
			self.fParameters.__setitem__(self.fParameters.keys()[index-1], value) 

		else :
			print "**ERROR: index out of range"




	##________________________________________________________________________________
	def SetRegisterContent(self, index, data) :

		self.fRegister[index] = data



	##________________________________________________________________________________
	def SetResetValues(self) :
		"""Set GCR reset values"""

		for i in range(14) :
			self.fRegister[i] = self.fResetValues[i]



	##________________________________________________________________________________
	def UpdateParameters(self) :


		## after any modification to GCR register contents, repack the word
		word = 0L

		for i in range(14) :
			word = word | self.GetRegisterContent(i) << 16*i 


		## **DEBUG
		#print word

		self.fPwmDelay      = int(word & 0x0001F) ;  word = (word >>  5)
		self.fPwmHigh       = int(word & 0x000FF) ;  word = (word >>  8)
		self.fPwmLow        = int(word & 0x03FFF) ;  word = (word >> 14)
		self.fIctrlTot      = int(word & 0x003FF) ;  word = (word >> 10)
		self.fVthDisc       = int(word & 0x003FF) ;  word = (word >> 10)
		self.fVblDisc       = int(word & 0x003FF) ;  word = (word >> 10)
		self.fIbiasP1       = int(word & 0x003FF) ;  word = (word >> 10)
		self.fIbiasP2       = int(word & 0x003FF) ;  word = (word >> 10)
		self.fIbiasDisc     = int(word & 0x003FF) ;  word = (word >> 10)
		self.fIbiasSF       = int(word & 0x003FF) ;  word = (word >> 10)
		self.fVrefKrum1     = int(word & 0x003FF) ;  word = (word >> 10)
		self.fIbiasFeed     = int(word & 0x003FF) ;  word = (word >> 10)
		self.fIrefTrim      = int(word & 0x0001F) ;  word = (word >>  5)
		self.fBgrTrim       = int(word & 0x0001F) ;  word = (word >>  5)
		self.fMonMux        = int(word & 0x0001F) ;  word = (word >>  5)
		self.fIldac         = int(word & 0x003FF) ;  word = (word >> 10)
		self.fIgdac         = int(word & 0x003FF) ;  word = (word >> 10)
		self.fVrefKrum2     = int(word & 0x003FF) ;  word = (word >> 10)
		self.fIkrum         = int(word & 0x003FF) ;  word = (word >> 10)
		self.fIfcBias       = int(word & 0x003FF) ;  word = (word >> 10)
		self.fIpaInBias     = int(word & 0x003FF) ;  word = (word >> 10)
		self.fCalLevel      = int(word & 0x003FF) ;  word = (word >> 10)
		self.fAdcMode       = int(word & 0x00001) ;  word = (word >>  1)
		self.fAdcGain       = int(word & 0x0000F) ;  word = (word >>  4)
		self.fAdcIdischarge = int(word & 0x0003F) ;  word = (word >>  6)
		self.fAdcIcharge    = int(word & 0x0003F) ;  word = (word >>  6)
		self.fAdcThreshold  = int(word & 0x0001F)


		## update also dictionary values
		self.fParameters.clear()

		self.fParameters["TO:  PWM delay  "] = self.fPwmDelay
		self.fParameters["TO:  PWM high   "] = self.fPwmHigh
		self.fParameters["TO:  PWM low    "] = self.fPwmLow
		self.fParameters["TO:  ICTRL_TOT  "] = self.fIctrlTot
		self.fParameters["TO:  VTH_DISC   "] = self.fVthDisc
		self.fParameters["TO:  VBL_DISC   "] = self.fVblDisc
		self.fParameters["TO:  IBIASP1    "] = self.fIbiasP1
		self.fParameters["TO:  IBIASP2    "] = self.fIbiasP2
		self.fParameters["TO:  IBIAS_DISC "] = self.fIbiasDisc
		self.fParameters["TO:  IBIAS_SF   "] = self.fIbiasSF
		self.fParameters["TO:  VREF_KRUM  "] = self.fVrefKrum1
		self.fParameters["TO:  IBIAS_FEED "] = self.fIbiasFeed
		self.fParameters["GBL: IREF_TRIM  "] = self.fIrefTrim
		self.fParameters["GBL: BGR_TRIM   "] = self.fBgrTrim
		self.fParameters["ADC: MON_MUX    "] = self.fMonMux
		self.fParameters["PV:  ILDAC      "] = self.fIldac
		self.fParameters["PV:  IGDAC      "] = self.fIgdac
		self.fParameters["PV:  VREF_FRUM  "] = self.fVrefKrum2
		self.fParameters["PV:  IKRUM      "] = self.fIkrum
		self.fParameters["PV:  IFC_BIAS   "] = self.fIfcBias
		self.fParameters["PV:  IPA_IN_BIAS"] = self.fIpaInBias
		self.fParameters["GBL: CAL_LEVEL  "] = self.fCalLevel
		self.fParameters["ADC: MODE       "] = self.fAdcMode
		self.fParameters["ADC: GAIN       "] = self.fAdcGain
		self.fParameters["ADC: IDISCH     "] = self.fAdcIdischarge
		self.fParameters["ADC: ICH        "] = self.fAdcIcharge
		self.fParameters["ADC: VTH        "] = self.fAdcThreshold



	##________________________________________________________________________________
	def UpdateRegisters(self) :
		self.fRegister = self.GetRegistersFromParameters()
		



class PCR_TO(object) :

	def __init__(self, DoubleColumn=0x00, PixelRegion=0x0, PCR=0b00,

		## left 
		MaskL=0,
		CalEnableL=0,
		FastModeL=0,
		SelC2fL=0,
		SelC4fL=0,

		## right
		MaskR=0,
		CalEnableR=0,
		FastModeR=0,
		SelC2fR=0,
		SelC4fR=1) :


		## assign parameters from constructor and check limits

		self.fAddress = [DoubleColumn, PixelRegion, PCR]

		self.MaskL      = clamp(MaskL, 0, 1)
		self.CalEnableL = clamp(CalEnableL, 0, 1)
		self.FastModeL  = clamp(FastModeL, 0, 1)
		self.SelC2fL    = clamp(SelC2fL, 0, 1)
		self.SelC4fL    = clamp(SelC4fL, 0, 1)
		self.MaskR      = clamp(MaskR, 0, 1)
		self.CalEnableR = clamp(CalEnableR, 0, 1)
		self.FastModeR  = clamp(FastModeR, 0, 1)
		self.SelC2fR    = clamp(SelC2fR, 0, 1)
		self.SelC4fR    = clamp(SelC4fR, 0, 1)


		## ordered dictionary of all parameter/value keys, used to return a single list for readback and for printing information
		self.fParameters = collections.OrderedDict()
	
		self.fParameters["L: MASK     "] = self.MaskL     
		self.fParameters["L: CAL_EN   "] = self.CalEnableL
		self.fParameters["L: FAST MODE"] = self.FastModeL 
		self.fParameters["L: SEL_C2F  "] = self.SelC2fL   
		self.fParameters["L: SEL_C4F  "] = self.SelC4fL   
		self.fParameters["R: MASK     "] = self.MaskR     
		self.fParameters["R: CAL_EN   "] = self.CalEnableR
		self.fParameters["R: FAST MODE"] = self.FastModeR 
		self.fParameters["R: SEL_C2F  "] = self.SelC2fR   
		self.fParameters["R: SEL_C4F  "] = self.SelC4fR   


		## registers reset values
		self.fResetValue = 0x0000


class PCR_BGPV(object) :
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


