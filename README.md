# Project Description
The goal of this device is to be able to monitor air quality throughout the day with little maintenance, once the apparatus is fully set up. Everything depends on the Raspberry Pi, a microcontroller that can run programs and connect itself to various sensors. The sensors will measure the temperature, humidity, pressure, and dust levels. The Pi will take readings periodically, which will then be stored locally in the `Environmental_Data.csv` file. The key files of the project are: 
- `config.py` --> It allows the user to modify parameters such as reading and upload intervals, and sensor toggling .
- `Sensors_Functions.py` --> This file contains the functions needed to obtain readings from the sensors.
- `MAIN_PROGRAM.py` --> This file will take periodic readings of the surrounding environment 

# Weather Station Device Setup Guide 

This guide is here to help you connect and set up the different sensors to the Raspberry Pi. Everything works with the default `Raspbian OS`. If one needs help installing it onto the microSD card, visit [**this site**](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/2). If one wants to update their version, visit [**this site**](https://www.raspberrypi.org/documentation/raspbian/updating.md).

Once the OS is set up, and a keyboard and mouse are plugged in, please wire up the sensors as illustrated in the [**diagram**](https://github.com/Brunner-neutrino-lab/Lab_Environmental_Monitor/blob/main/DOCS/Photos/Wiring_Diagram.png). There are writen instructions [**here**](https://github.com/Brunner-neutrino-lab/Lab_Environmental_Monitor/blob/main/DOCS/WiringDiagram.md) if ever you need more details concerning the wiring.

If you are connecting an individual sensor without the use of `i2c`, you may skip over the next section, otherwise enabling the i2c interface is crucial for the sensor connection. The main program connects with all the sensors via the i2c interface. It allows for a more centralized and simple wiring scheme without using too many pins.

## Enabling the I2C interface

For a more detailed guide with photos, go [**here**](https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/).

Otherwise start by typing `sudo raspi-config` into the **Command line**

It will launch the raspi-config utility. From there:
- select **Interfacing Options** :
- Highlight the “I2C” option and activate: **Select**
- Select and activate: **Yes**
- If prompted to reboot highlight and activate: **Yes**

Once the i2c interface is set up and the devices are wired up, run the following command in the terminal: `sudo i2cdetect -y 1`. It will give you all the hexadecimal addresses for the devices which should be double-checked with the ones in the `config.py`. If the values do not match, modify them in the code so it matches the one from the terminal. You will only need to activate the i2c interface once and then you will not have to worry about it anymore.

## Software Setup

The first thing to do is to download the missing packages by entering the following commands in the terminal.

```
sudo apt install python3-pip
sudo apt install libatlas3-base
sudo pip3 install RPi.bme280
```


## How to run

Make sure everything is properly set up and that all the criteria below are met:
- i2c is enabled on the Raspberry Pi.
- The sensors are wired accordingly to the wiring [**diagram**](https://github.com/Brunner-neutrino-lab/Lab_Environmental_Monitor/blob/main/DOCS/Photos/Wiring_Diagram.png).
- The addresses from `i2cdetect -y 1` match the ones found in the `config.py` file.

**Running when connected to a monitor and keyboard/mouse**
If all the requirements above are met, from the folder that contains the `MAIN_PROGRAM.py` program, press `F4` to open the console for that specific folder. Once opened, simply run `sudo python3 MAIN_PROGRAM.py` and it should start running and collecting data. It should print out `Starting!` and the LED should cycle through the colors of the rainbow. If the LED stays red, it means that an error has occured which should be printed in the terminal. 

**Running with remote ssh**
To remote ssh into the Pi, open *windows powershell* and type in `ssh` followed by its ip address. To allow the program to run even if we close the terminal, we will use **Linux screen**. To download it, simply type in `sudo apt install screen`. If you run `screen -ls` and no screens are present, run `screen -S session_name`, where we can name the session as we want. Once inside a screen session, navigate through the directories until you are in the Main_Folder. From there, run `sudo python3 MAIN_PROGRAM.py`. 

To be able to close the terminal without affecting the running program, perform `ctrl+a` `d` to detach the screen. From here you can close the terminal without any problems. The next time you will connect to the Pi and see an active screen after typing `screen -ls` you just need to run `screen -r` to resume it. For more help and guidance, go [here](https://linuxize.com/post/how-to-use-linux-screen/).


----------------

## Adding Additional Sensors

To add additional sensors, ideally they should be connected using the i2c module, making the wiring much easier and straight forward. The code to run the sensor should be in python, since most of the code is written in that language. 

- To start off, create a new variable in the `config.py` file to toggle the sensor on or off. It should be called something like NewSensor**Status** and will take values of either `1` or `0`. Then, in `Sensors_Functions.py` create the new variable: `NewSensor=config.NewSensorStatus`
- Once a systematic method of obtaining readings from the sensor is achieved, simply add a new function in the `Sensors_Functions.py` program before the `header()` function towards the end. The newly-created function should only return the observed reading such as temperature or pressure. No need for timestamps since the `Header()` function takes care of that. 
- In the `Header()` function, add a new "if" statement going along the lines of:
```
if NewSensorStatus==1:
    statement += ',NewSensor_units_used'
```
- Finally, in the `data()` function, add a new "if" statement looking like this:
```
if NewSensorStatus==1:
    statement += ',' + str(NewSensor())
```


## Contributors
- Felix Belair
- Chris Chambers
- Soud Al Kharusi

