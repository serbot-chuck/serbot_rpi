#!/usr/bin/env python
from __future__ import print_function

import roslib
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time
import os

class fullbody_detector:

  def __init__(self):
    self.pub = rospy.Publisher('fullbodydetect', String, queue_size=10)
    self.image_pub = rospy.Publisher("fullbodydetect/image",Image)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/image",Image,self.callback)
    rate = rospy.Rate(10)


  def callback(self,data):
    # allow the camera to warmup  
    time.sleep(0.1)

    model_path = os.path.join(os.path.dirname(__file__), 'haarcascade_fullbody.xml')
    fullbody_cascade = cv2.CascadeClassifier(model_path)

    # capture frames from the camera
    t1 = rospy.get_time()
    for frame in self.bridge.imgmsg_to_cv2(data, "bgra8"):

        if rospy.is_shutdown():
            break

        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        fullbody = fullbody_cascade.detectMultiScale(gray, 1.1, 5)
        if fullbody != None and len(fullbody) > 0:
            rospy.loginfo('fullbody detected: %s, started %s took %s' % (str(faces), t1, rospy.get_time() - t1))
            self.pub.publish(str(fullbody))


        for (x,y,w,h) in fullbody:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        # show the frame
        cv2.imshow("Frame", image)
        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(image, "bgra8"))
        except CvBridgeError as e:
            print(e)

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
                
        rate.sleep()
	t1 = rospy.get_time()

def main(args):
  fd = fullbody_detector()
  rospy.init_node('fullbody_detector', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
