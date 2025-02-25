import math
import matplotlib.pyplot as plt


## Example usage
#x = 200
#y = 100
#l1 = 155
#l2 = 135
## from my measures : l1 = 155; l2 = 135




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
    theta2 = -math.acos(cos_theta2)
    
    # Calculate the angle for the first joint
    k1 = l1 + l2 * cos_theta2
    k2 = l2 * math.sin(theta2)
    theta1 = math.atan2(y, x) - math.atan2(k2, k1)
    
    return theta1, theta2


# let's try to visualize the result on a chart
def visualize():
    theta1, theta2 = inverse_kinematics(x, y, l1, l2)
    print(f"Theta1: {math.degrees(theta1)} degrees")
    print(f"Theta2: {math.degrees(theta2)} degrees")
    # Compute joint positions
    joint1_x = l1 * math.cos(theta1)
    joint1_y = l1 * math.sin(theta1)
    joint2_x = joint1_x + l2 * math.cos(theta1 + theta2)
    joint2_y = joint1_y + l2 * math.sin(theta1 + theta2)

    # Plot the arm
    plt.figure(figsize=(5, 5))
    plt.plot([0, joint1_x, joint2_x], [0, joint1_y, joint2_y], 'o-', markersize=8, linewidth=3, label='Arm')
    plt.xlim(-l1-l2, l1+l2)
    plt.ylim(-l1-l2, l1+l2)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.legend()
    plt.title("2-Link Robotic Arm Visualization")
    plt.show()

#visualize()