import serial
import binascii
import time

def read_from_serial(ser):
    try:
        line = ser.read(size=10)
        print(f"Read: {binascii.hexlify(line)}")
    except serial.SerialException as e:
        print(f"Error: {e}")  
    
def send_to_serial(ser, data):
    try:
        ser.write(data)
        print(f"Sent: {binascii.hexlify(data)}")
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

def absolute_positioning(speed, acceleration, position):
    speed = f"{speed:04X}"
    acceleration = f"{acceleration:02X}"
    position = f"{position:08X}"
    command = f"FA01FE{speed}{acceleration}{position}"
    main(command)


def test():
    absolute_positioning(600,2,0)
    time.sleep(5)
    absolute_positioning(600,2,3200) #3200 is 360°
    time.sleep(5)
    absolute_positioning(600,2,0)
    
test()