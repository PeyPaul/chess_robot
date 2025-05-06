
#This file contains the hyperparameters of the robot


# Regarding the communication settings with the motor
port = 'COM3'
baudrate = 38400


# from my measures : l1 = 155; l2 = 135
# old
# l1 = 129
# l2 = 139

# l1 = 182
# l2 = 188

l1 = 490
l2 = 470



#small gers are 19
#big gears are 47
# gear_ratio = 47/19 OLD
gear_ratio = 5.1

gear_ratio_base = 5.1 # WE NEED TO COMPUTE THAT LATER

# gear ratio = 5.1 according to the datasheet




# 75 degree seems to be the max for motor 1

# regarding the position of the arm relative to the board

distance_to_board = 400
case_width = 57.5

height_movement = 230 # height of the arm when it is moving

height_above_piece = 33

piece_heigth = {'pawn': 44, 'rook': 46, 'knight': 57, 'bishop': 67, 'queen': 81, 'king': 94}

discard_position = "j4" # position where we put the pieces we don't want anymore


home_position = (0,200,200) # home position of the arm (x,y,z) in mm