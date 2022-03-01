import usb_hid
import board
import digitalio
import storage

# This is only one example of a gamepad descriptor, and may not suit your needs.
GAMEPAD_REPORT_DESCRIPTOR = bytes((
    # Joystick
    0x05, 0x01,               # USAGE_PAGE (Generic Desktop)
    0x09, 0x04,               # USAGE (Joystick)
    0xa1, 0x01,               # COLLECTION (Application)
    0x85, 0x04,               # REPORT_ID 04
    # 8 Buttons
    0x05, 0x09,               #   USAGE_PAGE (Button)
    0x19, 0x01,               #   USAGE_MINIMUM (Button 1)
    0x29, 0x08,               #   USAGE_MAXIMUM (Button 8)
    0x15, 0x00,               #   LOGICAL_MINIMUM (0)
    0x25, 0x01,               #   LOGICAL_MAXIMUM (1)
    0x75, 0x01,               #   REPORT_SIZE (1)
    0x95, 0x08,               #   REPORT_COUNT (8)
    0x81, 0x02,               #   INPUT (Data,Var,Abs)
    # X and Y Axis
    0x05, 0x01,               #   USAGE_PAGE (Generic Desktop)
    0x09, 0x01,               #   USAGE (Pointer)
    0xA1, 0x00,               #   COLLECTION (Physical)
    0x09, 0x30,               #     USAGE (x)
    0x09, 0x31,               #     USAGE (y)
    0x15, 0x00,               #     LOGICAL_MINIMUM (0)
    0x26, 0xff, 0x00,         #     LOGICAL_MAXIMUM (255)
    0x75, 0x08,               #     REPORT_SIZE (8)
    0x95, 0x02,               #     REPORT_COUNT (2)
    0x81, 0x02,               #     INPUT (Data,Var,Abs)
    0xc0,                     #   END_COLLECTION
    0xc0                      # END_COLLECTION
))

gamepad = usb_hid.Device(
    report_descriptor=GAMEPAD_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x04,                # Joystick
    report_ids=(4,),           # Descriptor uses report ID 4.
    in_report_lengths=(3,),    # This gamepad sends 3 bytes in its report.
    out_report_lengths=(0,),   # It does not receive any reports.
)

# if Sega Controller C button is held down during boot (controller_c_start.value == False) then do not disable the USB drive mode

controller_c_start = digitalio.DigitalInOut(board.GP19)
controller_c_start.direction = digitalio.Direction.INPUT
controller_c_start.pull = digitalio.Pull.UP

if (controller_c_start.value):
    storage.disable_usb_drive()

usb_hid.enable(
    (usb_hid.Device.KEYBOARD,
     usb_hid.Device.MOUSE,
     usb_hid.Device.CONSUMER_CONTROL,
     gamepad)
)
