#!/usr/bin/env python
import rospy
import pygame
import time
from std_msgs.msg import String

#pygame.mixer.music.play()

def callback(data):
   pygame.mixer.music.play()

def listener():
   rospy.init_node('play_reached_sound', anonymous=True)
   rospy.Subscriber('play_sound_file/reached', String, callback)
   rospy.spin()

if __name__ == '__main__':
   pygame.mixer.init()
   pygame.mixer.music.load("/home/chuck/Downloads/reached.mp3")
   listener()

while pygame.mixer.music.get_busy() == True:
