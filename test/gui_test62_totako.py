#!/usr/bin/env python

###################################################################################################
###################################################################################################
####                            Import python library                                        ######
###################################################################################################
###################################################################################################

###################################################################################################
###  to translate a keyword: hex to ascii
###################################################################################################

import hmac
import hashlib

####################################################################################################
# socket libraries is used to connection
####################################################################################################

import sys,socket

####################################################################################################
# for file existance
####################################################################################################

import os
from os.path import exists

###################################################################################################
# data, timing
###################################################################################################

import datetime

###################################################################################################
# to working on list
###################################################################################################

import string

###################################################################################################
# to use all time library
###################################################################################################

import time

###################################################################################################
###################################################################################################
####   Prepare the folder and file to save board output
###################################################################################################
###################################################################################################

###################################################################################################
# if don't found directory create it
###################################################################################################

try:
    os.stat("CHIPIX_response_board")
except:
    os.mkdir("CHIPIX_response_board")  

data = datetime.datetime.now()

my_day = str(data.day)
my_month = str(data.month)
my_year = str(data.year)
filename  = ["chipix"]
filename1 = ["cal_level"]

###################################################################################################
# create a file
###################################################################################################

filename.append(my_day)
filename.append(my_month)
filename.append(my_year)
filename_space = string.join(filename)
filecreator = filename_space.replace(" ","_")

filename1.append(my_day)
filename1.append(my_month)
filename1.append(my_year)
filename_space1 = string.join(filename1)
filecreator1 = filename_space1.replace(" ","_")

###################################################################################################
# create a directory
#####################################################################################################

cost_path = ["CHIPIX_response_board"]
cost_path.append(filecreator)
cost_path = string.join(cost_path)
path = cost_path.replace(" ","/")

cost_path1 = ["CHIPIX_response_board"]
cost_path1.append(filecreator1)
cost_path1 = string.join(cost_path1)
path1 = cost_path1.replace(" ","/")


####################################################################################################
# file exist?
####################################################################################################

if(exists(path)):
	#create file txt 
	f = open(path,"a")
	f.write("\n ")
else:
	f = open(path,"w")
	f.write("\n ")

if(exists(path1)):
	#create file txt 
	f1 = open(path1,"a")
	f1.write("\n ")
else:
	f1 = open(path1,"w")
	f1.write("\n ")

###################################################################################################
###################################################################################################
###   Verify if ROOT is correctly installed on pc
###################################################################################################
###################################################################################################

###################################################################################################
## import ROOT components (catch errors otherwise)
###################################################################################################

try :
   import ROOT

except ImportError :
   raise ImportError, "ROOT bindings are required to run this application!"


###################################################################################################
### gui structure
###################################################################################################

class my_Canvas( ROOT.TGMainFrame ):

	#################################################################################
	###### constructor
	################################################################################

	def __init__( self, parent, width, height ):
		fMain = ROOT.TGMainFrame.__init__( self, parent, width, height )

		####################################################################################
		## global variable
		##################################################################################
	
		global UDP_IP
		UDP_IP = "192.168.1.10"
		global UDP_PORT
		UDP_PORT = 10000

		#######################################################################################
		## when click the cross "close window" icon, terminate the application and exit Python 
		########################################################################################

		self.CloseWindowDispatcher = ROOT.TPyDispatcher( self.CloseWindow )
		self.Connect( "CloseWindow()", "TPyDispatcher", self.CloseWindowDispatcher, "Dispatch()" )

		###########################################################################################
		## build a top frame to contains TABs and a "Quit" button
		###########################################################################################

		self.topFrame = ROOT.TGHorizontalFrame(self, 650, 100, ROOT.kHorizontalFrame )
		self.Connect( "CloseWindow()", "TPyDispatcher", self.CloseWindowDispatcher, "Dispatch()" )
		
		self.quitButton  = ROOT.TGTextButton( self.topFrame, "   &Quit   ")
		self.quitButton.Connect    ('Clicked()' , 'TPyDispatcher' , self.CloseWindowDispatcher, 'Dispatch()')
		self.helpButton  = ROOT.TGTextButton( self.topFrame, "   &Help   ")
		self.Do_help = ROOT.TPyDispatcher( self.my_help )
		self.helpButton.Connect    ('Clicked()' , 'TPyDispatcher' , self.Do_help, 'Dispatch()')
		self.connectButton  = ROOT.TGTextButton( self.topFrame, "   &Connect   ")
		self.Do_Connect = ROOT.TPyDispatcher( self.my_Connect )
		self.connectButton.Connect    ('Clicked()' , 'TPyDispatcher' , self.Do_Connect, 'Dispatch()')

		self.topFrame.AddFrame( self.quitButton, ROOT.TGLayoutHints( ROOT.kLHintsRight, 0, 15, 10, 0) )
		self.topFrame.AddFrame( self.helpButton, ROOT.TGLayoutHints( ROOT.kLHintsRight, 0, 15, 10, 0) )
		self.topFrame.AddFrame( self.connectButton, ROOT.TGLayoutHints( ROOT.kLHintsRight, 0, 15, 10, 0) )
		self.AddFrame( self.topFrame, ROOT.TGLayoutHints( ROOT.kLHintsTop | ROOT.kLHintsExpandX, 0, 0, 0, 0) )
		
		##############################################################################################
		## TABs frame
		###############################################################################################

		self.tabsFrame = ROOT.TGTab(self, 650, 200)
		self.tabsFrame.DrawBorder()

		#################################
		##   tab LED color test        ##
		#################################

		self.tabA = self.tabsFrame.AddTab(" Color test ") # **NOTE! Each tab is now a ROOT.TGCompositeFrame object

		## create a vertical frame
		self.verticalbuttons  = ROOT.TGVerticalFrame(self.tabA, 200, 200 , ROOT.kRaisedFrame)

		## create buttons

		self.Turn_on_red    = ROOT.TGTextButton( self.verticalbuttons, "Turn on red led"   , 10 )
		self.Turn_off_red   = ROOT.TGTextButton( self.verticalbuttons, "Turn off red led"  , 20 )
		self.Turn_on_green  = ROOT.TGTextButton( self.verticalbuttons, "Turn on green led" , 30 )
		self.Turn_off_green = ROOT.TGTextButton( self.verticalbuttons, "Turn off green led", 40 )
		self.Turn_on_blue   = ROOT.TGTextButton( self.verticalbuttons, "Turn on blue led"  , 50 )
		self.Turn_off_blue  = ROOT.TGTextButton( self.verticalbuttons, "Turn off blue led" , 60 )

		self.verticalbuttons.AddFrame(self.Turn_on_red,ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft,10,10,10,0))
               # left right top bottom
		self.verticalbuttons.AddFrame(self.Turn_off_red,ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft,10,10,10,0))
		self.verticalbuttons.AddFrame(self.Turn_on_green,ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft,10,10,10,0))
		self.verticalbuttons.AddFrame(self.Turn_off_green,ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft,10,10,10,0))
		self.verticalbuttons.AddFrame(self.Turn_on_blue,ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft,10,10,10,0))
		self.verticalbuttons.AddFrame(self.Turn_off_blue,ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft,10,10,10,0))
		
		self.tabA.AddFrame(self.verticalbuttons,ROOT.TGLayoutHints(ROOT.kLHintsLeft|ROOT.kLHintsExpandX,10,500,10,0))



		# connect the buttons to a function
		self.Do_send = ROOT.TPyDispatcher( self.send )

		self.Turn_on_red.Connect    ('Clicked()' , 'TPyDispatcher' , self.Do_send, 'Dispatch()')
		self.Turn_off_red.Connect   ('Clicked()' , 'TPyDispatcher' , self.Do_send, 'Dispatch()')
		self.Turn_on_blue.Connect   ('Clicked()' , 'TPyDispatcher' , self.Do_send, 'Dispatch()')
		self.Turn_off_blue.Connect  ('Clicked()' , 'TPyDispatcher' , self.Do_send, 'Dispatch()')
		self.Turn_on_green.Connect  ('Clicked()' , 'TPyDispatcher' , self.Do_send, 'Dispatch()')
		self.Turn_off_green.Connect ('Clicked()' , 'TPyDispatcher' , self.Do_send, 'Dispatch()')

		#############################################################################################
		###  tab trasmission
		#############################################################################################

		self.tabB = self.tabsFrame.AddTab(" Test Hex Received ")

		self.label_space = ROOT.TGHorizontalFrame(self.tabB, 500, 500, ROOT.kRaisedFrame)
		self.tabB.AddFrame(self.label_space,ROOT.TGLayoutHints(ROOT.kLHintsLeft|ROOT.kLHintsExpandX,10,10,10,0))		  

		self.hext = ROOT.TGGroupFrame( self.label_space, "Hex Trasmitted")
		self.label = ROOT.TGLabel(self.hext, "No input.")
		self.hext.AddFrame(self.label, ROOT.TGLayoutHints(ROOT.kLHintsTop | ROOT.kLHintsLeft,15,15,15,5))

		self.hexr = ROOT.TGGroupFrame( self.label_space, "Hex Received")
		self.label1 = ROOT.TGLabel(self.hexr, "No input.");
		self.hexr.AddFrame(self.label1, ROOT.TGLayoutHints(ROOT.kLHintsTop | ROOT.kLHintsLeft,15,15,15,5));

		self.label_space.AddFrame(self.hext,ROOT.TGLayoutHints(ROOT.kLHintsLeft|ROOT.kLHintsExpandX,10,10,10,0))		  
		self.label_space.AddFrame(self.hexr,ROOT.TGLayoutHints(ROOT.kLHintsLeft|ROOT.kLHintsExpandX,10,10,10,0))

		# TextView Send
		self.textViewsend = ROOT.TGTextViewostream(self.tabB, 100, 200);
		self.tabB.AddFrame(self.textViewsend,ROOT.TGLayoutHints(ROOT.kLHintsExpandX|ROOT.kLHintsExpandY,5,5,5,0))

		# TextView Trasmit from FPGA
		self.textViewtras = ROOT.TGTextViewostream(self.tabB, 100, 200);
		self.tabB.AddFrame(self.textViewtras,ROOT.TGLayoutHints(ROOT.kLHintsExpandX|ROOT.kLHintsExpandY,5,5,5,0))

#		self.ButtonsFrame = ROOT.TGHorizontalFrame( self, 200, 60 )

		##############################################################
		############ tab send received verify
		##############################################################

		self.tabC = self.tabsFrame.AddTab(" Test trasmission ")

		self.space = ROOT.TGHorizontalFrame(self.tabC)

		# TextView Send
		self.verify = ROOT.TGTextViewostream(self.tabC, 100, 200);
		self.tabC.AddFrame(self.verify,ROOT.TGLayoutHints(ROOT.kLHintsExpandX|ROOT.kLHintsExpandY,5,5,5,0))


		##############################################################
		############ last mess on board
		##############################################################

		self.tabD = self.tabsFrame.AddTab(" Last word on board ")

		self.space = ROOT.TGHorizontalFrame(self.tabD)
		
		self.lastButton  = ROOT.TGTextButton( self.tabD, "   &Last word on board   ")
		self.tabD.AddFrame(self.lastButton,ROOT.TGLayoutHints(ROOT.kLHintsLeft|ROOT.kLHintsExpandX,10,500,10,0))
		self.Do_last = ROOT.TPyDispatcher( self.my_last_word )
		self.lastButton.Connect    ('Clicked()' , 'TPyDispatcher' , self.Do_last, 'Dispatch()')

		self.resetButton  = ROOT.TGTextButton( self.tabD, "   &Reset counter   ")
		self.tabD.AddFrame(self.resetButton,ROOT.TGLayoutHints(ROOT.kLHintsLeft|ROOT.kLHintsExpandX,10,500,10,0))
		self.Do_reset = ROOT.TPyDispatcher( self.my_reset )
		self.resetButton.Connect    ('Clicked()' , 'TPyDispatcher' , self.Do_reset, 'Dispatch()')

		# TextView Send
		self.last = ROOT.TGTextViewostream(self.tabD, 100, 200);
		self.tabD.AddFrame(self.last,ROOT.TGLayoutHints(ROOT.kLHintsExpandX|ROOT.kLHintsExpandY,5,5,5,0))


		##############################################################
		## spi
		##############################################################

		self.tabE = self.tabsFrame.AddTab(" Spi ")

		self.space    = ROOT.TGHorizontalFrame(self.tabE)   #, 500,500, ROOT.kRaisedFrame) # kRaisedFrame = high relief
		self.vertical  = ROOT.TGVerticalFrame(self.space)   #, 500,500, ROOT.kRaisedFrame)
		self.vertical2 = ROOT.TGVerticalFrame(self.space)   #, 500,500, ROOT.kRaisedFrame)
		self.vertical3 = ROOT.TGVerticalFrame(self.space)   #, 500,500, ROOT.kRaisedFrame)

		self.spiNumber = ROOT.TGNumberEntry(self.vertical, 0, 9, 999, ROOT.TGNumberFormat.kNESHex, ROOT.TGNumberFormat.kNEANonNegative, ROOT.TGNumberFormat.kNELLimitMinMax, 0, 1048575)
		self.Do_Setlabel = ROOT.TPyDispatcher( self.my_spiNumber_label )
		self.spiNumber.GetNumberEntry().Connect('ReturnPressed()', 'TPyDispatcher' , self.Do_Setlabel, 'Dispatch()')

		self.spiButton  = ROOT.TGTextButton( self.vertical2, "   &Send SPI command to CHIPIX   ")
		self.Do_spiNumber = ROOT.TPyDispatcher( self.my_spiNumber )
		self.spiButton.Connect('Clicked()' , 'TPyDispatcher' , self.Do_spiNumber, 'Dispatch()')

		self.numberframe = ROOT.TGGroupFrame(self.vertical2, "SPI command to send")
		self.label_space.AddFrame(self.numberframe,ROOT.TGLayoutHints(ROOT.kLHintsLeft|ROOT.kLHintsExpandX,10,200,10,0))
		self.label2 = ROOT.TGLabel(self.numberframe, "No input.")
		self.numberframe.AddFrame(self.label2, ROOT.TGLayoutHints(ROOT.kLHintsTop | ROOT.kLHintsLeft,15,200,15,5))

		self.spireceivedButton  = ROOT.TGTextButton( self.vertical3, "   &Received SPI command to CHIPIX   ")
		self.Do_spireceivedButton = ROOT.TPyDispatcher( self.my_received_spi )
		self.spireceivedButton.Connect('Clicked()' , 'TPyDispatcher' , self.Do_spireceivedButton, 'Dispatch()')

		self.number2frame = ROOT.TGGroupFrame(self.vertical3, "Board respoce to SPI command ")
		self.label_space.AddFrame(self.number2frame,ROOT.TGLayoutHints(ROOT.kLHintsLeft|ROOT.kLHintsExpandX,10,200,10,0))
		self.label3 = ROOT.TGLabel(self.number2frame, "No input.")
		self.number2frame.AddFrame(self.label3, ROOT.TGLayoutHints(ROOT.kLHintsTop | ROOT.kLHintsLeft,15,200,15,5))

		self.reset_chipix_Button  = ROOT.TGTextButton( self.tabE, "   &Reset CHIPIX SPI command ")
		self.Do_reset_Button = ROOT.TPyDispatcher( self.reset_Button )
		self.reset_chipix_Button.Connect('Clicked()' , 'TPyDispatcher' , self.Do_reset_Button, 'Dispatch()')

		self.vertical.AddFrame (self.spiNumber, ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft, 50, 5, 5, 5))

		self.vertical2.AddFrame(self.spiButton, ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft, 5, 5, 5, 5))		
		self.vertical2.AddFrame(self.numberframe, ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft, 5, 5, 5, 5))

		self.vertical3.AddFrame(self.spireceivedButton, ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft, 5, 5, 5, 5))
		self.vertical3.AddFrame(self.number2frame, ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft, 5, 5, 5, 5))


		self.space.AddFrame(self.vertical,  ROOT.TGLayoutHints(ROOT.kLHintsLeft, 10, 5, 5, 5))
		self.space.AddFrame(self.vertical2, ROOT.TGLayoutHints(ROOT.kLHintsLeft, 10, 5, 5, 5))
		self.space.AddFrame(self.vertical3, ROOT.TGLayoutHints(ROOT.kLHintsLeft, 10, 5, 5, 5))

		self.tabE.AddFrame(self.reset_chipix_Button,ROOT.TGLayoutHints(ROOT.kLHintsLeft|ROOT.kLHintsExpandX,10,500,10,0))

		self.tabE.AddFrame(self.space, ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft, 50, 5, 20, 5))
		
		
		###############################################################################################
		## in this tabulation graph V vs bit
		###############################################################################################

		self.tabF = self.tabsFrame.AddTab(" Graph V vs Bit ")

		self.h_space    = ROOT.TGHorizontalFrame(self.tabF)   

		self.graph_vertical = ROOT.TGVerticalFrame(self.h_space, 500,500, ROOT.kRaisedFrame)
		self.buttons_vertical = ROOT.TGVerticalFrame(self.h_space, 200,200, ROOT.kRaisedFrame)

		self.my_Canvas  = ROOT.TRootEmbeddedCanvas( 'Canvas', self.graph_vertical, 500, 500 )

#		self.my_Canvas.GetCanvas().Divide(2,1)

		self.graph_button = ROOT.TGTextButton( self.buttons_vertical, " &Generate graph V vs Bit for calibration level   ")
		self.Do_my_plot = ROOT.TPyDispatcher( self.my_plot )
		self.graph_button.Connect('Clicked()' , 'TPyDispatcher' , self.Do_my_plot, 'Dispatch()')

		self.fit_button = ROOT.TGTextButton( self.buttons_vertical, " &Fit graph")
		self.Do_fit = ROOT.TPyDispatcher( self.my_fit )
		self.fit_button.Connect('Clicked()' , 'TPyDispatcher' , self.Do_fit, 'Dispatch()')

#		self.dns_button = ROOT.TGTextButton( self.buttons_vertical, " &DNL ")
#		self.Do_my_plot2 = ROOT.TPyDispatcher( self.my_plot2 )
#		self.dns_button.Connect('Clicked()' , 'TPyDispatcher' , self.Do_my_plot2, 'Dispatch()')


		self.graph_vertical.AddFrame(self.my_Canvas, ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft, 5, 5, 5, 5))
		self.buttons_vertical.AddFrame(self.graph_button, ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft, 5, 5, 5, 5))
		self.buttons_vertical.AddFrame(self.fit_button, ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft, 5, 5, 5, 5))
#		self.buttons_vertical.AddFrame(self.dns_button, ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft, 5, 5, 5, 5))

		self.h_space.AddFrame(self.graph_vertical, ROOT.TGLayoutHints(ROOT.kLHintsLeft, 10, 5, 5, 5))
		self.h_space.AddFrame(self.buttons_vertical, ROOT.TGLayoutHints(ROOT.kLHintsLeft, 10, 5, 5, 5))


		self.tabF.AddFrame(self.h_space, ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsLeft, 5, 5, 5, 5))

		###############################################################################################
		## add buttons and tab frame 
		###############################################################################################

		self.AddFrame(self.topFrame,ROOT.TGLayoutHints(ROOT.kLHintsTop|ROOT.kLHintsExpandX, 0, 0, 0, 0) )
		self.AddFrame(self.tabsFrame,ROOT.TGLayoutHints(ROOT.kLHintsExpandX|ROOT.kLHintsExpandY,10,20,0,0) )

		###################################################################################################
		###  properties definition of the Window 
		###################################################################################################

		# Set a name to the main frame
		self.SetWindowName( 'GUI CHIPIX' )
		self.MapSubwindows()

		# Initialize the layout algorithm via Resize()
		self.Resize( self.GetDefaultSize() )
		
		# Map main frame
		self.MapWindow()
		self.Resize(width, height)


	###################################################################################################
	## distructor
	###################################################################################################


	def __del__(self):
		self.Cleanup()


	####################################################################################################
	##   CloseWindows() override   #####################################################################
	####################################################################################################


	def CloseWindow(self) :
		# verify existence of socket, if there is close it
		try:
			self.s.close()
			self.s.close()
			ROOT.gApplication.Terminate(0)
			raise SystemExit
			#exit()
		except:
			ROOT.gApplication.Terminate(0)
			raise SystemExit
			#exit()


	########################################################################################################
	###    send led signal test for ARTY7 board
	########################################################################################################


	def send(self):

		btn = ROOT.BindObject( ROOT.gTQSender, ROOT.TGTextButton )


	###################################################################################################
	### example led turn on and off, if you change message you can pull up or down brightness
	###################################################################################################


		if btn.WidgetId() == 10:
			MESSAGE = '\x01\x01\x00\x00\x10\x20\x00\xc0' # red turn on
		elif btn.WidgetId() == 20:
			MESSAGE = '\x01\x01\x00\x00\x10\x20\x00\x00' # red turn off
		elif btn.WidgetId() == 30:
			MESSAGE = '\x01\x01\x00\x00\x10\x20\x04\xc0' # green turn on
		elif btn.WidgetId() == 40:
			MESSAGE = '\x01\x01\x00\x00\x10\x20\x04\x00' # green turn off
		elif btn.WidgetId() == 50:
			MESSAGE = '\x01\x01\x00\x00\x10\x20\x08\x40' # blue turn on
		elif btn.WidgetId() == 60:
			MESSAGE = '\x01\x01\x00\x00\x10\x20\x08\x00' # blue turn of

		self.str_send = MESSAGE
		i = 0
		MESSAGEsent = []
		messent = []
		while i < 8:
			MESSAGEsent.append(MESSAGE[i])
			messent.append(MESSAGE[i].encode("hex"))
			if i == 7:
				f.write("0x%s " % MESSAGEsent[i].encode("hex"))
				f.write("\n ")
			else:
				f.write("0x%s " % MESSAGEsent[i].encode("hex"))
			i = i + 1			

		f.closed

		# It displays the value return from the board
   
		self.messent_print = string.join(messent)
		self.label.SetText("%s " % self.messent_print)
		
		self.textViewsend.AddLine("%s " % self.messent_print)
				
		# Parent frame Layout() method will redraw the label showing the new value.

		self.hext.Layout()

		self.send_test = self.messent_print[12:]


	##################################################################################
	## send and test if it has lost the last data
	##################################################################################
		self.s.sendto(self.str_send,(UDP_IP, UDP_PORT))
		self.receivedfromfpga()
		if self.messent_print == self.messtras_print:
			self.verify.AddLine("The message sent is equal the board reply ")
		else:
			self.verify.AddLine("The message sent is not equal, if the last word is not arrived it tries to retrasmet in other case it goes on")
			self.my_verify_Connect()
		#except:
			#print "you must connect the board"
			#ROOT.TPython.Exec( "execfile( \'error_connection.py\')" )       


	###################################################################################################
	## port sniff
	###################################################################################################


	def sniff(self):

		# set read time out 
		self.s.settimeout(0.5)

		# receive data from socket
		d = self.s.recvfrom(64)
		x = d[0]
				
		return x


	####################################################################################################
	##  received
	####################################################################################################


	def receivedfromfpga(self):
		
		messagewrite = []
		messtras = []

		a = self.sniff()

		i = 0
				
		while i < 8:
			messagewrite.append(a[i])
			messtras.append(messagewrite[i].encode("hex"))
			i = i + 1	

		# It displays the value return from the board

		self.messtras_print = string.join(messtras)
		self.label1.SetText("%s " % self.messtras_print)

		self.textViewtras.AddLine("%s " % self.messtras_print)

		# Parent frame Layout() method will redraw the label showing the new value.

		self.hexr.Layout()

		return self.messtras_print


	###################################################################################################
	###  Connect
	###################################################################################################


	def my_Connect(self):
	
		# create dgram udp socket send
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
			print 'Connection occurred for sending' 
		except socket.error:
			print 'Failed to create socket'
			ROOT.TPython.Exec( "execfile( \'error_socket.py\')" )       

		# create dgram udp socket reception
		try:
			#self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
			self.s.bind(("192.168.1.1", 10000))
			self.connectButton.SetTextColor(250)
			print 'Connection occurred for reception' 
		except socket.error:
			print 'Failed to create socket'
			ROOT.TPython.Exec( "execfile( \'error_socket.py\')" )       


	#######################################################################################
	## Help 
	#######################################################################################


	def my_help(self):
		ROOT.TPython.Exec( "execfile( \'help.py\')" )       


	#######################################################################################
	## Last word 
	#######################################################################################


	def my_last_word(self):

		MESSAGE = '\x08\x07\x00\x00\x00\x00\x00\x00' # board reply last memory word
		self.str_send = MESSAGE

		i = 0
		MESSAGEboardsent = []
		mesboardsent = []
		while i < 8:
			MESSAGEboardsent.append(MESSAGE[i])
			mesboardsent.append(MESSAGE[i].encode("hex"))
			if i == 7:
				f.write("0x%s " % MESSAGEboardsent[i].encode("hex"))
				f.write("\n ")
			else:
				f.write("0x%s " % MESSAGEboardsent[i].encode("hex"))
			i = i + 1			

		f.closed

		# It displays the value return from the board
   
		self.mesboardsent_print = string.join(mesboardsent)
		
	## the board is connect? 
		self.s.sendto(self.str_send,(UDP_IP, UDP_PORT))
		self.receivedfromfpga()
		self.last.AddLine(self.messtras_print)
		self.receive_test = self.messtras_print[12:]
		return self.receive_test
	#			print "you must connect the board"
		#	ROOT.TPython.Exec( "execfile( \'error_connection.py\')" )         


	#######################################################################################
	## reset counter in last word 
	#######################################################################################


	def my_reset(self):

		MESSAGE = '\x08\x01\x00\x00\x00\x00\x00\x00' # reset counters
		self.str_send = MESSAGE

		i = 0
		MESSAGEboardsent = []
		mesboardsent = []
		while i < 8:
			MESSAGEboardsent.append(MESSAGE[i])
			mesboardsent.append(MESSAGE[i].encode("hex"))
			if i == 7:
				f.write("0x%s " % MESSAGEboardsent[i].encode("hex"))
				f.write("\n ")
			else:
				f.write("0x%s " % MESSAGEboardsent[i].encode("hex"))
			i = i + 1			

		f.closed

		# It displays the value return from the board
   
		self.mesboardsent_print = string.join(mesboardsent)
			

	## the board is connect? 

		try:
			self.s.sendto(MESSAGE,(UDP_IP, UDP_PORT))
			self.receivedfromfpga()
			self.last.AddLine(self.messtras_print)
		except:
			print "you must connect the board"
			ROOT.TPython.Exec( "execfile( \'error_connection.py\')" )       


	#######################################################################################
	## error, data is lost?
	#######################################################################################

	def my_verify_Connect(self):
		self.my_last_word()
		if self.receive_test == self.send_test:
			print 'send new message'
		else:
			print 'last packet is lost, send another time'

			### to test turn on green led

#			self.str_send = '\x01\x01\x00\x00\x10\x20\x00\xc0'
			self.s.sendto(self.str_send,(UDP_IP, UDP_PORT))


	#######################################################################################
	## spi function
	#######################################################################################


	def my_spiNumber_label(self):
				
		self.manipolation(self.spiNumber.GetNumberEntry().GetHexNumber())		

		self.label2.SetText(" %s " %self.my_newstr_label_out)

		self.numberframe.Layout()


	def manipolation(self,var):

		# trasform dex in hex
		 
		self.keyboardnumber = var

		b = self.keyboardnumber /16
		a1 = (self.keyboardnumber - (b*16)) 

		c = b / 16
		a2 = (b - (c*16))

		d = c / 16
		a3 = (c - (d*16))

		e = d / 16
		a4 = (d - (e*16))

		f = e / 16
		a5 = (e - (f*16))

		self.my_hex_number = [a1,a2,a3,a4,a5]

		## convert log integer to integer

		hex_number = [int(x) for x in self.my_hex_number]
		
		## manipolation of the string 

		i = 0
		while i<5:
			if hex_number[i]>9:
				if hex_number[i] == 10:
					hex_number[i] = 'a'
				elif hex_number[i] == 11:
					hex_number[i] = 'b'
				elif hex_number[i] == 12: 
					hex_number[i] = 'c'
				elif hex_number[i] == 13:
					hex_number[i] = 'd'
				elif hex_number[i] == 14:  
					hex_number[i] = 'e'
				elif hex_number[i] == 15:  
					hex_number[i] = 'f'
				elif hex_number[i]== 9:
					hex_number[i] = '9'
				elif hex_number[i]== 8:
					hex_number[i] = '8'
				elif hex_number[i]== 7:
					hex_number[i] = '7'
				elif hex_number[i]== 6:
					hex_number[i] = '6'
				elif hex_number[i]== 5:
					hex_number[i] = '5'
				elif hex_number[i]== 4:
					hex_number[i] = '4'
				elif hex_number[i]== 3:
					hex_number[i] = '3'
				elif hex_number[i]== 2:
					hex_number[i] = '2'
				elif hex_number[i]== 1:
					hex_number[i] = '1'
				elif hex_number[i]== 0:
					hex_number[i] = '0'
			i = i+1

		# create a key

		# test led on Arty board
#		self.h=['0','1','0','1','0','0','0','0','1','0','2',str(hex_number[4]),str(hex_number[3]),str(hex_number[2]),str(hex_number[1]),str(hex_number[0])]

		# spi 
		self.h=['0','1','0','1','0','0','0','0','4','a','0',str(hex_number[4]),str(hex_number[3]),str(hex_number[2]),str(hex_number[1]),str(hex_number[0])]

		self.h1 = [self.h[0],self.h[1]]
		self.h2 = [self.h[2],self.h[3]]
		self.h3 = [self.h[4],self.h[5]]
		self.h4 = [self.h[6],self.h[7]]
		self.h5 = [self.h[8],self.h[9]]
		self.h6 = [self.h[10],self.h[11]]
		self.h7 = [self.h[12],self.h[13]]
		self.h8 = [self.h[14],self.h[15]]

		self.new_mess1 = string.join(self.h1)
		self.new_mess1 = ''.join(self.new_mess1.split())
		self.new_mess2 = string.join(self.h2)
		self.new_mess2 = ''.join(self.new_mess2.split())
		self.new_mess3 = string.join(self.h3)
		self.new_mess3 = ''.join(self.new_mess3.split())
		self.new_mess4 = string.join(self.h4)
		self.new_mess4 = ''.join(self.new_mess4.split())
		self.new_mess5 = string.join(self.h5)
		self.new_mess5 = ''.join(self.new_mess5.split())
		self.new_mess6 = string.join(self.h6)
		self.new_mess6 = ''.join(self.new_mess6.split())
		self.new_mess7 = string.join(self.h7)
		self.new_mess7 = ''.join(self.new_mess7.split())
		self.new_mess8 = string.join(self.h8)
		self.new_mess8 = ''.join(self.new_mess8.split())
		self.new_str = "\ x"

		self.newstr1 = "".join((self.new_str, self.new_mess1))
		self.newstr2 = "".join((self.new_str, self.new_mess2))
		self.newstr3 = "".join((self.new_str, self.new_mess3))
		self.newstr4 = "".join((self.new_str, self.new_mess4))
		self.newstr5 = "".join((self.new_str, self.new_mess5))
		self.newstr6 = "".join((self.new_str, self.new_mess6))
		self.newstr7 = "".join((self.new_str, self.new_mess7))
		self.newstr8 = "".join((self.new_str, self.new_mess8))

		self.my_newstr_label = [self.newstr1,self.newstr2,self.newstr3,self.newstr4,self.newstr5,self.newstr6,self.newstr7,self.newstr8]
		self.my_newstr = [self.new_mess1,self.new_mess2,self.new_mess3,self.new_mess4,self.new_mess5,self.new_mess6,self.new_mess7,self.new_mess8]

		self.newstr = string.join(self.my_newstr)
		self.newstr = ''.join(self.newstr.split())

		self.mess_to_send = self.newstr.decode('hex')

		self.my_newstr_label_out = string.join(self.my_newstr_label)
		self.my_newstr_label_out = ''.join(self.my_newstr_label_out.split())


	def my_spiNumber(self):

		try:
			# verify the existance of spi command			
			test_existence = self.mess_to_send[0]
			try:
				self.s.sendto(self.mess_to_send,(UDP_IP, UDP_PORT))
			except:
				print "connect the board"
				ROOT.TPython.Exec( "execfile( \'error_connection.py\')" )         

		except:
			print "create a string to send"


############################################################################################
## Reset chipix bottons
############################################################################################


	def reset_Button(self):
		print "RESET the chip"

		MESSAGE = '\x01\x01\x00\x00\x41\x00\x00\x00' # reset board 
		self.str_reset = MESSAGE

		i = 0
		MESSAGEboardsent = []
		mesboardsent = []
		while i < 8:
			MESSAGEboardsent.append(MESSAGE[i])
			mesboardsent.append(MESSAGE[i].encode("hex"))
			if i == 7:
				f.write("0x%s " % MESSAGEboardsent[i].encode("hex"))
				f.write("\n ")
			else:
				f.write("0x%s " % MESSAGEboardsent[i].encode("hex"))
			i = i + 1			

		f.closed

		# It displays the value return from the board
   
		self.mesboardsent_print = string.join(mesboardsent)
		
	## the board is connect? 

		try:
			self.s.sendto(self.str_reset,(UDP_IP, UDP_PORT))
			self.receivedfromfpga()
			self.last.AddLine(self.messtras_print)
			self.receive_test = self.messtras_print[12:]
			return self.receive_test
		except:
			print "you must connect the board"
			ROOT.TPython.Exec( "execfile( \'error_connection.py\')" )         


##############################################################################################
####  received from chip
##############################################################################################


	def my_received_spi(self):

		messagewrite = []
		messtras = []

		a = self.sniff()

		i = 0
				
		while i < 8:
			messagewrite.append(a[i])
			messtras.append(messagewrite[i].encode("hex"))
			i = i + 1	

		# It displays the value return from the board

		self.messtras_print = string.join(messtras)
		self.messtras_print1 = self.messtras_print[16:]
		self.label3.SetText("%s " % self.messtras_print1)

		# Parent frame Layout() method will redraw the label showing the new value.

		self.number2frame.Layout()
		return self.messtras_print1


###################################################################################################
##  Plot the calibration level 
###################################################################################################


	def my_plot(self):
	
		self.my_Canvas.GetCanvas()#.cd(1)
		self.computation()		

		global gr

		Npt = 1024

		gr = ROOT.TGraph(Npt)

		gr.Draw("AP") # if you write "ALP" draw a line from the first to last and go back
		gr.SetMarkerStyle(21)
		gr.SetMarkerSize(0.8)
		gr.SetTitle("Calibration Level;Valori del Cal_Lev(in scala decimale); ")

		for i in range(Npt) :
			x = float(i)			
			y1 = self.y[i]
			gr.SetPoint(i, x, y1)
			ROOT.gPad.Modified()
			ROOT.gPad.Update()


	def my_fit(self):

		self.my_Canvas.GetCanvas().cd(1)
		gr.Fit("pol1","RV","",0, 600)
		f2 = ROOT.TF1("f2", gr.Fit, 0, 600, 2)
		f2.SetParNames("a","b");		
		f2.SetNpx(10000)
		f2.SetLineStyle(1)
		f2.SetLineColor(1)
		f2.SetLineWidth(1)
		f2.Draw
		ROOT.gPad.Modified()
		ROOT.gPad.Update()


	def my_plot2(self):
		
#		self.my_Canvas.GetCanvas().cd(2)

		global gr2

		Npt = 1024

		gr2 = ROOT.TGraph(Npt)

		gr2.Draw("AP") # if you write "ALP" draw a line from the first to last and go back
		gr2.SetMarkerStyle(21)
		gr2.SetMarkerSize(0.8)


		for i in range(Npt) :
			x = float(i)
			y = ROOT.gRandom.Uniform(-0.5, 0.5)
			gr2.SetPoint(i, x, y)
			ROOT.gPad.Modified()
			ROOT.gPad.Update()

	##############################################################################
	##### computation
	##############################################################################

	def computation(self):
		
		t = 0.0004
		## set mux to read the 2 value
		## all number is decimal here
		self.reset_Button()			# reset all GCR, automatically the first of 7 GCR became 0
		time.sleep(t)
		# for reset you can't sniff the port because there is response
		self.manipolation(4104)		# write on 8 GCR 
		self.my_spiNumber()			# send spi command
		self.my_received_spi()		# you must sniff response message to empty the queue
		time.sleep(t)
		self.manipolation(69633)	# bit setting 0001
		self.my_spiNumber()			# send spi command
		self.my_received_spi()		# you must sniff response message to empty the queue
		time.sleep(t)
		## send 1024 value
		self.y = []
		n = 1024					#  we use DAC(10bit) and ADC 12 bit a 40MHz (2^10=1024)
		self.manipolation(4108)		# 12 GCR
		self.my_spiNumber()			# send spi command
		self.my_received_spi()		# you must sniff response message to empty the queue
		time.sleep(t)
		for i in range(n):				# start 0 end 1023
			z = 69632 + i			
			self.manipolation(z)		# set calibration level
			self.my_spiNumber()			# send spi command
			time.sleep(t)			
			self.my_received_spi()		# you must sniff response message to empty the queue
			time.sleep(t)			
			self.manipolation(458752)	# start ADC
			self.my_spiNumber()			# send spi command
			time.sleep(t)			
			self.my_received_spi()		# you must sniff response message to empty the queue
			time.sleep(t)  # sleep for time>0.001s,ADC use to convert possible maximum number 0.000256s
			self.manipolation(983040)	# Read ADC
			self.my_spiNumber()			# send spi command	
			y_tot = self.my_received_spi()	# sniff on board SPI response, command and payload			
			self.y.append(self.ADC10bitfound(y_tot))
		f1.write("0x%s " % self.y)
		f1.write("\n ")
	

	######################################################################################
	## found ADC number and trasform on integer
	#####################################################################################
	def ADC10bitfound(self, hex_word):
		i = 0
		variable = [hex_word[0], hex_word[2], hex_word[3], hex_word[5], hex_word[6]]
		while i<5:
			try:
				variable[i] = int(variable[i])
			except:
				if variable[i] == 'a':
					variable[i] = int(10)
				elif variable[i] == 'b':
					variable[i] = int(11)
				elif variable[i] == 'c':
					variable[i] = int(12)
				elif variable[i] == 'd':
					variable[i] = int(13)
				elif variable[i] == 'e':
					variable[i] = int(14)
				elif variable[i] == 'f':
					variable[i] = int(15)
			i = i + 1
		print variable
		b = variable[4]+variable[3]*16+variable[2]*16*16
		return b


#########################################################################################
#######################################################################################
## Program body
#######################################################################################
###########################################################################################


if __name__ == '__main__':

	a = ROOT.gApplication
	window = my_Canvas( ROOT.gClient.GetRoot(), 900, 650 )
	a.Run()
