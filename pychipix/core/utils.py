
#----------------------------------------------------------------------------------------------------
#                                        VLSI Design Laboratory
#                               Istituto Nazionale di Fisica Nucleare (INFN)
#                                   via Giuria 1 10125, Torino, Italy
#----------------------------------------------------------------------------------------------------
# {Trace}
# [Filename]      GbPhy.py [FUNCTIONS]
# [Project]       CHIPIX65 demonstrator PyROOT-based DAQ
# [Author]        Luca Pacher - pacher@to.infn.it
# [Version]       1.0
# [Language]      Python/ROOT
# [Created]       Aug 31, 2017
# [Description]   Useful collection of usei0defined functions
# [Notes]         -
# {Trace}
#----------------------------------------------------------------------------------------------------



##________________________________________________________________________________
def clamp(N, Nmin, Nmax) :
	"""for a given integer, returns either the number or its min/max permitted values"""
	return max(min(Nmax, N), Nmin)


##________________________________________________________________________________
def ror(x, y) :
	"""bitwise right-rotation, 16-bit max. data width"""
	mask = (2**y) -1
	mask_bits = x & mask
	return (x >> y) | (mask_bits << (16-y))


##________________________________________________________________________________
def rol(x, y) :
	"""bitwise left-rotation, 16-bit max. data width"""
	return ror(x, 16-y)


