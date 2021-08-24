
# Brief Overview 

The goal of the project is to record environmental variables continuously over years with the use of various sensors such as a particulate counter or pressure differential sensor, to then upload the data to a server using a Raspberry Pi. Using various python submodules specific to each sensor, properties such as temperature, pressure differential, humidity, and dust levels are monitored and uploaded to a database at periodic time intervals. This would allow the user to verify whether the lab has a positive pressure differential relative to the outside to keep the dust out and to correlate when and how the dust particles enter. A 3d-printed case has been designed to package all these components together.

# Parts Needed 

* [Raspberry Pi 4](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/) (The mastermind behind the project)
* [SPS30](https://www.sensirion.com/en/environmental-sensors/particulate-matter-sensors-pm25/) (Dust sensor)
* [SDP810](https://www.sensirion.com/en/flow-sensors/differential-pressure-sensors/sdp800-proven-and-improved/) (Pressure Differential sensor)
* [BME280](https://www.sparkfun.com/products/15440) (Atmospheric sensor that measures the Temperature, Humidity and Pressure)
* [Fan](https://www.sparkfun.com/products/15504) (will be placed above the Pi for it to cool off efficiently)
* [Small Soldering Board](http://www.proto-advantage.com/store/product_info.php?products_id=200062) (compact way to wire everything)
* 4x M2.5x6mm Standoffs (Raises the Pi slightly off the ground)--Must use this dimension since the openings for the Pi rely on the 6mm standoffs. McMaster-CARR number part:98952A103 
* 4x M2.5x12mm Standoffs (Raises the fan above the Pi)--Other heights may be used such as 14mm or 16mm if you do not have 12mm standoffs. McMaster-CARR number part:98952A109 
* 19x M2.5 Threaded Inserts (Allows us to use screws) McMaster-CARR number part:94180A321
* 10x M2.5x8mm Screws (used to attach fan onto the bracket, the lid, and SPS30) McMaster-CARR number part:91292A012
* 7x M2.5x10mm Screws (used to attach the BME280 and bottom part of the case) McMaster-CARR number part:91292A014
* 2x M2.5x16mm Screws (used to attach the SDP810) McMaster-CARR number part:91292A018
* 4x M4x16mm Screws (used for the fan) McMaster-CARR number part:90751A119
* 4x M4 nuts (also used for the fan) McMaster-CARR number part:91415A020
* Header pins (male and female)
* Jumper wires

# Software 

All the essentials can be found under the Main_Folder. 
* **The config.py** file can be modified by the user if ever they want to change something such as the time interval between scans or the I2C addresses for the sensors.
* **The MAIN_PROGRAM.py** does the data collection and the data upload.
* **The Sensors_Functions.py** is responsible for obtaining readings for all the sensors and for formatting the data that will be sent to the database. A python function is created for each sensor, and when called, returns a reading from that particular sensor. 

## Data File Format
The data being acquired is stored with headers....

* **timestamp:** This is the time at which the data was taken. The format is YYYY-MM-DD hh:mm:ss.
* **Temperature_C:** This is the temperature of the lab measured in Celsius. The readings should be around 21 degrees or so.
* **Pressure_Torr:** This is the pressure of the lab in Torr. Typically, the readings should be near 760Torr, which is the equivalent of 1 atmosphere.
* **Percent_Humidity:** This is the relative humidity in the air. At a given temperature, air can hold a certain amount of water vapor. Here it gives the ratio between the measured amount of water vapor present to the max carrying capacity at a given temperature.
* **Differential_Pressure_Pa:** This is the difference in pressure between the 2 nobs on the SDP810, measured in Pascale. Once the SDP810 is placed inside the case, it will measure the pressure from the nozzle on right minus the pressure of the nozzle on the left, when viewed from this angle: [https://github.com/Brunner-neutrino-lab/Lab_Environmental_Monitor/blob/main/DOCS/Photos/SDPNozzle.jpg]


It can give out both positive and negative values for the pressure difference, depending on which nozzle reads a higher pressure. This information comes from a diagram from this [https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/8_Differential_Pressure/Datasheets/Sensirion_Differential_Pressure_Datasheet_SDP8xx_Digital.pdf data sheet ]. 

[
The sensor will return the difference between the High pressure nozzle to the Low pressure one in the diagram.

*'''MC1um_ug_per_m3:''' This measures the mass concentration of particles between 0.3um to 1um for a given volume of 1 meter cube in ug. In other words, take 1 meter cube of air and weigh all the particles between 0.3um and 1um and the total mass is the returned final reading (in ug). 
*'''MC2point5um_ug_per_m3:''' This measures the mass concentration of particles between 0.3um to 2.5um for a given volume of 1 meter cube in ug. In other words, take 1 meter cube of air and weigh all the particles between 0.3um and 2.5um and the total mass is the returned final reading (in ug). 
*'''MC4um_ug_per_m3:''' This measures the mass concentration of particles between 0.3um to 4um for a given volume of 1 meter cube in ug. In other words, take 1 meter cube of air and weigh all the particles between 0.3um and 4um and the total mass the final reading. 
*'''MC10um_ug_per_m3:''' This measures the mass concentration of particles between 0.3um to 10um for a given volume of 1 meter cube in ug. In other words, take 1 meter cube of air and weigh all the particles between 0.3um and 10um and the total mass is the returned final reading (in ug).
*'''0point5um_Counts_Per_cm3:''' This measures the number of particle counts between 0.3um to 0.5um for a given volume of 1 centimeter cube. In other words, take 1 centimeter cube of air and count all the particles between 0.3um and 0.5um and return the number of counts.
*'''1um_Counts_Per_cm3:''' This measures the number of particle counts between 0.3um to 1um for a given volume of 1 centimeter cube. In other words, take 1 centimeter cube of air and count all the particles between 0.3um and 1um and return the number of counts.
*'''2point5um_Counts_Per_cm3:''' This measures the number of particle counts between 0.3um to 2.5um for a given volume of 1 centimeter cube. In other words, take 1 centimeter cube of air and count all the particles between 0.3um and 2.5um and return the number of counts.
*'''4um_Counts_Per_cm3:''' This measures the number of particle counts between 0.3um to 4um for a given volume of 1 centimeter cube. In other words, take 1 centimeter cube of air and count all the particles between 0.3um and 4um and return the number of counts.
*'''10um_Counts_Per_cm3:''' This measures the number of particle counts between 0.3um to 10um for a given volume of 1 centimeter cube. In other words, take 1 centimeter cube of air and count all the particles between 0.3um and 10um and return the number of counts.
*'''Typical_Particle_Size_um:''' The typical particle size (TPS) gives an indication on the average particle diameter in the sample aerosol in um. Such output correlates with the weighted average of the number concentration bins measured with a TSI 3330 optical particle sizer. Consequently, lighter aerosols will have smaller TPS values than heavier aerosols.

# Physical Design 
Once all the components have been acquired (Raspberry Pi and sensors), a case has been designed to package everything together. The case is 3d printed and the ''SolidWorks'' design files can be found in this [https://workbench.grabcad.com/workbench/projects/gcHzfLMLa-HXbQJv8QlMMii0fpi4dDAn0PsYPM48OZWLoZ#/folder/10605921 GrabCAD project]([File:SDP810_Sketch.png|300px]]). At the moment, we are using the '''Top_Fan_configuration''' design, where the fan lies above the Raspberry Pi to cool it off. In that folder, the '''3D print''' folder contains all the parts that have to be printed (lid, main body, fan bracket, bottom case).

## Assembly Instructions (Top Fan Configuration)

To start, make sure you have all the material listed above and that the case components have been printed. 

### Fan and Bracket


* With the use of the '''M4 nuts''' and '''M4x16mm screws''', clamp the fan onto the bracket. Ideally, the fan should be oriented such that the air should flow from below the bracket through the fan. This would ensure that the hot air is leaving the chip and going out of the case.
Here are 2 photos showing how it should look like once attached. 

[[[File:Fan_Bracket1.jpg|300px]([File:Fan_Bracket2.jpg|300px]])]

Once this component is assembled, put it aside and we will use it in a few steps.

### Case Bottom


* Heat up and place the '''M2.5 threaded inserts''' into the 4 prearranged holes near the vent slits. They will be used to mount the Raspberry Pi.
* Once placed, screw in the '''M2.5x6mm Standoffs'''.

[
* We can then proceed to mount the '''Raspberry Pi''' onto the corresponding standoffs by securing it with '''M2.5x12mm Standoffs'''. Make sure that the side with the USB and Ethernet ports is near the edge of the case and not the other way around. The 12mm standoffs will be used to place the fan above the Pi.

[[File:Case_Pi.jpg|300px]([File:Case_Bottom_threaded_insert.jpg|300px]])]

* From there, we can take the Bracket-Fan component that we assembled in the first step, and mount it onto the standoffs using '''M2.5x8mm screws'''. For an optimal wiring experience, be sure to orient the bracket such that a hole is placed above the Raspberry Pi GPIO pins.

[
### Main Body


* In the four outer corners of the main body of the case, heat up and place the '''M2.5 threaded inserts''' into the prearranged holes. Do this for the top and bottom holes of the corners.
* In all the inner holes of the case, heat up and place the '''M2.5 threaded inserts''' into the prearranged holes. This includes 2 for the SPS30, 3 for the BME280 and 2 for the SDP810.
* Place the '''SPS30''' in its assigned corner and fix it into place with 2 '''M2.5x8mm screws'''. Make sure the openings in the case align with the air intakes/outtakes of the sensor. 
* Place the '''SDP810''' by passing its 2 nozzles through the 2 wider holes. Make sure that it is oriented the right way up, such that its mounting holes align with the threaded inserts we placed earlier. Use 2 '''M2.5x16mm''' screws to secure it into place.
* The order of these steps is important since we cannot place the SDP810 once the BME280 is already placed. So once the SDP810 is mounted, we can now mount the '''BME280''' by inserting 3 '''M2.5x10mm screws'''. Make sure that the sensor component (the little box positioned in the middle) is facing outwards and aligned with the little opening.

[[File:Case_Insert_Overview.jpg|300px]([File:Case_Fan.jpg|300px]])]

[
### Soldering Board


* Using the small solder board, solder in a group of '''4 header pins''' for the RGB LED and a group of '''6 header pins''' for the rest of the sensors and the fan (the corresponding rows will be: 5V, 3.3V, SCL, SDA, Ground, Ground). The positioning is arbitrary, but in the photo, the header pins are placed in the upper row. These pins will be connected to the Pi with wires and the slots below them will connect to the various sensors. The use of the header pins allows us to rearrange a configuration without losing too much time. 

[[File:Solder_Board_Back.jpg|300px]([File:Sensors_Insert.jpg|300px]])]  In this photo, the 4 header pins for the RGB LED are placed on the far left, and the 6 others are placed on the right side of the board, all of which are on the top row.

* Flip the board over and solder in the '''RGB LED''' below the 4 header pins. Once the LED has been soldered, solder in '''female header pins''' in the same arrangement as the image below. 

[
### Wiring



* After all the pins have been soldered, each sensor will connect their '''Ground, power source (3V or 5V), SDA, and SCL''' wires to their corresponding columns. The BME280 and SDP810 will use the first 2 rows (the order does not matter) since they both need the same 4 pins: 3V, SDA, SCL, and ground. The row with 6 pins is for the SPS30, as it will use everything except for the 3V pin (it is easier to solder in 6 consecutive pins, rather than having a hole in the middle). Finally, the fan will only use the 5V and the ground pin in the bottom row. If you take a closer look at the previous image (by clicking on it), you will see a column layout that has worked. From there, all the SDA pins will group up in the same column. The same is done for all the other pin types mentioned above (Ground, 3V, 5V, SDA, SCL). 


Wire layout for each sensors:
* If we look at the the '''SPS30''' (dust sensor) with the metal cap facing right and the wires pointing towards us, the top pin is #1 and the one in the bottom is #5. Then the pin roles are:
    * pin 1: 5V    (be careful to not connect it with the other 3.3V)
    * pin 2: SDA
    * pin 3: SCL
    * pin 4: Ground
    * pin 5: Ground (Very important to connect both grounds)

* If we look at the '''SDP810''' (pressure differential sensor) with the logo Sensirion facing upright. The pin on the very left will be pin 4 and the pin on the far right will be pin 1. 
    * Pin1 SCL
    * Pin2 3.3V
    * Pin3 Ground
    * Pin4 SDA

For the '''BME280''', the pins should be physically labeled, so no worries there. Do not worry if there are some unused pins on the BME280, since we only use 3V, Ground, SDA and SCL.

For the '''Raspberry Pi''', this photo should help out a bit.

[[File:RPi4GPIO.jpg|400px]([File:Solder_Board_Top.jpg|300px]])]

*GPIO2 is for SDA and GPIO3 is for SCL.
*By default, the pins for the '''RGB LED''' are Red: GPIO13, Green: GPIO19, Blue: GPIO26. 

Here is a wiring diagram to help out. 

[
You can visit this [http://132.206.126.37/bvllab/particulate-sensor/tree/master/DOCS/Photos folder]([File:LWS_Wiring_Diagram.png|600px]]) for further guidance. 

At first, it may look a little messy...

[
but once the Pi is wired up and we orient things a little better, things can place out to look like this:

[[File:Wires_Pi.jpg|300px]([File:Bunch_of_wires.jpg|300px]])]

### Final Assembly


* Once things are wired up properly, flip the case over and mount the '''Case Bottom''' onto the Main Body with 4 '''M2.5x10mm''' screws. 
* Finally, flip the case over one last time to secure the '''Case Lid''' onto the Main Body with 4 '''M2.5x8mm''' screws.
[
* It is also crucial to stick on at least one '''BvL''' sticker onto the case as shown in the photo :D

# Measurement Locations
When recording data, the location of the weather station should be noted as well in the database collection name. The location can be expressed as a x and y coordinate. For instance, if the case is placed on the 020 Workbench, its coordinate would be 31. 3 for x and 1 for y (yes positive y is down :D so no negatives). In the database, its collection would be LWS001-loc31.


[[File:Pi_Placements.png|400px]([File:Final.jpg|300px]])]

# Known Issues

* If it is the first time running the program since it was last updated and errors are returned before it returns any readings, try rerunning the program once or twice.

* Another issue could be a wiring problem. Make sure all the components are wired properly. Take time to douche-check the wiring diagram to see if all the connections follow it. Make sure an electrical contact is properly made for all the sensors. It may be obvious if it is a jumper wire that is disconnected, but not so obvious if its the connector for the SPS30 or SDP810.
