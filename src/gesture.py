# gesture.py
def calculate_distance(point1, point2):
    return ((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2) ** 0.5

def is_clicking(fingertip_positions, threshold=35):
    if "Index" in fingertip_positions and "Thumb" in fingertip_positions:
        return calculate_distance(
            fingertip_positions["Index"],
            fingertip_positions["Thumb"]
        ) < threshold
    return False

def get_click_position(fingertip_positions):
    if "Index" in fingertip_positions and "Thumb" in fingertip_positions:
        ix, iy = fingertip_positions["Index"]
        tx, ty = fingertip_positions["Thumb"]
        return ((ix+tx)//2, (iy+ty)//2)
    return None

def get_fingers_up(landmark_positions):
    fingers = []
    # Thumb: compare x
    fingers.append(1 if landmark_positions[4][0] < landmark_positions[3][0] else 0)
    # Other 4 fingers: compare y (smaller y = higher on screen = up)
    for tip, pip in zip([8,12,16,20], [6,10,14,18]):
        fingers.append(1 if landmark_positions[tip][1] < landmark_positions[pip][1] else 0)
    return fingers