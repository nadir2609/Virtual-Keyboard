# hand_tracking.py
import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
from config import MAX_HANDS, DETECTION_CONFIDENCE, TRACKING_CONFIDENCE

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'hand_landmarker.task')

HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (0,9),(9,10),(10,11),(11,12),
    (0,13),(13,14),(14,15),(15,16),
    (0,17),(17,18),(18,19),(19,20),
    (5,9),(9,13),(13,17)
]

def init_detector():
    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=MAX_HANDS,
        min_hand_detection_confidence=DETECTION_CONFIDENCE,
        min_tracking_confidence=TRACKING_CONFIDENCE
    )
    return vision.HandLandmarker.create_from_options(options)

def find_hands(frame, detector):
    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    return detector.detect(mp_image).hand_landmarks

def draw_landmarks(frame, points, frame_shape=None):
    """
    Draw hand skeleton.
    points: list of 21 (x, y) tuples — already smoothed pixel coords.
    frame_shape is kept for API compatibility but not used.
    """
    for s, e in HAND_CONNECTIONS:
        cv.line(frame, points[s], points[e], (0,255,0), 2)
    for i, p in enumerate(points):
        if i in [4,8,12,16,20]:
            cv.circle(frame, p, 8, (0,0,255), -1)   # fingertips — red
        else:
            cv.circle(frame, p, 5, (255,0,0), -1)   # joints — blue

def get_landmark_positions(hand_landmarks, frame_shape):
    h, w = frame_shape[:2]
    return [(int(lm.x*w), int(lm.y*h)) for lm in hand_landmarks]

def get_fingertip_positions(hand_landmarks, frame_shape):
    lp = get_landmark_positions(hand_landmarks, frame_shape)
    return {"Thumb":lp[4],"Index":lp[8],"Middle":lp[12],"Ring":lp[16],"Pinky":lp[20]}