#!/usr/bin/env python
import rospy
from std_msgs.msg import String

import time
import sys
import tty
import termios
from adafruit_motorkit import MotorKit

kit = MotorKit()

def Forwards():
    kit.motor1.throttle = 0.5
    kit.motor2.throttle = 0.5

def Backwards():
    kit.motor1.throttle = -0.5
    kit.motor2.throttle = -0.5

def TurnLeft():
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.5

def TurnRight():
    kit.motor1.throttle = 0.5
    kit.motor2.throttle = 0.0

def StopMotors():
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0


# Message handler
def CommandCallback(commandMessage):
    command = commandMessage.data
    if command == 'w':
        print('Moving forwards')
        Forwards()
    elif command == 's':
        print('Moving backwards')
        Backwards()
    elif command == 'a':
        print('Turning left')
        TurnLeft()
    elif command == 'd':
        print('Turning right')
        TurnRight()
    elif command == ' ':
        print('Stopping')
        StopMotors()
    elif command == 'i':
        print('Pressing I from the PC')
    else:
        print('Unknown command, stopping instead')
        StopMotors()



def listener():
    rospy.init_node('driver', anonymous=True)

    rospy.Subscriber("command", String, CommandCallback)

    rospy.spin()

    print('Shutting down: stopping motors')
    StopMotors()
    
if __name__ == '__main__':
    listener()

