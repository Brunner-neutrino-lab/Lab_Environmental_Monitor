
#Sensor toggling: 
#1 turns it on and 0 turns it off
TemperatureStatus = 1
PressureStatus = 1
HumidityStatus = 1
Pressure_DiffStatus = 1   #SPD810
ParticulateStatus = 1     #SPS30
LightSignals = 1          #LED light to indicate when the system is running and when there are problems.

Interval_Between_Scans = 1 # in minutes 
csv_path = 'data/Environmental_Data.csv'  #Path to csv file

#These are the port addresses and have to be modified if the values do not match when <i2cdetect -y 1> is run
#The BME280 measures Temperature, Pressure and Humidity 
addressBME280 = 0x77 # Adafruit BME280 address, also known as the atmospheric sensor. Other BME280s may be different. To obtain it do <i2cdetect -y 1> in the terminal
addressDiff_Pressure = 0x25 #ths should be its i2c address but to verify it run <i2cdetect -y 1> in the terminal
addressSPS30 = 0x69 #for the sps30 dust sensor

#The GPIO pins which are attached to the RGB light
redGPIO = 13
greenGPIO = 19
blueGPIO = 26

