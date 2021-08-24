### Quick overview
For each sensor we will only need 4 connections: SDA, SCL, Voltage source, and ground. Even if there may be extra pins on the sensors, we will only need the 4 aforementioned pins. Since each sensor has a unique i2c address, all the SCL pins can be grouped up in the same column on a breadboard. The same should be done for the SDA pins. There are a few details concerning the power supply since the SPS30 uses 5V rather than 3.3V. Once all the wiring info is settled, you may wire up your sensors accoring to the [diagram](http://132.206.126.37/bvllab/particulate-sensor/blob/master/DOCS/Photos/Wiring_Diagram.png). To start off, we will first have to figure out which wires will do what.


### Pin labeling

For the **BME280**, the pins roles should be physically labeled on the sensor itself, so you shouldn't break a sweat for it. Soldering header pins is something I would recommend if it hasn't been done yet for that sensor. Do not worry if there are a few pins that will remain unused.

---------------------------------------------------------

If we look at the the **SPS30** (dust sensor) with the metal cap facing up, the pin on the left is pin 1 and the one on the right is pin 5. The pin roles are:

- pin 1: 5V    (be careful to not connect it with the other 3.3V)
- pin 2: SDA
- pin 3: SCL
- pin 4: Ground 
- pin 5: Ground (Very important to connect both grounds)

The reason why there are 2 ground wire connections, is because pin 4 determines how we connect the device. If it hangs there doing nothing, we select UART, and if we ground it, it chooses the i2c interface, which is what we are using. Furthermore, the ground pins cannot be connected with the ones from the other sensors since the voltage is different. For further guidance, here is a [diagram](http://132.206.126.37/bvllab/particulate-sensor/blob/master/DOCS/Photos/SPS30.png) of the sensor.

---------------------------------------------------------

If we look at the **SDP810** (pressure differential sensor) with the logo *Sensirion* facing upright. The pin on the very left will be **pin 4** and the pin on the far right will be **pin 1**. Please note that the order of the wires is different from the SPS30. For further guidance, here is a [diagram](http://132.206.126.37/bvllab/particulate-sensor/blob/master/DOCS/Photos/SDP810.png) of the sensor.

- Pin1 SCL
- Pin2 3.3V
- Pin3 Ground
- Pin4 SDA


---------------------------------------------------------
and finally for the Raspberry Pi we have:

- pin 1: 3.3V
- pin 2: 5V
- pin 3: GPIO2 ==>SDA
- pin 5: GPIO3 ==>SCL
- pin 6: GROUND (for the 5V dust sensor)
- pin 9: GROUND (for the 3.3V sensors)

This [diagram](http://132.206.126.37/bvllab/particulate-sensor/blob/master/DOCS/Photos/RPi4GPIO.jpg) shows the function of each pin on the Raspberry Pi 4.

