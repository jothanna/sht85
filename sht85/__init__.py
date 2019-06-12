
# Modules
import smbus
import time
import math

bus = smbus.SMBus(1)

# SHT85 hex adress
SHT85_ADDR       = 0x44 # Device Adress
SHT85_SS         = 0x24 # Single Shot Data Acquisition Mode
SHT85_SS_2       = {'HIGH' : 0x00, 'MEDIUM' : 0x0B, 'LOW' : 0x16} # Repeatability: (HIGH, MEDIUM, LOW)
SHT85_P          = {0.5 : 0x20, 1 : 0x21, 2 : 0x22, 4 : 0x23, 10 : 0x27} # Periodic Data Acquisition Mode mps
SHT85_P_2        = {0.5 : (0x32,0x24,0x2F), 1 : (0x30,0x26,0x2D), 2 : (0x36,0x20,0x2B), 4 : (0x34,0x22,0x29), 10 : (0x37,0x21,0x2A)} # Repeatability: (HIGH, MEDIUM, LOW)
SHT85_ART        = 0x2B # ART Command (accelerated response time) frequency of 4Hz
SHT85_ART_2      = 0x32
SHT85_STOP       = 0x30 # Break command / Stop Periodic Data Acquisition Mode
SHT85_STOP_2     = 0x93
SHT85_RESET      = 0x30 # Soft Reset
SHT85_RESET_2    = 0xA2
SHT85_HEATER     = 0x30 # Heater for plausibility checking
SHT85_HEATER_ON  = 0x6D # enable
SHT85_HEATER_OFF = 0x66 # disable
SHT85_STATUS     = 0xF3 # Status Register
SHT85_STATUS_2   = 0x2D
SHT85_CLEAR      = 0x30 # Clear Status Register
SHT85_CLEAR_2    = 0x41
SHT85_SN         = 0x36 # Serial Number
SHT85_SN_2       = 0x82

SHT85_READ       = 0x00 # Read output

def single_shot(rep='HIGH'):
    '''
    Single Shot Data Acquisition Mode
    In this mode one issued measurement command triggers the acquisition of one data pair.
    '''
    bus.write_i2c_block_data(SHT85_ADDR,SHT85_SS,[SHT85_SS_2[rep]])
    time.sleep(0.5)
    data   = bus.read_i2c_block_data(SHT85_ADDR,SHT85_READ,6)
    t_data = data[0] << 8 | data[1]
    h_data = data[3] << 8 | data[4]
    temp = -45. + 175. * t_data / (2**16-1.)
    relh = 100. * h_data / (2**16-1.)
    return round(temp,4), round(relh,4)

def periodic(mps=1,rep='HIGH'):
    ''' 
    Start Periodic Data Acquisition Mode
    In this mode one issued measurement command yields a stream of data pairs.
    In periodicmode different measurement commands can be selected.
    They differ with respect to data acquisition frequency (0.5, 1, 2, 4 & 10 measurements per second, mps) and repeatability (LOW, MEDIUM and HIGH, rep).
    '''
    rep_dict = {'HIGH' : 0, 'MEDIUM' : 1, 'LOW' : 2}
    rep = rep_dict[rep]
    bus.write_i2c_block_data(SHT85_ADDR,SHT85_P[mps],[SHT85_P_2[mps][rep]])
    time.sleep(0.5e-3)
    return 'Periodic Data Acquisition Mode started'

def art():
    '''
    Start the ART (accelerated response time) feature
    After issuing the ART command the sensor will start acquiring data with a frequency of 4Hz
    '''
    bus.write_i2c_block_data(SHT85_ADDR,SHT85_ART,[SHT85_ART_2])
    return 'ART Comannd started'

def read_data():
    '''
    Readout of Measurement Results for Periodic Mode or ART feature
    Transmission  of  the  measurement  data  can  be  initiated  through  the  fetch  data  command. After the read out command fetch data has been issued, the data memory is cleared
    '''
    data   = bus.read_i2c_block_data(SHT85_ADDR,SHT85_READ,6)
    t_data = data[0] << 8 | data[1]
    h_data = data[3] << 8 | data[4]
    temp = -45. + 175. * t_data / (2**16-1.)
    relh = 100. * h_data / (2**16-1.)
    return round(temp,4), round(relh,4)

def stop():
    '''
    Break command / Stop Periodic Data Acquisition Mode or ART feature
    It is recommended to stop  the  periodic  data  acquisition  prior  to  sending  another  command  (except  Fetch  Data  command)  using  the  break command Upon reception of the break command the sensor will abort the ongoing measurement and enter the single shot mode. This takes 1ms.
    '''
    bus.write_i2c_block_data(SHT85_ADDR,SHT85_STOP,[SHT85_STOP_2])
    return 'Break'

def reset():
    '''
    Soft Reset
    A system reset of the SHT85 can be generated externally by issuing a command (soft reset). Additionally, a system reset is generated internally during power-up. During the reset procedure the sensor will not process commands. 
    '''
    bus.write_i2c_block_data(SHT85_ADDR,SHT85_RESET,[SHT85_RESET_2])
    return 'Reset'

def heater(heat='on'):
    '''
    Switch heater on/off
    The SHT85is equipped with an internal heater, which is meant for plausibility checking only.
    '''
    if heat == 'on':
        heat = SHT85_HEATER_ON
    elif heat == 'off':
        heat = SHT85_HEATER_OFF
    bus.write_i2c_block_data(SHT85_ADDR,SHT85_HEATER,[heat])
    return 'heater is ', heat

def status():
    '''
    Status Register
    The status register contains information on the operational status of the heater, the alert mode and on the execution status of the last command and the last write sequence.
    '''
    bus.write_i2c_block_data(SHT85_ADDR,SHT85_STATUS,[SHT85_STATUS_2])
    time.sleep(0.5e-3)
    status_read = bus.read_i2c_block_data(SHT85_ADDR,SHT85_READ,3)
    status_to_bit = bin(status_read[0] << 8 | status_read[1])
    status_dict={'checksum status'      : status_to_bit[0],
                 'Command status'       : status_to_bit[1],
                 'System reset'         : status_to_bit[4],
                 'T tracking alert'     : status_to_bit[10],
                 'RH tracking alert'    : status_to_bit[11],
                 'Heater status'        : status_to_bit[13],
                 'Alert pending status' : status_to_bit[15]
                }
    return status_dict

def clear():
    '''
    Clear Status Register
    All flags (Bit 15, 11, 10, 4)in the status register can be cleared (set to zero)
    '''
    bus.write_i2c_block_data(SHT85_ADDR,SHT85_CLEAR,[SHT85_CLEAR_2])
    return 'Status Register cleared'

def sn():
    '''
    Output of the serial number
    '''
    bus.write_i2c_block_data(SHT85_ADDR,SHT85_SN,[SHT85_SN_2])
    time.sleep(0.5e-3)
    sn_read = bus.read_i2c_block_data(SHT85_ADDR,SHT85_READ,6)
    sn = sn_read[0] << 16 | sn_read[4]
    return sn

def dew_point(t,rh):
    '''
    Calculate dew point from temperature and rel. humidity.
    '''
    t_range = 'water' if t >= 0 else 'ice'
    tn = dict(water=243.12, ice=272.62)[t_range]
    m = dict(water=17.62, ice=22.46)[t_range]

    dew_p = tn * (math.log(rh / 100.0) + (m * t) / (tn + t))/ (m - math.log(rh / 100.0) - m * t / (tn + t))
    return round(dew_p,4)






