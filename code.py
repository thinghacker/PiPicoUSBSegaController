# code.py for PiPicoUSBSegaController - https://github.com/thinghacker/PiPicoUSBSegaController
#
# This is a very simple project to take a Raspbery Pi Pico and turn it USB joystick adapter for a 3 or 6 Button Sega Genesis/Megadrive Controller using CircuitPython.
#
# References used while developing this:
#  Circuit Python USB Gamepad concept - https://signal11.wordpress.com/tag/flight-simulation/
#  Sega Controller State Machine - https://www.raspberryfield.life/2019/03/25/sega-mega-drive-genesis-6-button-xyz-controller/
#  HID Descriptor for 8 Buttons and Dpad from an arduino pro micro version of this - https://github.com/thinghacker/DualUSBSegaController/blob/master/examples/DualUSBSegaController/DualUSBSegaController.ino
#
# Wiring Details (Uses a 2x5 connector that connects to 10 pin Ribbon Cable Connector Adapter that presents a DB9 male connector
#
#|Pico Pin | Pico Signal | 2x5 / DB9 Pin | Sega Signal  | Wire Colour |
#|---------|-------------|---------------|--------------|-------------|
#| 40      | VBUS        | 5             | +5V          | Red         |
#| 38      | GND         | 5             | GND          | Black       |
#| 34      | GP28        | 7             | Select       | Brown       |
#| 32      | GP27        | 1             | Up / Z       | Orange      |
#| 31      | GP26        | 2             | Down / Y     | Yellow      |
#| 29      | GP22        | 3             | Left / X     | Green       |
#| 27      | GP21        | 4             | Right / Mode | Blue        |
#| 26      | GP20        | 6             | B / A        | Purple      |
#| 25      | GP19        | 9             | C / Start    | Grey        |

import board
import digitalio
import time
import usb_hid
from adafruit_hid import find_device

controllerpins_in = {
    "up_z": digitalio.DigitalInOut(board.GP27),
    "down_y": digitalio.DigitalInOut(board.GP26),
    "left_x": digitalio.DigitalInOut(board.GP22),
    "right_mode": digitalio.DigitalInOut(board.GP21),
    "a_b": digitalio.DigitalInOut(board.GP20),
    "c_start": digitalio.DigitalInOut(board.GP19),
}

controllerpins_out = {"select": digitalio.DigitalInOut(board.GP28)}


# set the state for the input pins and enable built in pullups
for pin, pinio in controllerpins_in.items():
    pinio.direction = digitalio.Direction.INPUT
    pinio.pull = digitalio.Pull.UP

# set the state for the ouput pins and set the initial state
for pin, pinio in controllerpins_out.items():
    pinio.direction = digitalio.Direction.OUTPUT
    pinio.value = True

class Stick:
    """Stick
    Used to reference the USB HID joystick defined in boot.py and for sending USB reports
    """
    def __init__(self, devices):
        # Find the stick we defined in boot.py
        self._stick_device = find_device(devices, usage_page=0x1, usage=0x04)
        self._report = bytearray(3)
       
    def update(self, a,b,c,x,y,z,start,mode,l,r,u,d):
        """update
        passed the Sega Genesis/Megadrive Controller State for transmission to the USB Host
        returns nothing
        """
        # The first byte contains the 8 button states (1 = pressed, 0 = released)
        self._report[0] = int(f"{mode:1n}{start:1n}{z:1n}{y:1n}{x:1n}{c:1n}{b:1n}{a:1n}" ,2)
        # The second byte contains the x-axis (0 = left, 127 = centre, 255 = right)
        self._report[1] = 127
        if int(l) == True:
          self._report[1] = 0
        if int(r) == True:
          self._report[1] = 255
        # The third byte contains the y-axis (0 = left, 127 = centre, 255 = right)
        self._report[2] = 127
        if int(u) == True:
          self._report[2] = 0
        if int(d) == True:
          self._report[2] = 255
        # Transmit the USB update
        self._stick_device.send_report(self._report)

def sega():
    """sega
    Read the Sega Genesis/Megadrive Controller State and send USB Updates
    returns nothing
    """
    oldstring = None
    while 1:
        controller = "-"
        button_up = False
        button_down = False
        button_left = False
        button_right = False
        button_a = False
        button_b = False
        button_c = False
        button_x = False
        button_y = False
        button_z = False
        button_start = False
        button_mode = False

        # A detailed description of the controller states are described in https://www.raspberryfield.life/2019/03/25/sega-mega-drive-genesis-6-button-xyz-controller/
        # Start State 0
        controllerpins_out["select"].value = False
        # Start State 1
        controllerpins_out["select"].value = True
        # Start State 2
        controllerpins_out["select"].value = False
        # If both left_x and right_mode are LOW then we have a 3 Button Controller
        if (
            controllerpins_in["left_x"].value == False
            and controllerpins_in["right_mode"].value == False
        ):
            controller = 3
        if controllerpins_in["a_b"].value == False:
            button_a = True
        if controllerpins_in["c_start"].value == False:
            button_start = True
        # Start State 3
        controllerpins_out["select"].value = True
        if controllerpins_in["up_z"].value == False:
            button_up = True
        if controllerpins_in["down_y"].value == False:
            button_down = True
        if controllerpins_in["left_x"].value == False:
            button_left = True
        if controllerpins_in["right_mode"].value == False:
            button_right = True
        if controllerpins_in["a_b"].value == False:
            button_b = True
        if controllerpins_in["c_start"].value == False:
            button_c = True
        # Start State 4
        controllerpins_out["select"].value = False
        # If both up_z and down_y are LOW then we have a 6 Button Controller
        if (
            controllerpins_in["up_z"].value == False
            and controllerpins_in["down_y"].value == False
        ):
            controller = 6
            # Start State 5 (if controller == 6)
            controllerpins_out["select"].value = True
            time.sleep(0.001)            
            if controllerpins_in["right_mode"].value == False:
                button_mode = True
            if controllerpins_in["up_z"].value == False:
                button_z = True
            if controllerpins_in["down_y"].value == False:
                button_y = True
            if controllerpins_in["left_x"].value == False:
                button_x = True
            # Start State 6 (if controller == 6)
            controllerpins_out["select"].value = False
            time.sleep(0.001)            
            # Start State 7 (if controller == 6)
            time.sleep(0.001)            
            controllerpins_out["select"].value = True

        newstring = f"{controller}{button_up:1n}{button_down:1n}{button_left:1n}{button_right:1n}{button_start:1n}{button_a:1n}{button_b:1n}{button_c:1n}{button_x:1n}{button_y:1n}{button_z:1n}{button_mode:1n}"
        # Only update if something has changed since last time
        if newstring != oldstring:
            # the following two lines is to help with debugging        
            # print("TUDLRSABCXYZM")
            # print(newstring)
            st.update(button_a,button_b,button_c,button_x,button_y,button_z,button_start,button_mode,button_left,button_right,button_up,button_down)            
            oldstring = newstring
        # adding a delay for allowing the controller to reset after state reading    
        time.sleep(0.03)


if __name__ == "__main__":
    time.sleep(1)
    try:
        st=Stick(usb_hid.devices)
    except:
        print("Problem with usb_hid.devices")
    sega()