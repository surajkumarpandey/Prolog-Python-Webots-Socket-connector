"""test_control controller."""

from controller import Robot, Motor
import socket
import threading 

data = ""                                           #incoming data from client used as robot's heading direction        

def connect():                                      #socket communication thread
    global data
    s = socket.socket()
    print('Socket created')
    s.bind(('localhost',9999))
    s.listen(1)
    while(True):
        c, addr = s.accept()
        data = c.recv(1024)
        print('Connected with', addr,data)
        c.close()
    


        

# time in [ms] of a simulation step
TIME_STEP = 64

MAX_SPEED = 6.28

# create the Robot instance.
robot = Robot()


leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

left_turn = 0
right_turn = 0

def bot():                                                              #robot control thread
    while robot.step(TIME_STEP) != -1:
        
        global data
        left_turn = 0
        right_turn = 0
        back = 0
        front = 0
        
        if data == 'l':
            left_turn = 1
        elif data == 'r':
            right_turn = 1
        elif data == 'b':
            back = 1    
        elif data == 'f':
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
    
        