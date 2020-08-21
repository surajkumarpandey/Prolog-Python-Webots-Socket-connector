"""test_control controller."""

from controller import Robot,  DistanceSensor, Motor
import socket
import threading 

direction = ""                                           # incoming data from client used as robot's heading direction        
sensor_data = ""                                         # sensor data sent to the client    
def connect():                                           #socket communication thread
    global direction
    s = socket.socket()
    print('Socket created')
    s.bind(('localhost',9999))
    s.listen(1)
    try:
        while(True):
            c, addr = s.accept()
            direction = c.recv(1024)
            print('Connected with', addr,direction)
            c.send(sensor_data)
            c.close()
    finally:
        s.close()


        

# time in [ms] of a simulation step
TIME_STEP = 64

MAX_SPEED = 6.28

# create the Robot instance.
robot = Robot()

ps = []
psNames = [
    'ps0', 'ps1', 'ps2', 'ps3',
    'ps4', 'ps5', 'ps6', 'ps7'
]

for i in range(8):
    ps.append(robot.getDistanceSensor(psNames[i]))
    ps[i].enable(TIME_STEP)
    
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

left_turn = 0
right_turn = 0

def bot():                                                              # robot control thread
    while robot.step(TIME_STEP) != -1:
        
        global direction, sensor_data
        left_turn = 0
        right_turn = 0
        back = 0
        front = 0
        
        sensor_data = ""
        for i in range(8):
            sensor_data += str(ps[i].getValue()) + " "                 # update the sensor data to be sent to the client   
        
        if direction == 'l':
            left_turn = 1
        elif direction == 'r':
            right_turn = 1
        elif direction == 'b':
            back = 1    
        elif direction == 'f':
            front = 1    
        
        
        print(left_turn,right_turn,back,front)
        
        if left_turn:
            leftSpeed  = -1 * MAX_SPEED
            rightSpeed = MAX_SPEED
        elif right_turn:
            leftSpeed  = MAX_SPEED
            rightSpeed = -1 * MAX_SPEED
        elif back:
            leftSpeed  = -1 * MAX_SPEED
            rightSpeed = -1 * MAX_SPEED
        elif front:
            leftSpeed  = MAX_SPEED
            rightSpeed = MAX_SPEED
        
        else:
            leftSpeed  = 0
            rightSpeed = 0
            
        leftMotor.setVelocity(leftSpeed)
        rightMotor.setVelocity(rightSpeed)
        
if __name__ == "__main__": 
  
    t1 = threading.Thread(target=connect, name='t1') 
    t2 = threading.Thread(target=bot, name='t2')   
  
    # starting threads 
    t1.start() 
    t2.start() 
  
    # wait until all threads finish 
    t1.join() 
    t2.join()
    
        
