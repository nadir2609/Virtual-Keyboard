# input_handler.py
from pynput.keyboard import Controller, Key

_SPECIAL = {'BACK','TAB','CAPS','ENTER','SHIFT','SPACE','CLEAR'}

def init_keyboard_controller():
    return Controller()

def is_special_key(char):
    return char.upper() in _SPECIAL

def handle_key_press(controller, char, typed_text, caps_on, shift_on):
    """
    Handle any key press. Returns (typed_text, caps_on, shift_on).
    SHIFT is one-shot: turns off after one character.
    """
    label = char.upper()

    if label == 'SHIFT':
        return typed_text, caps_on, not shift_on

    if label == 'CAPS':
        return typed_text, not caps_on, shift_on

    if label == 'CLEAR':
        return '', caps_on, shift_on

    if label == 'BACK':
        controller.tap(Key.backspace)
        return typed_text[:-1], caps_on, shift_on

    if label == 'ENTER':
        controller.tap(Key.enter)
        return typed_text + '\n', caps_on, shift_on

    if label == 'TAB':
        controller.tap(Key.tab)
        return typed_text + '    ', caps_on, shift_on

    if label == 'SPACE':
        controller.tap(Key.space)
        return typed_text + ' ', caps_on, shift_on

    # Regular character — SHIFT XOR CAPS = uppercase
    uppercase = caps_on ^ shift_on
    out = char.upper() if uppercase else char.lower()
    controller.tap(out)
    return typed_text + out, caps_on, False   # shift turns off after 1 char