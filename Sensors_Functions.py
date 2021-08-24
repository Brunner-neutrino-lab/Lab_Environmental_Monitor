import bme280
from smbus2 import SMBus
import time
import config#config file
import RPi.GPIO as GPIO# this is used for the ligts
from datetime import datetime
if config.ParticulateStatus==1:#we'll only import the sps30 stuff if it is selected in the config file.
    from sps30 import SPS30
import smtplib, ssl# for sending automated emails

'''
The Sensors_Functions.py program is in charge of taking readings from the sensors. 
For instance, if we would print Temperature() in the console, it would return a temperature reading at the moment it was run. 
Similar functions exist for each sensor. At the end of the file, we have the header and the data functions which properly format everything for a .csv file.
The header function generates a header depending on the sensors chosen in the config.py file. 
And for the data function, it generates a string of readings depending on the configuration file. 
'''

# Functions for each sensor. when we call them, they take a reading and return that value
def Temperature():
    #From the atmospheric sensor
    with SMBus(1) as bus:
        bme280.load_calibration_params(bus,config.addressBME280)
        bme280_data = bme280.sample(bus,config.addressBME280)
        ambient_temperature = bme280_data.temperature
    return round(ambient_temperature,3)

def Pressure_atmos():
    #From the atmospheric sensor
    with SMBus(1) as bus:
        bme280.load_calibration_params(bus,config.addressBME280)
        bme280_data = bme280.sample(bus,config.addressBME280)
        pressure = bme280_data.pressure
    return round(pressure*3040/4053,3) #default gives in hPa, but after several heated discussions over which unit to use, we agreed on using Torr. 760 Torr= 1 atmosphere

def Humidity():
    #From the atmospheric sensor
    with SMBus(1) as bus:
        bme280.load_calibration_params(bus,config.addressBME280)
        bme280_data = bme280.sample(bus,config.addressBME280)
        humidity = bme280_data.humidity
    return round(humidity,3)

def diff_pressure():# a tiny time delay is used to prevent errors from taking place.
    with SMBus(1) as bus:
        bus.write_i2c_block_data(config.addressDiff_Pressure, 0x3F, [0xF9]) #Stop any cont measurement of the sensor
        time.sleep(0.5)
        bus.write_i2c_block_data(config.addressDiff_Pressure, 0x36, [0X03]) # The command code 0x3603 is split into two arguments, cmd=0x36 and [val]=0x03
        time.sleep(0.5)
        reading=bus.read_i2c_block_data(config.addressDiff_Pressure,0,9)
        pressure_value=reading[0]+float(reading[1])/255
        if pressure_value>=0 and pressure_value<128:
            diffirential_pressure=round(pressure_value*60/256,3) #scale factor adjustment
        elif pressure_value>128 and pressure_value<=256:
            diffirential_pressure=round(-(256-pressure_value)*60/256,3) #scale factor adjustment
        #it returns the differential pressure in Pa
    return diffirential_pressure

def particulate_sensor():
    #measures the different sized particles in the air, sadly cannot detect neutrinos or subatomic particles.
    with SPS30(1) as sps:
        sps.read_measured_values()
    return [round(sps.dict_values['pm1p0'],2),round(sps.dict_values['pm2p5'],2),round(sps.dict_values['pm4p0'],2),round(sps.dict_values['pm10p0'],2),round(sps.dict_values['nc0p5'],2),round(sps.dict_values['nc1p0'],2),round(sps.dict_values['nc2p5'],2),round(sps.dict_values['nc4p0'],2),round(sps.dict_values['nc10p0'],2),round(sps.dict_values['typical'],2)]

#The header function generates a header for the .csv file. It will give the name for each column along with the units.
def Header():#The header used when uploading the data to the csv file. 
    statement='timestamp'#by default we'll always have the time. 
    if config.TemperatureStatus==1:
        statement+=',Temperature_C'
    if config.PressureStatus==1:
        statement+=',Pressure_Torr'
    if config.HumidityStatus==1:
        statement+=',Percent_Humidity'
    if config.Pressure_DiffStatus==1:
        statement+=',Differential_Pressure_Pa'
    if config.ParticulateStatus==1:
        statement+=',MC1um_ug_per_m3,MC2point5um_ug_per_m3,MC4um_ug_per_m3,MC10um_ug_per_m3,0point5um_Counts_Per_cm3,1um_Counts_Per_cm3,2point5um_Counts_Per_cm3,4um_Counts_Per_cm3,10um_Counts_Per_cm3,Typical_Particle_Size_um'
    return statement

#This is how all the data is collected and stringed together. It is properly formated for the bvl-MongoDB script. 
def data():#The data readings from the sensor. 
    statement=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    if config.TemperatureStatus==1:
        statement+=','+str(Temperature())
    if config.PressureStatus==1:
        statement+=','+str(Pressure_atmos())
    if config.HumidityStatus==1:
        statement+=','+str(Humidity())
    if config.Pressure_DiffStatus==1:
        statement+=','+str(diff_pressure())
    if config.ParticulateStatus==1:
        for x in particulate_sensor():
            statement+=','+str(x)
    return statement

#rgb lights that will tell us if everything is ok.
def lights(setting,period=0):#period is in minutes and is only used for the rainbow lights
    if config.LightSignals==0:#if lights are disabled, it will just skip over it.
        return None
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)# this means that we are refering to the BCM Pi pins and not the Board pin numbers
    GPIO.setup(config.greenGPIO,GPIO.OUT)#Defining all the LED gpio pins as outputs for the Pi
    GPIO.setup(config.redGPIO,GPIO.OUT)
    GPIO.setup(config.blueGPIO,GPIO.OUT)
    if setting == 'green':
        GPIO.output(config.redGPIO,GPIO.LOW)#turns off all the other colors other than the selected one
        GPIO.output(config.blueGPIO,GPIO.LOW)
        GPIO.output(config.greenGPIO,GPIO.HIGH)
    if setting == 'off':
        GPIO.cleanup()#tunrs off all the pins
    if setting == 'red':
        GPIO.output(config.blueGPIO,GPIO.LOW)
        GPIO.output(config.greenGPIO,GPIO.LOW)
        GPIO.output(config.redGPIO,GPIO.HIGH)
    
    if setting == 'rainbow':#Soud's special request!!!
        RED = GPIO.PWM(config.redGPIO, 100)  
        GREEN = GPIO.PWM(config.greenGPIO, 100)
        BLUE = GPIO.PWM(config.blueGPIO, 100)
        for i in range(int(4*period)):#it takes 15 seconds to cycle through the colors, we multiply it by 4 to make a minute and the period is chosen by the user.
            RED.start(100)
            GREEN.start(1)
            BLUE.start(1)
            for x in range(1,101):#power consciencious HSV curve
                GREEN.ChangeDutyCycle(x)
                RED.ChangeDutyCycle(101-x)
                time.sleep(0.05)
            for x in range(1,101):
                GREEN.ChangeDutyCycle(101-x)
                BLUE.ChangeDutyCycle(x)
                time.sleep(0.05)
            for x in range(1,101):
                RED.ChangeDutyCycle(x)
                BLUE.ChangeDutyCycle(101-x)
                time.sleep(0.05)

def send_message(message):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(config.sender_email, config.password)
        server.sendmail(config.sender_email, config.receiver_email, message)
    return None

