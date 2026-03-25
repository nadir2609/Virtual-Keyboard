import cv2
from config import COLOR_KEY_DEFAULT, COLOR_KEY_HOVER, COLOR_KEY_PRESS


def generate_key_positions(layout):
    key_width = 60
    key_height = 60
    gap = 5
    start_x = 50
    start_y = 100

    keys = []

    for row_index, row in enumerate(layout):
        y = start_y + row_index * (key_height + gap)

        # Add row offset for staggered keyboard look
        row_offset = row_index * 15

        for char_index, char in enumerate(row):
            x = start_x + row_offset + char_index * (key_width + gap)

            keys.append({
                "char": char,
                "x": x,
                "y": y,
                "w": key_width,
                "h": key_height
            })

    return keys


def draw_single_key(frame, key_data, color):
    x = key_data["x"]
    y = key_data["y"]
    w = key_data["w"]
    h = key_data["h"]
    char = key_data["char"]

    # Draw filled rectangle for key background
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, cv2.FILLED)

    # Draw key border
    cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 50), 2)

    # Draw character centered in the key
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    text_size = cv2.getTextSize(char, font, font_scale, 2)[0]
    text_x = x + (w - text_size[0]) // 2
    text_y = y + (h + text_size[1]) // 2

    cv2.putText(frame, char, (text_x, text_y), font, font_scale, (255, 255, 255), 2)


def draw_keyboard(frame, keys, hover_key=None, pressed_key=None):
    for key in keys:
        # Prioritize pressed key color, then hover color, then default
        if pressed_key and key["char"] == pressed_key["char"]:
            draw_single_key(frame, key, COLOR_KEY_PRESS)
        elif hover_key and key["char"] == hover_key["char"]:
            draw_single_key(frame, key, COLOR_KEY_HOVER)
        else:
            draw_single_key(frame, key, COLOR_KEY_DEFAULT)


def point_in_key(point, key_data):
    px, py = point
    kx = key_data["x"]
    ky = key_data["y"]
    kw = key_data["w"]
    kh = key_data["h"]

    if kx <= px <= kx + kw and ky <= py <= ky + kh:
        return True
    return False


def get_hovered_key(point, keys):
    # This function will use point_in_key to find which key (if any) the point is currently over
    
    for key in keys:
        if point_in_key(point, key):
            return key
    return None


