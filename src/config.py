# config.py
CAMERA_ID = 0
WINDOW_WIDTH  = 1280
WINDOW_HEIGHT = 720

MAX_HANDS            = 1
DETECTION_CONFIDENCE = 0.8
TRACKING_CONFIDENCE  = 0.8

KEYBOARD_ROWS = [
    [('`',1),('1',1),('2',1),('3',1),('4',1),('5',1),('6',1),
     ('7',1),('8',1),('9',1),('0',1),('-',1),('=',1),('BACK',2)],
    [('TAB',1.5),('Q',1),('W',1),('E',1),('R',1),('T',1),('Y',1),
     ('U',1),('I',1),('O',1),('P',1),('[',1),(']',1),('\\',1.5)],
    [('CAPS',1.75),('A',1),('S',1),('D',1),('F',1),('G',1),('H',1),
     ('J',1),('K',1),('L',1),(';',1),("'",1),('ENTER',2.25)],
    [('SHIFT',2.25),('Z',1),('X',1),('C',1),('V',1),('B',1),('N',1),
     ('M',1),(',',1),('.',1),('/',1),('SHIFT',2.75)],
    [('SPACE',6)],
]

# Keys sized to fit full 1280x720 frame
KEY_UNIT   = 40   # halved from 80
KEY_HEIGHT = 28   # halved from 56
KEY_GAP    = 3

KEYBOARD_START_X = 14   # small left margin so row fills nicely
KEYBOARD_START_Y = 10   # top of screen

KEY_ALPHA = 0.55   # 0=invisible 1=solid

COLOR_KEY_DEFAULT = (50,  50,  50)
COLOR_KEY_HOVER   = (100, 100, 100)
COLOR_KEY_PRESS   = (0,   200,  0)
COLOR_KEY_SPECIAL = (70,  40,  60)
COLOR_KEY_ACTIVE  = (0,   140, 200)   # SHIFT/CAPS when ON
COLOR_TEXT        = (255, 255, 255)
COLOR_BORDER      = (130, 130, 130)

TEXT_BOX_HEIGHT  = 38
TEXT_BOX_COLOR   = (30, 30, 30)

CLICK_THRESHOLD = 35
DEBOUNCE_DELAY  = 0.3