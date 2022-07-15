pi-display is a python script to diplay data on a waveshare e-ink display that is connected to a raspberry pi zero. The data includes weather, time, crypto and temperature data from a dht22 sensor.

# Installation
* install all needed python3 libraries that are listed in the waveshare documentation: https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT#Install_libraries 
* enable SPI on the pi through *raspi-config*
* copy the correct display size and type module to the waveshare/ dir. For example if you are using a 4.2 inch display you need to copy the corresponding waveshare python library in *e-Paper/RaspberryPi_JetsonNano/python/lib/epd4in2.py* to the waveshare/ dir and change the main.py accordingly.
