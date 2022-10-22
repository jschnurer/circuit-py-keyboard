import time
import board
import digitalio
import usb_hid
import sys

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

key_dict = {
    'A': Keycode.A,
    'B': Keycode.B,
    'C': Keycode.C,
    'D': Keycode.D,
    'E': Keycode.E,
    'F': Keycode.F,
    'G': Keycode.G,
    'H': Keycode.H,
    'I': Keycode.I,
    'J': Keycode.J,
    'K': Keycode.K,
    'L': Keycode.L,
    'M': Keycode.M,
    'N': Keycode.N,
    'O': Keycode.O,
    'P': Keycode.P,
    'Q': Keycode.Q,
    'R': Keycode.R,
    'S': Keycode.S,
    'T': Keycode.T,
    'U': Keycode.U,
    'V': Keycode.V,
    'W': Keycode.W,
    'X': Keycode.X,
    'Y': Keycode.Y,
    'Z': Keycode.Z,
    'F1': Keycode.F1,
    'F2': Keycode.F2,
    'F3': Keycode.F3,
    'F4': Keycode.F4,
    'F5': Keycode.F5,
    'F6': Keycode.F6,
    'F7': Keycode.F7,
    'F8': Keycode.F8,
    'F9': Keycode.F9,
    'F10': Keycode.F10,
    'F11': Keycode.F11,
    'F12': Keycode.F12,
    'ONE': Keycode.ONE,
    'TWO': Keycode.TWO,
    'THREE': Keycode.THREE,
    'FOUR': Keycode.FOUR,
    'FIVE': Keycode.FIVE,
    'SIX': Keycode.SIX,
    'SEVEN': Keycode.SEVEN,
    'EIGHT': Keycode.EIGHT,
    'NINE': Keycode.NINE,
    'ZERO': Keycode.ZERO,
    'ENTER': Keycode.ENTER,
    'RETURN': Keycode.RETURN,
    'ESCAPE': Keycode.ESCAPE,
    'BACKSPACE': Keycode.BACKSPACE,
    'TAB': Keycode.TAB,
    'SPACEBAR': Keycode.SPACEBAR,
    'SPACE': Keycode.SPACE,
    'MINUS': Keycode.MINUS,
    'EQUALS': Keycode.EQUALS,
    'LEFT_BRACKET': Keycode.LEFT_BRACKET,
    'RIGHT_BRACKET': Keycode.RIGHT_BRACKET,
    'BACKSLASH': Keycode.BACKSLASH,
    'POUND': Keycode.POUND,
    'SEMICOLON': Keycode.SEMICOLON,
    'QUOTE': Keycode.QUOTE,
    'GRAVE_ACCENT': Keycode.GRAVE_ACCENT,
    'COMMA': Keycode.COMMA,
    'PERIOD': Keycode.PERIOD,
    'FORWARD_SLASH': Keycode.FORWARD_SLASH,
    '_': None
}

pin_dict = {
    '0': board.GP0,
    '1': board.GP1,
    '2': board.GP2,
    '3': board.GP3,
    '4': board.GP4,
    '5': board.GP5,
    '6': board.GP6,
    '7': board.GP7,
    '8': board.GP8,
    '9': board.GP9,
    '10': board.GP10,
    '11': board.GP11,
    '12': board.GP12,
    '13': board.GP13,
    '14': board.GP14,
    '15': board.GP15,
    '16': board.GP16,
    '17': board.GP17,
    '18': board.GP18,
    '19': board.GP19,
    '20': board.GP20,
    '21': board.GP21,
    '22': board.GP22,
}

keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

class ShortcutButton:
    def __init__(self, btn_num, key_text, pin, keycode):
        self.btn_num = btn_num
        self.key_text = key_text
        self.pin = pin
        self.btn = digitalio.DigitalInOut(pin)
        self.btn.direction = digitalio.Direction.INPUT
        self.btn.pull = digitalio.Pull.DOWN
        self.keycode = keycode
        self.is_down = 0

print("Reading file...")
f = open('keys.txt')
keystrings = f.read()
f.close()
keylines = keystrings.split('\n')
curr_config = None
pin_config = None

for line in keylines:
    if len(line) > 0 and line[0] == '!':
        curr_config = line[1:].split(',')
        print('Current config: ' + line[1:])
    elif len(line) > 0 and line[0] == ':':
        pin_config = line[1:].split(',')

sbuttons = []
active_keycodes = []
key_texts = []
active_pins = []

if curr_config is None:
    print("No active profile found in keys.txt!")
    print("Please update keys.txt and restart Pico!")
    sys.exit()

if pin_config is None:
    print("No pin config found in keys.txt! Update it!")

print("Reading pin configuration...")
btnIx = 1
for pin in pin_config:
    if pin in pin_dict:
        active_pins.append(pin_dict[pin])
        print(str(pin_dict[pin]) + " is now bound to button " + str(btnIx))
        btnIx += 1

btnIx = 1
for key in curr_config:
    if key != '!':
        stripped_key = key
        if stripped_key in key_dict:
            active_keycodes.append(key_dict[stripped_key])
            key_texts.append(stripped_key)
            print("button " + str(btnIx) + " = " + stripped_key + " -> " + str(key_dict[stripped_key]))
        else:
            active_keycodes.append(None)
            key_texts.append(None)
            print('No keycode found for ' + stripped_key + " for button " + str(btnIx))
        btnIx += 1

if len(active_keycodes) == 0:
    print("No active profile found in keys.txt!")
    print("Please update keys.txt and restart Pico!")
    sys.exit()

if len(active_keycodes) > 0 and active_keycodes[0] is not None and active_pins[0] is not None:
    sbuttons.append(ShortcutButton(1, key_texts[0], active_pins[0], active_keycodes[0]))
    print("::: Button 1 is now active & bound to " + str(key_texts[0]))

if len(active_keycodes) > 1 and active_keycodes[1] is not None and active_pins[1] is not None:
    sbuttons.append(ShortcutButton(2, key_texts[1], active_pins[1], active_keycodes[1]))
    print("::: Button 2 is now active & bound to " + str(key_texts[1]))

if len(active_keycodes) > 2 and active_keycodes[2] is not None and active_pins[2] is not None:
    sbuttons.append(ShortcutButton(3, key_texts[2], active_pins[2], active_keycodes[2]))
    print("::: Button 3 is now active & bound to " + str(key_texts[2]))

if len(active_keycodes) > 3 and active_keycodes[3] is not None and active_pins[3] is not None:
    sbuttons.append(ShortcutButton(4, key_texts[3], active_pins[3], active_keycodes[3]))
    print("::: Button 4 is now active & bound to " + str(key_texts[3]))

print("Starting button routine...")

while True:
    for sbtn in sbuttons:
        if sbtn.btn.value and sbtn.is_down == 0:
            print("Button " + str(sbtn.btn_num) + " was pressed. Sending " + sbtn.key_text)
            keyboard.press(sbtn.keycode)
            sbtn.is_down = 1
        elif not sbtn.btn.value and sbtn.is_down == 1:
            print("Button " + str(sbtn.btn_num) + " was released.")
            sbtn.is_down = 0
            keyboard.release(sbtn.keycode)
    time.sleep(0.1)