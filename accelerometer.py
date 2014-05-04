from grovepi import *
LSM303_MAG = 0x1E  # assuming SA0 grounded
LSM303_ACC = 0x18  # assuming SA0 grounded

X =0
Y =1
Z =2

CTRL_REG1_A = 0x20
CTRL_REG2_A = 0x21
CTRL_REG3_A = 0x22
CTRL_REG4_A = 0x23
CTRL_REG5_A =0x24
HP_FILTER_RESET_A = 0x25
REFERENCE_A = 0x26
STATUS_REG_A = 0x27
OUT_X_L_A = 0x28
OUT_X_H_A = 0x29
OUT_Y_L_A =0x2A
OUT_Y_H_A =0x2B
OUT_Z_L_A =0x2C
OUT_Z_H_A =0x2D
INT1_CFG_A =0x30
INT1_SOURCE_A =0x31
INT1_THS_A =0x32
INT1_DURATION_A =0x33
CRA_REG_M =0x00
CRB_REG_M =0x01#refer to the Table 58 of the datasheet of LSM303DLM
MAG_SCALE_1_3 =0x20#full-scale is +/-1.3Gauss
MAG_SCALE_1_9 =0x40#+/-1.9Gauss
MAG_SCALE_2_5 =0x60#+/-2.5Gauss
MAG_SCALE_4_0 =0x80#+/-4.0Gauss
MAG_SCALE_4_7 =0xa0#+/-4.7Gauss
MAG_SCALE_5_6 =0xc0#+/-5.6Gauss
MAG_SCALE_8_1 =0xe0#+/-8.1Gauss
MR_REG_M =0x02
OUT_X_H_M =0x03
OUT_X_L_M =0x04
OUT_Y_H_M =0x07
OUT_Y_L_M =0x08
OUT_Z_H_M =0x05
OUT_Z_L_M =0x06
SR_REG_M =0x09
IRA_REG_M =0x0A
IRB_REG_M =0x0B
IRC_REG_M =0x0C

def accMagWrite(addr, data):
	if(addr >= 0x20):
		return bus.write_byte_data(LSM303_ACC, addr, data)
	else:
		return bus.write_byte_data(LSM303_MAG, addr, data)


def accMagRead(addr):
	try:
		if(addr >= 0x20):
			bus.write_byte(LSM303_ACC, addr)
			return bus.read_byte(LSM303_ACC)
		else:
			bus.write_byte(LSM303_ACC, addr)
			return bus.read_byte(LSM303_MAG)
	except IOERROR:
		print "IOERROR"
		return -1

def getAcc():
	raw = {}
	raw['z'] = accMagRead(OUT_X_L_A)<<8 | accMagRead(OUT_X_H_A)
	raw['x'] = accMagRead(OUT_Y_L_A)<<8 | accMagRead(OUT_Y_H_A)
	raw['y'] = accMagRead(OUT_Z_L_A)<<8 | accMagRead(OUT_Z_H_A)
	return raw

def getMag():
	raw = {}
	raw['x'] = accMagRead(OUT_X_H_M)<<8 | accMagRead(OUT_X_L_M)
	raw['z'] = accMagRead(OUT_Y_H_M)<<8 | accMagRead(OUT_Y_L_M)
	raw['y'] = accMagRead(OUT_Z_H_M)<<8 | accMagRead(OUT_Z_L_M)
	return raw

def setup(scale):
	accMagWrite(CTRL_REG1_A, 0x27)
	if((scale==8) or (scale==4)):
		accMagWrite(CTRL_REG4_A, (0x00|(scale-scale/2-1)<<4))
	else:
		accMagWrite(CTRL_REG4_A, 0x00)
	accMagWrite(CRA_REG_M, 0x14)
	accMagWrite(CRB_REG_M, MAG_SCALE_1_3)
	accMagWrite(MR_REG_M, 0x00)

setup(2)
for each in range(0,5):
	print getAcc()
	print getMag()
	time.sleep(.5)
