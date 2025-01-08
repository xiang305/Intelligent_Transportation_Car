import RPi.GPIO as GPIO
import time

# 定義 L298N 的 GPIO 接腳
IN1 = 31  # GPIO 接腳號
IN2 = 33
IN3 = 35
IN4 = 37

# 初始化 GPIO 模式
GPIO.setmode(GPIO.BOARD)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)

def stop():
    # 停止所有馬達
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def forward():
    # 前進：左輪正轉，右輪正轉
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def backward():
    # 後退：左輪反轉，右輪反轉
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    
# 測試程式
try:
    for i in range(5):
        print("前進 2 秒")
        forward()
        time.sleep(2)
        print("後退 2 秒")
        backward()
        time.sleep(2)
        print("停止 2 秒")
        stop()
        time.sleep(2)

except KeyboardInterrupt:
    print("程式中止")

finally:
    GPIO.cleanup()

