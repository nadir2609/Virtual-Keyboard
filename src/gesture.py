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
