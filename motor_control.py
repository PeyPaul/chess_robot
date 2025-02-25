import serial
import binascii
import time
import math
from inverse_kinematics import inverse_kinematics
import hyperparameters as hp

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

def main(command): #if __name__ == "__main__":
    port = 'COM3'
    baudrate = 38400
    data = int(command+checksum(bytes.fromhex(command)), 16).to_bytes(int(len(command)/2) + 1, byteorder='big')
    ser = serial.Serial(port, baudrate, timeout=1)
    print(f"Port: {port}, Baudrate: {baudrate}, Data: {data}")
    send_to_serial(ser, data)
    read_from_serial(ser)
    ser.close()

# start : FA01F681F002
# stop : FA01F6000002

def absolute_positioning(slave, speed, acceleration, position):
    speed = f"{speed:04X}"
    acceleration = f"{acceleration:02X}"
    position = f"{position:08X}"
    slave = f"{slave:02X}"
    command = f"FA{slave}FE{speed}{acceleration}{position}"
    main(command)


def test(x, y):
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

absolute_positioning(1,600,2,0)
time.sleep(3)
absolute_positioning(1,600,2,int(3200*20/360*hp.gear_ratio))
time.sleep(3)


### 3 motors ###

def _3_motors_absolute_positioning(speed, acceleration, position1, position2, position3):
    absolute_positioning(speed, acceleration, position1)
    absolute_positioning(speed, acceleration, position2)
    absolute_positioning(speed, acceleration, position3)