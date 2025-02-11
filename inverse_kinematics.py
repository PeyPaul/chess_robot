import math

def inverse_kinematics(x, y, l1, l2):
    """
    Calculate the inverse kinematics for a 2-link robotic arm.

    Parameters:
    x (float): The x-coordinate of the end effector.
    y (float): The y-coordinate of the end effector.
    l1 (float): The length of the first link.
    l2 (float): The length of the second link.

    Returns:
    tuple: The angles (theta1, theta2) in radians.
    """
    # Calculate the distance from the base to the end effector
    r = math.sqrt(x**2 + y**2)
    
    # Check if the point is reachable
    if r > (l1 + l2) or r < abs(l1 - l2):
        raise ValueError("The point is not reachable.")
    
    # Calculate the angle for the second joint
    cos_theta2 = (x**2 + y**2 - l1**2 - l2**2) / (2 * l1 * l2)
    theta2 = math.acos(cos_theta2)
    
    # Calculate the angle for the first joint
    k1 = l1 + l2 * cos_theta2
    k2 = l2 * math.sin(theta2)
    theta1 = math.atan2(y, x) - math.atan2(k2, k1)
    
    return theta1, theta2

# Example usage
x = 1.0
y = 1.0
l1 = 2.0
l2 = 2.0

theta1, theta2 = inverse_kinematics(x, y, l1, l2)
print(f"Theta1: {math.degrees(theta1)} degrees")
print(f"Theta2: {math.degrees(theta2)} degrees")