# PiPicoUSBSegaController
This is a very simple project to take a Raspbery Pi Pico and turn it USB joystick adapter for a 3 or 6 Button Sega Genesis/Megadrive Controller with supporting Circuit Python code.

Please note that the code requires the following libraries in addition to the base CircuitPython Install 
* [Adafruit_CircuitPython_HID](https://github.com/adafruit/Adafruit_CircuitPython_HID)

### Hardware

This setup is fairly minimal.

A Raspberry Pi Pico https://www.raspberrypi.org/products/raspberry-pi-pico/
and some dupont cables that can provide pins that connect to a 2x5 connector of a DB9 RS232 to 10 pin Ribbon Cable Connector Adapter similar to that below

![image](https://user-images.githubusercontent.com/36720937/155993479-3043488f-428e-476c-a7a2-64751add007f.png)

For my case the follow is the pinout used

|Pico Pin | Pico Signal | 2x5 / DB9 Pin | Sega Signal  | Wire Colour |
|---------|-------------|---------------|--------------|-------------|
| 40      | VBUS        | 5             | +5V          | Red         |
| 38      | GND         | 5             | GND          | Black       |
| 34      | GP28        | 7             | Select       | Brown       |
| 32      | GP27        | 1             | Up / Z       | Orange      |
| 31      | GP26        | 2             | Down / Y     | Yellow      |
| 29      | GP22        | 3             | Left / X     | Green       |
| 27      | GP21        | 4             | Right / Mode | Blue        |
| 26      | GP20        | 6             | B / A        | Purple      |
| 25      | GP19        | 9             | C / Start    | Grey        |

### Theory of Operation
The Raspberry Pi Pico needs to have boot.py configured to create the custom USB HID Gamepad descriptor.  It needs to be done here as by the time code.py begins, the USB interface is set to go
The main code initialises the HID device and starts the main loop:
* Toggle the select line to step through the various gamepad states that give button state information (additionally we can detect if a Sega gamepad is detected and if it is a 3 or 6 button variant)
* Based on the read states, send HID updates to the host 

### References
* Circuit Python USB Gamepad concept - https://signal11.wordpress.com/tag/flight-simulation/
* Sega Controller State Machine - https://www.raspberryfield.life/2019/03/25/sega-mega-drive-genesis-6-button-xyz-controller/
* HID Descriptor for 8 Buttons and Dpad from an arduino pro micro version of this - https://github.com/thinghacker/DualUSBSegaController/blob/master/examples/DualUSBSegaController/DualUSBSegaController.ino
