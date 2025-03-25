from motor_control import move_arm
import hyperparameters as hp


def position_to_coordinates(position: str, color = "w"): # DO NOT USE CAPITAL LETTERS
    if color == 'b':
        y = hp.distance_to_board + hp.case_width/2 + hp.case_width * ( 8 - int(position[1]))
        x = 4.5 *hp.case_width - (ord(position[0])-96) * hp.case_width
    else:
        y = hp.distance_to_board + hp.case_width/2 + hp.case_width * (int(position[1]) - 1)
        x = - 4.5 *hp.case_width + (ord(position[0])-96) * hp.case_width
    return x, y
    
#print(position_to_coordinates("g7", "b"))

def path_planning(start_position: str, end_position: str): # HARDCODE PIECE4S HEIGHT
    x_start, y_start = position_to_coordinates(start_position)
    x_end, y_end = position_to_coordinates(end_position)
    
    move_arm(x_start, y_start, hp.height)
    move_arm(x_start, y_start, 0)
    # grab piece
    move_arm(x_start, y_start, hp.height)
    
    move_arm(x_end, y_end, hp.height)
    move_arm(x_end, y_end, 0)
    # release piece
    move_arm(x_end, y_end, hp.height)
    
    # go home position
    pass

path_planning("g7", "g6")