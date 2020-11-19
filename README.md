# sht85
Python driver for Sensirion SHT85 sensors connected to I2c pins of a Raspberrry Pi

## Useage
An example of a periodic query is presented in **test_run_sht85.py**.  
The functions mentioned below are implemented. For the exact usage please refer to the datasheet of sensirion

**single_shot(rep='HIGH'):**  
    Single Shot Data Acquisition Mode
    In this mode one issued measurement command triggers the acquisition of one data pair.
    rep: HIGH, MEDIUM, LOW

**periodic(mps=1,rep='HIGH'): ** 
    Start Periodic Data Acquisition Mode
    In this mode one issued measurement command yields a stream of data pairs.
    In periodicmode different measurement commands can be selected.
    They differ with respect to data acquisition frequency (0.5, 1, 2, 4 & 10 measurements per second, mps) and repeatability (LOW, MEDIUM and HIGH, rep).

**art():**  
    Start the ART (accelerated response time) feature
    After issuing the ART command the sensor will start acquiring data with a frequency of 4Hz
  
**read_data():**  
    Readout of Measurement Results for Periodic Mode or ART feature
    Transmission  of  the  measurement  data  can  be  initiated  through  the  fetch  data  command. After the read out command fetch data has been issued, the data memory is cleared
  
**stop():**  
    Break command / Stop Periodic Data Acquisition Mode or ART feature
    It is recommended to stop  the  periodic  data  acquisition  prior  to  sending  another  command  (except  Fetch  Data  command)  using  the  break command Upon reception of the break command the sensor will abort the ongoing measurement and enter the single shot mode. This takes 1ms.
  
**reset():**  
    Soft Reset
    A system reset of the SHT85 can be generated externally by issuing a command (soft reset). Additionally, a system reset is generated internally during power-up. During the reset procedure the sensor will not process commands. 
    
**heater(heat='on'):**  
    Switch heater on/off
    The SHT85is equipped with an internal heater, which is meant for plausibility checking only.
    
**status():**  
    Status Register
    The status register contains information on the operational status of the heater, the alert mode and on the execution status of the last command and the last write sequence.
    
**clear():**  
    Clear Status Register
    All flags (Bit 15, 11, 10, 4)in the status register can be cleared (set to zero)
    
**sn():**  
    Output of the serial number
    
**dew_point(t,rh):**  
        Calculate dew point from temperature and rel. humidity.
    
