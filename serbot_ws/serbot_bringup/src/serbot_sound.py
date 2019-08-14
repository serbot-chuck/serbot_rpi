#!/usr/bin/env python
import rospy
import pygame
import time
from std_msgs.msg import String
from omxplayer import OMXPlayer

stepAsidePlayer = OMXPlayer('gen.mp3')

def callback(data):
    stepAsidePlayer.play()
    #stepAsideSound.play()
    time.sleep(2.0)
    player.pause()
    
def listener():

    rospy.init_node('serbot_sound', anonymous=True)
    rospy.Subscriber('/play_sound_file', String, callback)

    rospy.spin()

if __name__ == '__main__':
    pygame.mixer.init()
    stepAsideSound = pygame.mixer.Sound('gen.mp3')
    listener()
