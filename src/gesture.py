def calculate_distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


def is_clicking(fingertip_positions, threshold=40):
    if "Index" in fingertip_positions and "Thumb" in fingertip_positions:
        index_pos = fingertip_positions["Index"]
        thumb_pos = fingertip_positions["Thumb"]
        distance = calculate_distance(index_pos, thumb_pos)
        return distance < threshold
    return False


def get_click_position(fingertip_positions):
    if "Index" in fingertip_positions and "Thumb" in fingertip_positions:
        index_pos = fingertip_positions["Index"]
        thumb_pos = fingertip_positions["Thumb"]
        click_x = (index_pos[0] + thumb_pos[0]) // 2
        click_y = (index_pos[1] + thumb_pos[1]) // 2
        return (click_x, click_y)
    return None

def get_fingers_up(landmark_positions):

    fingers = []

    if landmark_positions[4][0] < landmark_positions[3][0]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Pinky: tip=20, PIP=18
    tip_ids = [8, 12, 16, 20]
    pip_ids = [6, 10, 14, 18]

    for tip, pip in zip(tip_ids, pip_ids):
        # Y is inverted in image coordinates (smaller Y = higher on screen)
        if landmark_positions[tip][1] < landmark_positions[pip][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers