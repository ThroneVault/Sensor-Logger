'''
Created on Jan 26, 2016

@author: work
'''

import Adafruit_GPIO.FT232H as FT232H
import struct

# Temporarily disable FTDI serial drivers.
FT232H.use_FT232H()
# Find the first FT232H device.
ft232h = FT232H.FT232H()

class L3G4200DDriver:
    #gyro defines - ST L3G2
    L3G_CTRL_REG1 = 0x20
    L3G_CTRL_REG2 = 0x21
    L3G_CTRL_REG3 = 0x22
    L3G_CTRL_REG4 = 0x23
    L3G_CTRL_REG5 = 0x24
    L3G_OUT_X_L   = 0x28
    L3G_WHO_AM_I  = 0x0F
    L3G_I2C_ADDR  = 0x69#0110 1001   
    READ = 0x80
 
    def __init__(self):

        self.gyro = FT232H.I2CDevice(ft232h,self.L3G_I2C_ADDR,400000)
        
    def Setup(self):
        #whoAmI = gyro.readU8(L3G_WHO_AM_I)
        #print format(whoAmI,'02x')
        #print (bin(whoAmI))
        self.gyro.write8(self.L3G_CTRL_REG2, 0x00)
        self.gyro.write8(self.L3G_CTRL_REG3, 0x00)
        self.gyro.write8(self.L3G_CTRL_REG4, 0x20)
        self.gyro.write8(self.L3G_CTRL_REG5, 0x02)
        self.gyro.write8(self.L3G_CTRL_REG1, 0x8F)     

    def Read(self):
        gyroByteList = self.gyro.readList(self.L3G_OUT_X_L | self.READ, 6)
        gyroIntList = struct.unpack('hhh',gyroByteList[0:6])
        return gyroIntList;
    

class LSM303DLHAccDriver:
    #ACC defines
    ACC_ADDRESS       = 0x18#0001 1000
    CTRL_REG1_A       = 0x20
    CTRL_REG2_A       = 0x21
    CTRL_REG3_A       = 0x22
    CTRL_REG4_A       = 0x23
    CTRL_REG5_A       = 0x24
    CTRL_REG6_A       = 0x25
    HP_FILTER_RESET_A = 0x25
    REFERENCE_A       = 0x26
    STATUS_REG_A      = 0x27
    
    OUT_X_L_A         = 0x28
    OUT_X_H_A         = 0x29
    OUT_Y_L_A         = 0x2A
    OUT_Y_H_A         = 0x2B
    OUT_Z_L_A         = 0x2C
    OUT_Z_H_A         = 0x2D
    
    READ = 0x80
    
    def __init__(self):
        self.acc = FT232H.I2CDevice(ft232h,self.ACC_ADDRESS,400000) 
    
    def Setup(self):
        self.acc.write8(self.CTRL_REG1_A, 0x3F)
        self.acc.write8(self.CTRL_REG2_A, 0x00)
        self.acc.write8(self.CTRL_REG3_A, 0x00)
        self.acc.write8(self.CTRL_REG4_A, 0x30)
        self.acc.write8(self.CTRL_REG5_A, 0x00)
        
    def Read(self):
        accByteList = self.acc.readList(self.OUT_X_L_A | self.READ, 6)
        accIntList = struct.unpack('hhh',accByteList[0:6])
        return accIntList    
        
#end classes ---------------------------------------------------------        
gyro = L3G4200DDriver()
acc = LSM303DLHAccDriver()

gyro.Setup()
acc.Setup()

print gyro.Read()
print acc.Read()























