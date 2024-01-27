import math

def get_distance_to_frame_subject(bounding_box, aperture, focal_length):
    distance_to_capture_horizontal = calculate_field_of_view_distance(aperture, bounding_box.width, focal_length)
    distance_to_capture_vertical = calculate_field_of_view_distance(aperture, bounding_box.height, focal_length)

    return max(distance_to_capture_horizontal, distance_to_capture_vertical)

def calculate_field_of_view_distance(sensor_size, object_size, focal_length):
    return calculate_camera_distance(object_size, calculate_field_of_view(sensor_size, focal_length))
    
def calculate_field_of_view(sensor_size, focal_length):
    # Focal length and sensor size should be in the same units (e.g., mm)
    field_of_view = 2 * math.atan(sensor_size / (2 * focal_length))
    return field_of_view

def calculate_camera_distance(subject_size, field_of_view):
    # Subject size and field of view should be in the same units (e.g., mm and degrees)
    distance = (subject_size / 2) / math.tan(field_of_view / 2)
    return distance