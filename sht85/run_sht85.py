import sht85
import time

mps = 1 # accepted intervals 0.5, 1, 2, 4, 10 seconds
rep = 'HIGH' # Repeatability: HIGH, MEDIUM, LOW

print 'serial number = ', sht85.sn()
time.sleep(0.5e-3)

sht85.periodic(mps,rep)
time.sleep(1)
    while True:
        t,rh = sht85.read_data()
        dp = sht85.dew_point(t,rh)
        print 'Temperature =', t
        print 'Relative Humidity =', rh
        print 'Dew Point =', dp
        time.sleep(mps)

except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print("Killing Thread...")
    time.sleep(0.5e-3)
    sht85.stop()

sht85.stop()
