import cv2 as cv
from config import CAMERA_ID, WINDOW_WIDTH, WINDOW_HEIGHT
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
                draw_landmarks(frame, hand_landmarks, frame.shape)
                landmark_positions = get_landmark_positions(hand_landmarks, frame.shape)
        cv.imshow("Virtual Keyboard", frame)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
