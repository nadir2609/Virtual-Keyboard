import cv2 as cv
from config import CAMERA_ID, WINDOW_WIDTH, WINDOW_HEIGHT
from gesture import is_clicking, get_click_position, get_fingers_up
from hand_tracking import (
    init_detector,
    find_hands,
    get_landmark_positions,
    draw_landmarks,
    get_fingertip_positions,
)


def main():
    cap = cv.VideoCapture(CAMERA_ID)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)

    detector = init_detector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv.flip(frame, 1)  # Mirror the frame

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

                # Check for click gesture
                if is_clicking(fingertip_positions):
                    click_pos = get_click_position(fingertip_positions)
                    if click_pos:
                        # Draw green circle at click position
                        cv.circle(frame, click_pos, 15, (0, 255, 0), -1)
                        cv.putText(frame, "CLICK!", (click_pos[0] + 20, click_pos[1]),
                                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                index_pos = fingertip_positions["Index"]
                cv.circle(frame, index_pos, 10, (255, 0, 255), 2)

        cv.imshow("Virtual Keyboard", frame)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
