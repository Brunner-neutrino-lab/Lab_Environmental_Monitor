import time  #I hope you know what the time module does
import config #all the settings the user can modify
import Sensors_Functions # functions used to obtain readings from the sensors

Sensors_Functions.lights('off') #turning the LED off
with open(config.csv_path,'w') as update_log:#this writes the header in the empty .csv file
        update_log.write(Sensors_Functions.Header()+'\n')
        update_log.close()
StartTime=time.time() #Start and End time will be used to calculate the time ellapsed since the program started 
print('Starting!')
while True:
    try:
        #This part uploads the readings to the CSV file
        with open(config.csv_path,'a') as update_log:# Writing to the .csv file
            update_log.write(Sensors_Functions.data()+'\n')# the new line is to skip a line in the csv file so that all the columns are alligned.
            update_log.close()
        print(Sensors_Functions.data())
        EndTime=time.time()
        if config.LightSignals==1:#if lights are connected, the waiting time will have rainbow lights, otherwise it'll be boring :((. At the end of the day, the waiting time stays the same, but the one with the rainbow LED will always be awesomer :D 
            Sensors_Functions.lights('rainbow',config.Interval_Between_Scans)
        else:
            time.sleep(60*config.Interval_Between_Scans)#The time in minutes that the user chose to have between readings. Also the rate at which the uploading time increases by.
            
    except KeyboardInterrupt:#uploads everything once we close the program
        print('closing down')
        with open(config.csv_path,'a') as update_log:
            update_log.write(Sensors_Functions.data()+'\n')# the new line is to skip a line in the csv file so that all the columns are alligned.
            update_log.close()
        print('Fully uploaded!')
        Sensors_Functions.lights('off')
        break #Closes off the loop. No need to write another header.
    
    except Exception as error:
        Sensors_Functions.lights('off')
        Sensors_Functions.lights('red')#Red LED means that something went wrong
        print('Houston,we have a problem')#is it ok for me to put this here?
        print(error)
        time.sleep(5)

