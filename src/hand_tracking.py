import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os

from config import MAX_HANDS, DETECTION_CONFIDENCE, TRACKING_CONFIDENCE

# Path to the model file
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'hand_landmarker.task')

# Hand connections for drawing
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),      # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),      # Index
    (0, 9), (9, 10), (10, 11), (11, 12), # Middle
    (0, 13), (13, 14), (14, 15), (15, 16), # Ring
    (0, 17), (17, 18), (18, 19), (19, 20), # Pinky
    (5, 9), (9, 13), (13, 17)            # Palm
]


def init_detector():
    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=MAX_HANDS,
        min_hand_detection_confidence=DETECTION_CONFIDENCE,
        min_tracking_confidence=TRACKING_CONFIDENCE
    )
    detector = vision.HandLandmarker.create_from_options(options)
    return detector


def find_hands(frame, detector):
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
    results = detector.detect(mp_image)
    return results.hand_landmarks


def draw_landmarks(frame, hand_landmarks, frame_shape):
    h, w = frame_shape[:2]

    # Convert normalized landmarks to pixel coordinates
    points = []
    for landmark in hand_landmarks:
        x = int(landmark.x * w)
        y = int(landmark.y * h)
        points.append((x, y))

    # Draw connections
    for connection in HAND_CONNECTIONS:
        start_idx, end_idx = connection
        start_point = points[start_idx]
        end_point = points[end_idx]
        cv.line(frame, start_point, end_point, (0, 255, 0), 2)

    # Draw landmark points
    for i, point in enumerate(points):
        # Fingertips (4, 8, 12, 16, 20) in red, others in blue
        if i in [4, 8, 12, 16, 20]:
            cv.circle(frame, point, 8, (0, 0, 255), -1)
        else:
            cv.circle(frame, point, 5, (255, 0, 0), -1)


def get_landmark_positions(hand_landmarks, frame_shape):
    h, w = frame_shape[:2]
    landmark_positions = []
    for landmark in hand_landmarks:
        x = int(landmark.x * w)
        y = int(landmark.y * h)
        landmark_positions.append((x, y))
    return landmark_positions
