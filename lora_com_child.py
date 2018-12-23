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
sendCommand(ser, 1.00, "SKSREG S01 12345678abcdef05")
sendCommand(ser, 1.00, "SKSREG S05 12345678")
sendCommand(ser, 3.00, "SKSETPSK 11111111222222223333333344444444")
sendCommand(ser, 1.00, "SKSREG S02 1")          #親機は最後を0，子機は最後を1に設定

try:
        # Receive loop start
        while 1:
                receive_data = ser.readline()           #通信データの読み込み
                print receive_data              #通信データの表示

                # Send data
                if "ERXBCN" in receive_data:            #通信データに"ERXBCN"が含まれている場合
                        if GPIO.input(PIR) == GPIO.HIGH:                #人感センサが検知した場合
                                ser.write("SKSEND 0000000000000000 5 1111111111" + "\r\n")              #"1111111111"をデータとして送る
                                print("********** Detected!!! **********" + "\r\n")

                        elif GPIO.input(PIR) == GPIO.LOW:               #人感センサが検知しなかった場合
                                ser.write("SKSEND 0000000000000000 5 0000000000" + "\r\n")              #"0000000000"をデータとして送る
                                print ("********** NOT... **********" + "\r\n")


# Exit with [Ctrl + C]（強制終了）
except KeyboardInterrupt:
        ser.close()     #port close
        print ("\r\n" + "Bye")
        GPIO.cleanup()
        sys.exit
