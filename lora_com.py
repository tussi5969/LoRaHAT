
# LoRa communication with python
import RPi.GPIO as GPIO
import sys
import serial
from time import sleep

# Function of send command
def sendCommand(ser, time, command):
	sleep(time)
	ser.write(command + "\r\n")

#PIN NO SET
LED1 = 11   #16
LED2 = 13
LED3 = 15
PIR = 7     #PIR

#GPIO SETUP
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
GPIO.setup(PIR, GPIO.IN)




# Port open
ser = serial.Serial('/dev/ttyS0', 115200, timeout = None)

# Send set up command
sendCommand(ser, 1.00, "SKSREG S08 1A")
sendCommand(ser, 1.00, "SKSREG S01 12345678abcdef05")
sendCommand(ser, 1.00, "SKSREG S05 12345678")
sendCommand(ser, 3.00, "SKSETPSK 11111111222222223333333344444444")
sendCommand(ser, 1.00, "SKSREG S02 1")

try:
	# Receive loop start
	while 1:
		receive_data = ser.readline()
		print receive_data

		# Send data
		if "ERXBCN" in receive_data:
			if GPIO.input(PIR) == GPIO.HIGH:
				ser.write("SKSEND 0000000000000000 5 1111111111" + "\r\n")
				print ("********** Detected!!! **********" + "\r\n")
			elif GPIO.input(PIR) == GPIO.LOW:
				ser.write("SKSEND 0000000000000000 5 0000000000" + "\r\n")
                                print ("********** NOT... **********" + "\r\n")


# Exit with [Ctrl + C]
except KeyboardInterrupt:
	ser.close()	#port close
	print ("\r\n" + "Bye")
	GPIO.cleanup()
	sys.exit
