import serial
import binascii
import time
import math
from inverse_kinematics import inverse_kinematics
import hyperparameters as hp
from jonas import jonas_inverse_kinematics

# theta10 = 26
# theta20 = 21
# theta30 = 0

theta10 = 146
theta20 = -14
theta30 = 0

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



# start : FA01F681F002
# stop : FA01F6000002

def absolute_positioning(slave, speed, acceleration, position):
    speed = f"{speed:04X}"
    acceleration = f"{acceleration:02X}"
    position = f"{position & 0xFFFFFFFF:08X}"
    slave = f"{slave:02X}"
    command = f"FA{slave}FE{speed}{acceleration}{position}"
    print(command)
    main(command)


def test(x,y):

    theta1, theta2 = inverse_kinematics(x, y, hp.l1, hp.l2)

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


def horse_pick():
    homing()
    time.sleep(3)
    for i in range(0,20):
        jonas(400,200)
        time.sleep(1.5)
        jonas(400, 15)
        time.sleep(3)
    jonas(400, 400)
    
horse_pick()


def move_arm(x, y, z): # we will need to work on this function
    
    theta3 = math.atan2(x,y)
    theta3 = math.degrees(theta3)
    
    r = math.sqrt(x**2 + y**2)
    
    theta1, theta2 = inverse_kinematics(r, z, hp.l1, hp.l2)

    theta1 = math.degrees(theta1)
    theta2 = math.degrees(theta2)
    
    theta2 = theta2 - theta1

    theta1 = theta1 - theta10
    theta2 = theta2 - theta20
    theta3 = theta3 - theta30

    print("theta1", theta1)
    print("theta2", theta2)
    print("theta3", theta3)

    theta1 = int(3200*theta1/360)
    theta2 = int(3200*theta2/360)
    theta3 = int(3200*theta3/360)
    
    absolute_positioning(1,600,2,int(theta1*hp.gear_ratio))
    absolute_positioning(2,600,2,int(theta2*hp.gear_ratio))
    absolute_positioning(3,600,2,int(theta3*hp.gear_ratio_base))

# move_arm(200,200,200)
# time.sleep(1)
# move_arm(150,100,-200)

   
    
    
def test2(x, y):
    l1 = 2.0
    l2 = 2.0
    theta1, theta2 = inverse_kinematics(x, y, l1, l2)
    theta1 = int(abs(3200*math.degrees(theta1)/360))
    theta2 = int(abs(3200*math.degrees(theta2)/360))
    print(f"Theta1: {theta1} steps")
    print(f"Theta2: {theta2} steps")
    for i in range(1,3):
        absolute_positioning(i,600,2,0)
        print(i)
    time.sleep(5)
    absolute_positioning(1,600,2,theta1)
    absolute_positioning(2,600,2,theta2)
    #for i in range(1,3):
    #    absolute_positioning(i,600,2,3200) #3200 is 360°
    time.sleep(5)
    for i in range(1,3):
        absolute_positioning(i,600,2,0)
    
#test(1,1)