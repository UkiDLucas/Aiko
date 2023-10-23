"""

"""
# Importing the math module
import math

def calculate_beam_width(theta, adjacent):
    """
    For the known laser beam's angle (theta) in degrees 
    and the distance known as "adjacent" side of the right triangle,
    calculate the "opposite" side which is half of the beam width.
    see: right_triangle_trigonometry.png
    Angular beam width is only half of the angle
    """
    opposite = math.tan(math.radians(theta/2)) * adjacent
    beam_width = 2 * opposite   
    return beam_width

theta = 1.2 # beam angle in degrees
adjacent = 220 # meters distance from the LiDAR to the target

beam_width = calculate_beam_width(theta, adjacent)


print ("The beam width side is: ", round(beam_width,3), " meters.")


