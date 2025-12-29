print("TKeeb is starting...")
import board
import busio
import time
import rtc

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.scanners.digitalio import DigitalIO
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.vial import Vial
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.extensions.peg_oled_display import Oled, OledDisplayMode, OledData

# --- 1. My Keyboard & Matrix Setup ---
keyboard = KMKKeyboard()

# I am defining the Main Matrix (88 Keys)
# Rows: GP0-GP7, Cols: GP8-GP18
matrix_scanner = DiodeOrientation(
    col_pins=(board.GP8, board.GP9, board.GP10, board.GP11, 
              board.GP12, board.GP13, board.GP14, board.GP15, 
              board.GP16, board.GP17, board.GP18),
    row_pins=(board.GP0, board.GP1, board.GP2, board.GP3, 
              board.GP4, board.GP5, board.GP6, board.GP7),
    diode_orientation=DiodeOrientation.COL2ROW
)

# I configured the Encoder Button (GP26) as a Direct Pin here.
# This allows my button to work even though it's not in the main grid.
direct_scanner = DigitalIO(
    pins=(board.GP26,),
    pull_up=True  # Switch connects Pin -> GND
)

# I combine both scanners so the keyboard sees all 89 keys
keyboard.matrix = [matrix_scanner, direct_scanner]

# --- 2. Modules & Extensions ---
keyboard.modules.append(Layers())
keyboard.extensions.append(MediaKeys())

# Vial Integration (For my dynamic remapping)
vial = Vial()
vial.vial_keyboard_uid = bytearray.fromhex("8f2e4a1b-9c3d-4e5f-b6a7-0d9e8c7b6a51")
vial.vial_unlock_combo = (KC.LSHIFT, KC.RSHIFT, KC.UP)
keyboard.modules.append(vial)

# --- 3. Rotary Encoder (Rotation) ---
# My Pins: A=GP21, B=GP22
encoder_handler = EncoderHandler()
encoder_handler.pins = ((board.GP21, board.GP22, None, False),)
# Mapping Rotation: [Layer 0: (Volume Down, Volume Up)]
encoder_handler.map = [ ((KC.VOLD, KC.VOLU),) ]
keyboard.modules.append(encoder_handler)

# --- 4. RGB Lighting (GP27) ---
rgb = RGB(
    pixel_pin=board.GP27,
    num_pixels=88,
    val_limit=150,     # I set a safety brightness limit (0-255)
    hue_default=0,
    sat_default=255,
    val_default=100,
    animation_mode=AnimationModes.BREATHING
)
keyboard.extensions.append(rgb)

# --- 5. OLED Display (Time & Date) ---
# Pins: SCL=GP19, SDA=GP20
# 'adafruit_display_text', 'adafruit_ssd1306', 'adafruit_bus_device' in /lib is needed here.

# Custom Class I wrote to display Time
class TimeDisplay(OledData):
    def __init__(self):
        self._rtc = rtc.RTC()
        # Set Default Time: YYYY, M, D, H, M, S, W, Y, DST
        # Note: Time resets on power loss since I don't have a battery backup yet.
        self._rtc.datetime = time.struct_time((2025, 1, 1, 12, 00, 00, 2, 1, -1))

    def text(self, keyboard):
        t = self._rtc.datetime
        return f"{t.tm_hour:02}:{t.tm_min:02}:{t.tm_sec:02}\n{t.tm_year}-{t.tm_mon:02}-{t.tm_mday:02}"

# Initialize OLED
try:
    oled_ext = Oled(
        OledData(image={0: TimeDisplay()}),
        toDisplay=OledDisplayMode.TXT,
        flip=False,
    )
    # Force I2C pins in case auto-detect fails on my setup
    oled_ext._i2c = busio.I2C(board.GP19, board.GP20)
    keyboard.extensions.append(oled_ext)
except Exception as e:
    print("OLED Error:", e)

# --- 6. Keymap ---
# There are 88 Matrix Keys + 1 Encoder Button so it's 89 items in the map
# Cuz I am using Vial, these are just placeholders. 
# I will use vial.rocks to assign the real keys later.

keyboard.keymap = [
    [
        # --- My 88 Matrix Keys ---
        KC.A, KC.B, KC.C, KC.D, KC.E, KC.F, KC.G, KC.H, KC.I, KC.J, KC.K,
        KC.L, KC.M, KC.N, KC.O, KC.P, KC.Q, KC.R, KC.S, KC.T, KC.U, KC.V,
        KC.W, KC.X, KC.Y, KC.Z, KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6,
        KC.N7, KC.N8, KC.N9, KC.N0, KC.ENT, KC.ESC, KC.BSPC, KC.TAB, KC.SPC, KC.MINS,
        KC.EQL, KC.LBRC, KC.RBRC, KC.BSLS, KC.SCLN, KC.QUOT, KC.GRV, KC.COMM, KC.DOT, KC.SLSH,
        KC.CAPS, KC.F1, KC.F2, KC.F3, KC.F4, KC.F5, KC.F6, KC.F7, KC.F8, KC.F9,
        KC.F10, KC.F11, KC.F12, KC.PSCR, KC.SLCK, KC.PAUS, KC.INS, KC.HOME, KC.PGUP, KC.DEL,
        KC.END, KC.PGDN, KC.RGHT, KC.LEFT, KC.DOWN, KC.UP, KC.NLCK, KC.PSLS, KC.PAST, KC.PMNS,
        KC.PPLS, KC.PENT, KC.PDOT, KC.P0, KC.P1, KC.P2, KC.P3, KC.P4,
        
        # --- My Encoder Switch (Key #89) ---
        KC.MUTE 
    ]
]

if __name__ == '__main__':
    keyboard.go()