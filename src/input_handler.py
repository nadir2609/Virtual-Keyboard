from pynput.keyboard import Controller, Key

def init_keyboard_controller():
    return Controller()

def press_character(controller, char):
    controller.tap(char)

def press_special_key(controller, key_name):
    special_keys = {
        "Space": Key.space,
        "Enter": Key.enter,
        "Backspace": Key.backspace,
        "Tab": Key.tab,
        "Shift": Key.shift,
        "Ctrl": Key.ctrl,
        "Alt": Key.alt
    }
    key = special_keys.get(key_name)
    if key:
        controller.tap(key)