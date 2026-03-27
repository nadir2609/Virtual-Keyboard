# main.py
import cv2 as cv
import time
from config import CAMERA_ID, WINDOW_WIDTH, WINDOW_HEIGHT, CLICK_THRESHOLD, DEBOUNCE_DELAY
from gesture import is_clicking, get_click_position, get_fingers_up
from hand_tracking import (init_detector, find_hands, get_landmark_positions,
                            draw_landmarks, get_fingertip_positions)
from keyboard_ui import (generate_key_positions, draw_keyboard,
                          get_hovered_key, draw_text_display)
from input_handler import init_keyboard_controller, handle_key_press, is_special_key

PRESS_FEEDBACK = 0.15
SMOOTH = 0.35  # smoothing factor: 0.0 = max smooth, 1.0 = no smooth

def smooth_landmarks(prev, curr, factor):
    """Blend previous and current landmark positions to reduce jitter."""
    if prev is None:
        return curr
    return [
        (int(prev[i][0] * (1 - factor) + curr[i][0] * factor),
         int(prev[i][1] * (1 - factor) + curr[i][1] * factor))
        for i in range(len(curr))
    ]

def main():
    cap = cv.VideoCapture(CAMERA_ID)
    cap.set(cv.CAP_PROP_FRAME_WIDTH,  WINDOW_WIDTH)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)

    detector = init_detector()
    keys     = generate_key_positions()
    keyboard = init_keyboard_controller()

    typed_text   = ''
    caps_on      = False
    shift_on     = False
    pressed_key  = None
    pressed_time = 0.0

    was_pinching  = False
    can_press     = True
    prev_lm_pos   = None   # smoothed landmark positions from last frame

    cv.namedWindow("Virtual Keyboard", cv.WINDOW_NORMAL)
    cv.setWindowProperty("Virtual Keyboard", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv.flip(frame, 1)
        hovered_key = None

        landmarks_list = find_hands(frame, detector)
        if landmarks_list:
            for lm in landmarks_list:
                # Raw positions this frame
                raw_lm_pos = get_landmark_positions(lm, frame.shape)

                # Smooth all 21 points against previous frame
                smooth_lm_pos = smooth_landmarks(prev_lm_pos, raw_lm_pos, SMOOTH)
                prev_lm_pos   = smooth_lm_pos

                # Build smoothed fingertip dict from smoothed positions
                ft_pos = {
                    "Thumb":  smooth_lm_pos[4],
                    "Index":  smooth_lm_pos[8],
                    "Middle": smooth_lm_pos[12],
                    "Ring":   smooth_lm_pos[16],
                    "Pinky":  smooth_lm_pos[20],
                }

                # Draw skeleton using smoothed points
                draw_landmarks(frame, smooth_lm_pos, frame.shape)

                index_pos   = ft_pos['Index']
                hovered_key = get_hovered_key(index_pos, keys)

                pinching = is_clicking(ft_pos, threshold=CLICK_THRESHOLD)

                if was_pinching and not pinching:
                    can_press = True

                if pinching and can_press and hovered_key:
                    typed_text, caps_on, shift_on = handle_key_press(
                        keyboard, hovered_key['char'],
                        typed_text, caps_on, shift_on)
                    pressed_key  = hovered_key
                    pressed_time = time.time()
                    can_press    = False

                    cp = get_click_position(ft_pos)
                    if cp:
                        cv.circle(frame, cp, 12, (0,255,0), -1)
                        cv.circle(frame, cp, 12, (255,255,255), 2)

                was_pinching = pinching

                cv.circle(frame, index_pos, 8, (255,0,255), -1)
                cv.circle(frame, index_pos, 8, (255,255,255),  2)

        else:
            # Hand left frame — reset smoothing
            prev_lm_pos = None

        if pressed_key and time.time() - pressed_time > PRESS_FEEDBACK:
            pressed_key = None

        draw_keyboard(frame, keys, hovered_key, pressed_key, shift_on, caps_on)
        draw_text_display(frame, typed_text, keys)

        hy = frame.shape[0] - 10
        if caps_on:
            cv.putText(frame,'CAPS',(10,hy),cv.FONT_HERSHEY_SIMPLEX,0.55,(0,200,255),2)
        if shift_on:
            cv.putText(frame,'SHIFT',(80 if caps_on else 10, hy),
                       cv.FONT_HERSHEY_SIMPLEX,0.55,(255,160,0),2)

        cv.imshow("Virtual Keyboard", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()