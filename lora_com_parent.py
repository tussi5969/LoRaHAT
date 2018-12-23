# LoRa communication with python
import RPi.GPIO as GPIO
import sys
import serial
from time import sleep

# Function of send command（コマンド送信を行うための関数）
def sendCommand(ser, time, command):
        sleep(time)
        ser.write(command + "\r\n")

#PIN NO SET
LED1 = 11
LED2 = 13
LED3 = 15
PIR = 7     #PIR（人感センサ）

#GPIO SETUP
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
GPIO.setup(PIR, GPIO.IN)



# Port open（シリアル通信）
ser = serial.Serial('/dev/ttyS0', 115200, timeout = None)

# Send set up command（通信のための初期設定）
sendCommand(ser, 1.00, "SKSREG S08 1A")
sendCommand(ser, 1.00, "SKSREG S01 12345678abcdef77")
sendCommand(ser, 1.00, "SKSREG S05 12345678")
sendCommand(ser, 1.00, "SKSREG S03 0")          #子機の場合は不要
sendCommand(ser, 3.00, "SKSETPSK 11111111222222223333333344444444")
sendCommand(ser, 1.00, "SKSREG S02 0")          #親機は最後を0，子機は最後を1に設定

try:
        # Receive loop start
        while 1:
                receive_data = ser.readline()           #通信データの読み込み
                print receive_data              #通信データの表示

		# Send data
		if "ERXDATA" in receive_data:           #通信データに"ERXDATA"が含まれている場合
			if "0000000000" in receive_data:                #通信データに"0000000000"が含まれている場合（人感センサ不検知）
				GPIO.output(LED1, False)                #LED不点灯

			elif "1111111111" in receive_data:              #通信データに"1111111111"が含まれている場合（人感センサ検知）
				GPIO.output(LED1, True)                 #LED点灯


# Exit with [Ctrl + C]（強制終了）
except KeyboardInterrupt:
        ser.close()     #port close
        print ("\r\n" + "Bye")
        GPIO.cleanup()
        sys.exit
