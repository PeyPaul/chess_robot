import serial
import binascii
import time
import math
import struct
from inverse_kinematics import paul_inverse_kinematics
import hyperparameters as hp
from jonas import jonas_inverse_kinematics
from gripper import open_gripper, close_gripper

# theta10 = 26
# theta20 = 21
# theta30 = 0

theta10 = 146
theta20 = -14
theta30 = 0


### Functions to send and receive data from the serial port ###


def read_from_serial(ser):
    try:
        line = ser.read(size=10)
        #print(f"Read: {binascii.hexlify(line)}")
    except serial.SerialException as e:
        print(f"Error: {e}")  
    
def send_to_serial(ser, data):
    try:
        ser.write(data)
        #print(f"Sent: {binascii.hexlify(data)}")
    except serial.SerialException as e:
        print(f"Error: {e}")

def checksum(data):
    checksum = 0
    for byte in data:
        checksum += byte
    checksum = checksum & 0xFF
    return f"{checksum:02X}"

def test_checksum():
    data = bytes.fromhex("FA 01 80 00")
    print(f"Data: {data}")
    print(f"Checksum: {checksum(data)}")

def check_port():
    ser = serial.Serial('COM3', 38400)
    if not ser.isOpen():
        ser.open()
    print('com3 is open', ser.isOpen())

def main(command: str):
    port = 'COM3'
    baudrate = 38400
    data = int(command+checksum(bytes.fromhex(command)), 16).to_bytes(int(len(command)/2) + 1, byteorder='big')
    ser = serial.Serial(port, baudrate, timeout=0.1)
    print(f"Port: {port}, Baudrate: {baudrate}, Data: {data}")
    send_to_serial(ser, data)
    read_from_serial(ser)
    ser.close()
    

### Function to send commands to the motor controller ###


def homing():
    main("FA019400000000010320")
    main("FA029400000000010320")
    main("FA039400000000010320")

    main("FA01830BB8")
    main("FA02830BB8")
    #main("FA03830BB8")

    main("FA0191")
    main("FA0291")
    #main("FA0391")
    time.sleep(3)

def absolute_positioning(slave, speed, acceleration, position):
    speed = f"{speed:04X}"
    acceleration = f"{acceleration:02X}"
    position = f"{position & 0xFFFFFFFF:08X}"
    slave = f"{slave:02X}"
    command = f"FA{slave}FE{speed}{acceleration}{position}"
    print(command)
    main(command)

def test(x,y):

    theta1, theta2 = paul_inverse_kinematics(x, y, hp.l1, hp.l2)

    print(f"Theta1: {math.degrees(theta1)} degrees")
    print(f"Theta2: {math.degrees(theta2)} degrees")
    
    theta1 = math.degrees(theta1)
    theta2 = math.degrees(theta2)
    
    theta2 = theta2 - theta1
    
    print("theta1", theta1)
    print("theta2", theta2)

    theta1 = theta1 - theta10
    theta2 = theta2 - theta20

    print("theta1", theta1)
    print("theta2", theta2)

    theta1 = int(3200*theta1/360)
    theta2 = int(3200*theta2/360)
    
    absolute_positioning(1,600,2,-int(theta1*hp.gear_ratio))
    absolute_positioning(2,600,2,-int(theta2*hp.gear_ratio))

def jonas(x,y):
    theta1, theta2 = jonas_inverse_kinematics(hp.l1, hp.l2, x,y)
    
    print(f"Theta1: {theta1} degrees")
    print(f"Theta2: {theta2} degrees")

    theta1 = theta1 - theta10
    theta2 = theta2 - theta20 
    
    theta2 = theta2 / 1.38

    print("theta1", theta1)
    print("theta2", theta2)

    theta1 = int(3200*theta1/360) +10
    theta2 = int(3200*theta2/360)-10
    
    absolute_positioning(1,600,2,-int(theta1*hp.gear_ratio))
    absolute_positioning(2,600,2,-int(theta2*hp.gear_ratio))

def move_arm(x,y,angle):
    jonas(x,y)
    absolute_positioning(3,600,2,-int(3200*angle*hp.gear_ratio_base/360))
    
def go_to_position(position: str):
    theta1, theta2, angle = hp.position[position]
    print(theta1, theta2, angle)
    absolute_positioning(1,600,2,-int(3200*theta1*hp.gear_ratio/360))
    absolute_positioning(2,600,2,-int(3200*theta2*hp.gear_ratio/360))
    absolute_positioning(3,100,2,-int(3200*angle*hp.gear_ratio_base/360))


if __name__ == "__main__":
    pass

    
### Some demo functions ###


def demo_1():
    homing()

    time.sleep(3)
    jonas(400, 50)
    time.sleep(3)
    jonas(400, 300)

    time.sleep(1.5)
    jonas(700, 200)
    time.sleep(3)
    jonas(400, 400)
    time.sleep(1.5)

    homing()


def demo_horse_pick():
    homing()
    time.sleep(3)
    for i in range(0,20):
        jonas(400,200)
        time.sleep(1.5)
        jonas(400, 15)
        time.sleep(3)
    jonas(400, 400)


def demo_square(gripper: bool = False):
    positions = ['a8', 'a2', 'h2', 'h8']
    homing()
    if gripper:
        open_gripper()
    time.sleep(3)
    for pos in positions:
        go_to_position(pos)
        time.sleep(3)
        if gripper:
            open_gripper()
            time.sleep(3)
            close_gripper()
            time.sleep(3)
        move_arm(400, 400, 0)
        time.sleep(3)

def demo_delimitation():
    positions = ['a8', 'idle', 'a2', 'idle','b8', 'idle','b2', 'idle',
                'c8', 'idle','c2', 'idle','d8', 'idle','d2', 'idle',
                'e8', 'idle','e2', 'idle','f8', 'idle','f2', 'idle',
                'g8', 'idle','g2', 'idle','h8', 'idle','h2', 'idle']
    homing()
    time.sleep(3)
    for pos in positions:
        go_to_position(pos)
        time.sleep(3)
    homing()
    
demo_delimitation()
### Functions used to read values from the serial port ###



def read_motor_position(ser, motor_id, gear_ratio=5.1):
    # Création de la commande : FA XX 30 + CRC
    command = bytes.fromhex(f"FA{motor_id:02X}30")
    crc = checksum(command)
    full_command = command + bytes.fromhex(crc)

    send_to_serial(ser, full_command)

    response = ser.read(size=10)  # taille typique attendue
    if len(response) < 9:
        return None

    # Décodage de la réponse
    if response[0] == 0xFB and response[1] == motor_id and response[2] == 0x30:
        carry_bytes = response[3:7]  # 4 octets signés
        value_bytes = response[7:9]  # 2 octets non signés

        carry = struct.unpack(">i", carry_bytes)[0]
        value = struct.unpack(">H", value_bytes)[0]

        absolute_position = carry * 0x4000 + value
        degrees = (absolute_position * 360) / (16384 * gear_ratio) # conversion pulses → degrés
        return round(degrees, 2)

    return None

def read_all_motors_continuously():
    port = 'COM3'
    baudrate = 38400
    ser = serial.Serial(port, baudrate, timeout=0.1)
    
    print("Lecture continue des positions moteurs (Ctrl+C pour arrêter)")
    
    try:
        while True:
            for motor_id in [1, 2, 3]:
                ratio = hp.gear_ratio if motor_id < 3 else hp.gear_ratio_base
                angle = read_motor_position(ser, motor_id, ratio)
                if angle is not None:
                    print(f"🔁 Moteur {motor_id}: {angle}°")
                else:
                    print(f"⚠️ Erreur de lecture moteur {motor_id}")
            print("-" * 30)
            time.sleep(10)
    except KeyboardInterrupt:
        print("⏹️ Lecture arrêtée.")
    finally:
        ser.close()
        
# if __name__ == "__main__":
#     main("FA019B00")
#     main("FA029B00")
#     main("FA039B00")
#     read_all_motors_continuously()
#     main("FA019B04")
#     main("FA029B04")
#     main("FA039B04")