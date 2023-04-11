#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

class ImageSubscriber:

    def __init__(self):
        self.bridge = CvBridge()
        self.subscriber = rospy.Subscriber("/camera/image_raw", Image, self.callback)
        self.publisher = rospy.Publisher("/image_clahe", Image, queue_size=1)

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "mono8")
        except CvBridgeError as e:
            rospy.logerr(e)

        # Apply CLAHE on the image
        clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(6,6))
        clahe_image = clahe.apply(cv_image)

        try:
            self.publisher.publish(self.bridge.cv2_to_imgmsg(clahe_image, "mono8"))
        except CvBridgeError as e:
            rospy.logerr(e)

if __name__ == '__main__':
    rospy.init_node('image_subscriber', anonymous=True)
    image_subscriber = ImageSubscriber()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")