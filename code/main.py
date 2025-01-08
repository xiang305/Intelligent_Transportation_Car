from flask import Flask, Response, request
import cv2
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

camera = cv2.VideoCapture(0)

IN1 = 31 
IN2 = 33
IN3 = 35
IN4 = 37

GPIO.setmode(GPIO.BOARD)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)

pwm_right = GPIO.PWM(IN1, 100)
pwm_left = GPIO.PWM(IN3, 100)
pwm_right.start(0)
pwm_left.start(0)

button_press_history = []
is_recording = False 

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_right.ChangeDutyCycle(0)
    pwm_left.ChangeDutyCycle(0)

def move_backward(speed=100):
    print("Move Backward")
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm_right.ChangeDutyCycle(speed)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_left.ChangeDutyCycle(speed) 

def move_forward():
    print("Move Forward")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def move_left():
    print("Turn Left")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def move_right():
    print("Turn Right")
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = cv2.flip(frame, 0)
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/move')
def move():
    direction = request.args.get('direction')
    press_time = time.time()  # 記錄按下的時間

    if direction == 'forward':
        move_forward()
    elif direction == 'backward':
        move_backward()
    elif direction == 'left':
        move_left()
    elif direction == 'right':
        move_right()
    elif direction == 'stop':
        stop()

    # 如果正在紀錄，則記錄按鈕被按下的時間和方向
    if is_recording:
        if direction != 'stop':
            button_press_history.append({
                'direction': direction,
                'time': press_time
            })
    
    return '', 204

@app.route('/toggle_record')
def toggle_record():
    global button_press_history, is_recording
    
    if is_recording:
        # 停止紀錄        
        is_recording = False
        print(f"紀錄儲存資料: {button_press_history}")
        return '紀錄', 200   
    else:
        button_press_history = []  # 清空記錄
        is_recording = True
        return '停止紀錄', 200
    
@app.route('/toggle_return')
def toggle_return():
    global button_press_history
    # 按照記錄的動作順序倒序執行
    for action in reversed(button_press_history):
        direction = action['direction']
        if direction == 'forward':
            move_backward()
        elif direction == 'backward':
            move_forward()
        elif direction == 'left':
            move_right()
        elif direction == 'right':
            move_left() 
        time.sleep(1)
    stop()
    button_press_history = []
    return '已返回起點', 200

@app.route('/')
def index():
    # 顯示簡單的網頁，嵌入攝像頭串流
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Camera Stream</title>
        <style>
            body{
                overflow: hidden;  /* 禁用所有滾動條 */
            }
            #container{
              display: flex;
              justify-content: space-between;
              align-items: flex-start;
              height: 100vh;
              margin: 0;
            }
            #title{
                text-align: center;
                font-size: 2rem;
                margin: 20px 0;
            }

            #video-container {
                margin: 20px auto;
            }
            
            #camera-stream {
                width: 50%;
                object-fit: contain;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
            }

            #controls {
              display: flex;
              flex-direction: column;
              justify-content: center;
              margin-left: 200px;
              margin-top: 20px;
            }

            #direction-controls {
              display: flex;
              flex-direction: column;
              justify-content: center;
              margin-right: 200px;
              margin-top: 20px;
            }

            button {
              margin: 10px 0;
              padding: 10px 20px;
              font-size: 1rem;
              cursor: pointer;
            }
            
            #status {
                position: fixed;
                text-align: center;
                font-size: 1.5rem;
                width: 100%;
                bottom: 40px;
            }
        </style>
        <script>
            let currentDirection = null;  // 當按下按鈕時持續發送指令
            function startMoving(command) {
                if (currentDirection !== command) {
                    fetch(`/move?direction=${command}`, { method: 'GET' });
                    currentDirection = command;
                    updateStatus(currentDirection);
                }
            }
            // 當放開按鈕時停止移動
            function stopMoving() {
                fetch(`/move?direction=stop`, { method: 'GET' });
                currentDirection = null;
                updateStatus(currentDirection);
            }
            //顯示車子目前狀況
            function updateStatus(direction) {
                const statusElement = document.getElementById('status');
                if (direction === 'forward') {
                    statusElement.innerText = '目前正在前進';
                } else if (direction === 'backward') {
                    statusElement.innerText = '目前正在後退';
                } else if (direction === 'left') {
                    statusElement.innerText = '目前正在左轉';
                } else if (direction === 'right') {
                    statusElement.innerText = '目前正在右轉';
                } else {
                    statusElement.innerText = '目前保持靜止';
                }
            }
            // 偵測按鈕按下與放開
            window.onload = function() {
                const buttons = document.querySelectorAll('button');
                buttons.forEach(button => {
                    button.onmousedown = () => startMoving(button.id);
                    button.onmouseup = stopMoving;
                    button.onmouseleave = stopMoving;  // 防止滑鼠離開時停止
                });
            };

            function toggleRecord() {
                fetch('/toggle_record')
                    .then(response => response.text())
                    .then(data => {
                        document.getElementById("recordButton").innerText = data;
                    });
            }
            function toggleReturn() {
                fetch('/toggle_return')
                    .then(response => response.text())
                    .then(data => {
                        alert(data);  // 提示返回完成
                    });
            }
        </script>
    </head>
    <body>
        <h1 id="title">物流概念遙控車</h1>
        <div id="container">
            <div id="controls">
                <button id="recordButton" onclick="toggleRecord()">紀錄</button>
                <button id="return" onclick="toggleReturn()">返回起點</button>
            </div>
            
            <div id="video-container">
                <img id="camera-stream" src="/video_feed">
            </div>
            
            <div id="direction-controls">
                <button id="forward">前進</button>
                <button id="backward">後退</button>
                <button id="left">左轉</button>
                <button id="right">右轉</button>
            </div>
        </div>
        <div id="status">目前保持靜止</div>
    </body>
    </html>
    '''

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        GPIO.cleanup()
