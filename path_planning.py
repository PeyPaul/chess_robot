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

def path_planning(start_position: str, end_position: str, piece_move: str):
    x_start, y_start = position_to_coordinates(start_position)
    x_end, y_end = position_to_coordinates(end_position)
    pick_up_height = hp.piece_heigth[piece_move] + hp.height_above_piece
    
    move_arm(x_start, y_start, hp.height_movement)
    move_arm(x_start, y_start, pick_up_height)
    # grab piece
    move_arm(x_start, y_start, hp.height_movement)
    
    move_arm(x_end, y_end, hp.height_movement)
    move_arm(x_end, y_end, pick_up_height)
    # release piece
    move_arm(x_end, y_end, hp.height_movement)
    
    # go home position
    x,y,z = hp.home_position
    move_arm(x, y, z)
    pass

path_planning("g7", "g6")

def play(start_position: str, end_position: str, piece_move: str, capture: bool = False, piece_captured: str = None):
    if capture:
        path_planning(end_position, hp.discard_position, piece_captured)
    path_planning(start_position, end_position, piece_move)
    pass