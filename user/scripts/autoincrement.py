
connect()

reset()

sendSpiFrame(0x09000)

for i in range(14) :
	sendSpiFrame(i | 0x10000)


for i in range(14) :
	sendSpiFrame(0x90000)
