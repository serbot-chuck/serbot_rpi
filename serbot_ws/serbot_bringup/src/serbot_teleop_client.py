#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import RPi.GPIO as GPIO

# Set the GPIO modes
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Set variables for the GPIO motor pins
#RIGHT
Motor1A = 16
Motor1B = 18
Motor1E = 22

#LEFT
#Motor2A = 19
#Motor2B = 21
#Motor2E = 23

Motor2A = 21
Motor2B = 19
Motor2E = 23

#Motor2A = 23
#Motor2B = 21
#Motor2E = 19

# How many times to turn the pin on and off each second
Frequency = 100
# How long the pin stays on each cycle, as a percent (here, it's 30%)
DutyCycle = 30
DutyCycle2 = 35
# Setting the duty cycle to 0 means the motors will not turn
Stop = 0

# Set the GPIO Pin mode to be Output
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

# Set the GPIO to software PWM at 'Frequency' Hertz
p1 = GPIO.PWM(Motor1E, Frequency)
p2 = GPIO.PWM(Motor2E, Frequency)

p1.start(Stop)
p2.start(Stop)

# Turn all motors off
def StopMotors():
    p1.start(Stop)
    p2.start(Stop)

    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)

# Turn both motors forwards
def Forwards():
    p1.start(DutyCycle2)
    p2.start(DutyCycle)

    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)

    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)

#    pwmMotorAForwards.ChangeDutyCycle(DutyCycle)
#    pwmMotorABackwards.ChangeDutyCycle(Stop)
#    pwmMotorBForwards.ChangeDutyCycle(DutyCycle)
#    pwmMotorBBackwards.ChangeDutyCycle(Stop)

def Backwards():
    p1.start(DutyCycle2)
    p2.start(DutyCycle)

    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)

    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)

#    pwmMotorAForwards.ChangeDutyCycle(Stop)
#    pwmMotorABackwards.ChangeDutyCycle(DutyCycle)
#    pwmMotorBForwards.ChangeDutyCycle(Stop)
#    pwmMotorBBackwards.ChangeDutyCycle(DutyCycle)

# Turn left
def Left():

#    p1.start(DutyCycle)
    p2.start(DutyCycle)

#    GPIO.output(Motor1A,GPIO.HIGH)
#    GPIO.output(Motor1B,GPIO.LOW)
#    GPIO.output(Motor1E,GPIO.HIGH)

    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)

#    pwmMotorAForwards.ChangeDutyCycle(Stop)
#    pwmMotorABackwards.ChangeDutyCycle(DutyCycle)
#    pwmMotorBForwards.ChangeDutyCycle(DutyCycle)
#    pwmMotorBBackwards.ChangeDutyCycle(Stop)

# Turn Right
def Right():
    p1.start(DutyCycle2)
#    p2.start(DutyCycle)

    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)

#    GPIO.output(Motor2A,GPIO.HIGH)
#    GPIO.output(Motor2B,GPIO.LOW)
#    GPIO.output(Motor2E,GPIO.HIGH)

#    pwmMotorAForwards.ChangeDutyCycle(DutyCycle)
#    pwmMotorABackwards.ChangeDutyCycle(Stop)
#    pwmMotorBForwards.ChangeDutyCycle(Stop)
#    pwmMotorBBackwards.ChangeDutyCycle(DutyCycle)

# Message handler
def CommandCallback(commandMessage):
#    rospy.loginfo(rospy.get_caller_id() + "I heard %s", commandMessage.data)
    command = commandMessage.data
    if command == 'w':
        print('Moving forwards')
        Forwards()
    elif command == 's':
        print('Moving backwards')
        Backwards()
    elif command == 'a':
        print('Turning left')
        Left()
    elif command == 'd':
        print('Turning right')
        Right()
    elif command == ' ':
        print('Stopping')
        StopMotors()
    else:
        print('Unknown command, stopping instead')
        StopMotors()


#def callback(data):
#    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    
def listener():
    rospy.init_node('driver', anonymous=True)

    rospy.Subscriber("command", String, CommandCallback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

    print('Shutting down: stopping motors')
    StopMotors()
    GPIO.cleanup()

if __name__ == '__main__':
    listener()
