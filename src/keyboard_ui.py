# keyboard_ui.py
import cv2
from config import (
    KEYBOARD_ROWS, KEY_UNIT, KEY_HEIGHT, KEY_GAP,
    KEYBOARD_START_X, KEYBOARD_START_Y, KEY_ALPHA,
    COLOR_KEY_DEFAULT, COLOR_KEY_HOVER, COLOR_KEY_PRESS,
    COLOR_KEY_SPECIAL, COLOR_KEY_ACTIVE, COLOR_TEXT, COLOR_BORDER,
    TEXT_BOX_HEIGHT, TEXT_BOX_COLOR,
)

_SPECIAL = {'BACK','TAB','CAPS','ENTER','SHIFT','SPACE','\\','CLEAR'}
_SMALL   = {'BACK','TAB','CAPS','ENTER','SHIFT','SPACE','CLEAR'}

def _row_px(row):
    return sum(int(u*KEY_UNIT) for _,u in row) + KEY_GAP*(len(row)-1)

def generate_key_positions():
    keys  = []
    y     = KEYBOARD_START_Y
    full_w = _row_px(KEYBOARD_ROWS[0])

    for row in KEYBOARD_ROWS:
        # Bottom row: SPACE centered + CLEAR to the right
        if len(row) == 1 and row[0][0] == 'SPACE':
            space_w = int(row[0][1] * KEY_UNIT)
            clear_w = int(2 * KEY_UNIT)
            # Centre SPACE under the full keyboard width
            space_x = KEYBOARD_START_X + (full_w - space_w) // 2
            keys.append({'char':'SPACE','x':space_x,'y':y,'w':space_w,'h':KEY_HEIGHT})
            # CLEAR sits right after SPACE with a gap
            clear_x = space_x + space_w + KEY_GAP
            keys.append({'char':'CLEAR','x':clear_x,'y':y,'w':clear_w,'h':KEY_HEIGHT})
            y += KEY_HEIGHT + KEY_GAP
            continue

        x = KEYBOARD_START_X
        for label, units in row:
            w = int(units * KEY_UNIT)
            keys.append({'char':label,'x':x,'y':y,'w':w,'h':KEY_HEIGHT})
            x += w + KEY_GAP
        y += KEY_HEIGHT + KEY_GAP

    return keys

def _kb_bottom(keys):
    return max(k['y']+k['h'] for k in keys)

def _key_color(key, hover_key, pressed_key, shift_on, caps_on):
    c = key['char']
    if pressed_key and c == pressed_key['char']:          return COLOR_KEY_PRESS
    if (c=='SHIFT' and shift_on) or (c=='CAPS' and caps_on): return COLOR_KEY_ACTIVE
    if hover_key   and c == hover_key['char']:            return COLOR_KEY_HOVER
    if c in _SPECIAL:                                     return COLOR_KEY_SPECIAL
    return COLOR_KEY_DEFAULT

def _draw_key(overlay, key, color):
    x,y,w,h = key['x'],key['y'],key['w'],key['h']
    label   = key['char']
    cv2.rectangle(overlay,(x,y),(x+w,y+h),color,cv2.FILLED)
    cv2.rectangle(overlay,(x,y),(x+w,y+h),COLOR_BORDER,1)
    font  = cv2.FONT_HERSHEY_SIMPLEX
    fs    = 0.46 if label in _SMALL else 0.70
    thick = 1    if label in _SMALL else 2
    tw,th = cv2.getTextSize(label,font,fs,thick)[0]
    cv2.putText(overlay, label,
                (x+(w-tw)//2, y+(h+th)//2),
                font, fs, COLOR_TEXT, thick, cv2.LINE_AA)

def draw_keyboard(frame, keys, hover_key=None, pressed_key=None,
                  shift_on=False, caps_on=False):
    overlay = frame.copy()
    for k in keys:
        _draw_key(overlay, k, _key_color(k, hover_key, pressed_key, shift_on, caps_on))
    cv2.addWeighted(overlay, KEY_ALPHA, frame, 1-KEY_ALPHA, 0, frame)

def draw_text_display(frame, text, keys):
    full_w = _row_px(KEYBOARD_ROWS[0])
    x1 = KEYBOARD_START_X
    x2 = x1 + full_w
    y1 = _kb_bottom(keys) + KEY_GAP * 2
    y2 = y1 + TEXT_BOX_HEIGHT

    ov = frame.copy()
    cv2.rectangle(ov,(x1,y1),(x2,y2),TEXT_BOX_COLOR,cv2.FILLED)
    cv2.rectangle(ov,(x1,y1),(x2,y2),COLOR_BORDER,1)
    cv2.addWeighted(ov, 0.75, frame, 0.25, 0, frame)

    display = text.replace('\n','↵ ')[-80:]
    cv2.putText(frame, display, (x1+10, y2-9),
                cv2.FONT_HERSHEY_SIMPLEX, 0.60, COLOR_TEXT, 2, cv2.LINE_AA)

def point_in_key(pt, key):
    px,py = pt
    return key['x']<=px<=key['x']+key['w'] and key['y']<=py<=key['y']+key['h']

def get_hovered_key(point, keys):
    for k in keys:
        if point_in_key(point, k): return k
    return None