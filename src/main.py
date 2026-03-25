import cv2 as cv
from config import CAMERA_ID, WINDOW_WIDTH, WINDOW_HEIGHT, KEYBOARD_LAYOUT, DEBOUNCE_DELAY
from gesture import is_clicking, get_click_position, get_fingers_up
from hand_tracking import (
    init_detector,
    find_hands,
    get_landmark_positions,
    draw_landmarks,
    get_fingertip_positions,
)
from keyboard_ui import generate_key_positions, draw_keyboard, get_hovered_key
from input_handler import init_keyboard_controller, press_character, press_special_key
import time

def main():
    cap = cv.VideoCapture(CAMERA_ID)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)

    detector = init_detector()

    # Generate key positions ONCE at start (not every frame)
    keys = generate_key_positions(KEYBOARD_LAYOUT)
    keyboard = init_keyboard_controller()
    last_press_time = 0
    pressed_key = None
    pressed_key_time = 0
    press_feedback_duration = 0.15
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv.flip(frame, 1)  # Mirror the frame

        # Track hovered key (None if no hand or not hovering)
        hovered_key = None

        hand_landmarks_list = find_hands(frame, detector)
        if hand_landmarks_list:
            for hand_landmarks in hand_landmarks_list:
                # Draw hand skeleton
                draw_landmarks(frame, hand_landmarks, frame.shape)

                # Get positions
                landmark_positions = get_landmark_positions(hand_landmarks, frame.shape)
                fingertip_positions = get_fingertip_positions(hand_landmarks, frame.shape)

                # Check which fingers are up
                fingers_up = get_fingers_up(landmark_positions)
                finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]

                # Display fingers status
                fingers_text = "Fingers: "
                for i, (name, is_up) in enumerate(zip(finger_names, fingers_up)):
                    if is_up:
                        fingers_text += f"{name} "
                cv.putText(frame, fingers_text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                # Get index finger position for hover detection
                index_pos = fingertip_positions["Index"]

                # Check if index finger is hovering over any key
                hovered_key = get_hovered_key(index_pos, keys)

                # Display hovered key
                if hovered_key:
                    cv.putText(frame, f"Hover: {hovered_key['char']}", (10, 60),
                               cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                # Check for click gesture AND hovering over a key
                if is_clicking(fingertip_positions) and hovered_key:
                    current_time = time.time()

                    # Debounce check - only press if enough time has passed
                    if current_time - last_press_time > DEBOUNCE_DELAY:
                        # Press the key
                        press_character(keyboard, hovered_key["char"].lower())

                        # Update tracking variables
                        last_press_time = current_time
                        pressed_key = hovered_key
                        pressed_key_time = current_time

                        # Visual feedback
                        click_pos = get_click_position(fingertip_positions)
                        if click_pos:
                            cv.circle(frame, click_pos, 15, (0, 255, 0), -1)

                # Draw purple circle on index fingertip
                cv.circle(frame, index_pos, 10, (255, 0, 255), 2)

        # Display pressed key feedback
        if pressed_key:
            cv.putText(frame, f"Pressed: {pressed_key['char']}", (10, 90),
                       cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Clear pressed_key feedback after duration
        if pressed_key and time.time() - pressed_key_time > press_feedback_duration:
            pressed_key = None

        # Draw keyboard EVERY frame (with hover and press highlight)
        draw_keyboard(frame, keys, hovered_key, pressed_key)

        cv.imshow("Virtual Keyboard", frame)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()
    
 
if __name__ == "__main__":
    main()
