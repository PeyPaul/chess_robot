import math

def find_circle_intersections(L1, x2, y2, L2):
    # Step 1: Calculate the distance between the centers of the circles
    d = math.sqrt((x2)**2 + (y2)**2)
    
    # Step 2: Check if the circles intersect
    if d > (L1 + L2) or d < abs(L1 - L2) or d == 0:
        return "No intersection"
    
    # Step 3: Calculate the distance from the first circle's center to the line of intersection
    a = (L1**2 - L2**2 + d**2) / (2 * d)
    h = math.sqrt(L1**2 - a**2)
    
    # Step 4: Find the point P2, the point where the line through the intersection points intersects the line between the two centers
    x0 =  a * (x2) / d
    y0 =  a * (y2) / d
    
    # Step 5: Find the intersection points
    rx = -(y2) * (h / d)
    ry = (x2) * (h / d)
    
    # The intersection points are:
    intersection1 = (x0 + rx, y0 + ry)
    intersection2 = (x0 - rx, y0 - ry)

    print("Intersection points:", intersection1, intersection2)
    
    return intersection1, intersection2

def highest_y_intersection(L1, x2, y2, L2):
    result = find_circle_intersections(L1, x2, y2, L2)
    if result == "No intersection":
        return result
    p1, p2 = result
    return p1 if p1[1] > p2[1] else p2

def jonas_inverse_kinematics(L1, L2, x2, y2):
    intersections = highest_y_intersection(L1, x2, y2, L2)
    angle_from_origin = math.degrees(math.atan2(intersections[1], intersections[0]))
    angle_from_center2 = 180 - math.degrees(math.atan2(intersections[1] - y2, intersections[0] - x2))
    return angle_from_origin, angle_from_center2



# teta1, teta2 = jonas_inverse_kinematics(490,475,400,400)

# print(teta1, teta2)
