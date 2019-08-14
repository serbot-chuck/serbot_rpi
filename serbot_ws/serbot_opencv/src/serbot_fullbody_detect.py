#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

import rospy
from std_msgs.msg import String
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os


def fullbody_detect():
    pub = rospy.Publisher('fullbodydetect', String, queue_size=10)
    pub2 = rospy.Publisher('fullbodydetect/image', String, queue_size=10)
    rospy.init_node('fullbodydetect', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))

    # allow the camera to warmup
    time.sleep(0.1)

    model_path = os.path.join(os.path.dirname(__file__), 'haarcascade_fullbody.xml')
    fullbody_cascade = cv2.CascadeClassifier(model_path)

    # capture frames from the camera
    t1 = rospy.get_time()
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        if rospy.is_shutdown():
            break

        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        fullbody = fullbody_cascade.detectMultiScale(gray, 1.1, 5)
        if fullbody != None and len(fullbody) > 0:
            rospy.loginfo('fullbody detected: %s, started %s took %s' % (str(fullbody), t1, rospy.get_time() - t1))
            pub.publish(str(fullbody))


        for (x,y,w,h) in fullbody:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        # show the frame
        cv2.imshow("Frame", image)
        pub2.publish(image)

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        # if the `q` key was pressed, break from the loop
        # key = cv2.waitKey(1) & 0xFF
        # if key == ord("q"):
        #     break                 
        rate.sleep()
	t1 = rospy.get_time()
        #rospy.loginfo('[%s] capture started' % rospy.get_time())


if __name__ == '__main__':
    try:
        fullbody_detect()
    except rospy.ROSInterruptException:
        pass
