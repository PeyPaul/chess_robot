import serial
import time

arduino = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)

while True:
    def send_angle(angle):
        if angle == "":
            arduino.write(b"\n")
        else:
            angle_str = str(angle) + "\n"
            arduino.write(angle_str.encode('utf-8'))
    stoppEnter=(input("enter or s:" )).lower()
    angle=160
    send_angle(angle)
    if stoppEnter=="s":break
    stoppEnter=(input("enter or s:" )).lower()
    angle=90
    if stoppEnter=="s":break
    send_angle(angle)
    #time.sleep(1)