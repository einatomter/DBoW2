#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

image_topic = "/camera/image_raw"
image_topic2 = "/slave1/image_raw/compressed"
clahe_clip_limit = 10.0
clahe_grid_size = (6,6)

class ImageSubscriber:
    def __init__(self):

        self.bridge = CvBridge()

        self.subscriber = rospy.Subscriber(image_topic, Image, self.callback)
        self.subscriber_compressed = rospy.Subscriber(image_topic2, CompressedImage, self.callback_compressed)

        self.publisher = rospy.Publisher("/image_clahe", Image, queue_size=1)

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "mono8")
        except CvBridgeError as e:
            rospy.logerr(e)

        # Apply CLAHE on the image
        clahe = cv2.createCLAHE(clipLimit=clahe_clip_limit, tileGridSize=clahe_grid_size)
        clahe_image = clahe.apply(cv_image)

        try:
            self.publisher.publish(self.bridge.cv2_to_imgmsg(clahe_image, "mono8"))
        except CvBridgeError as e:
            rospy.logerr(e)


    def callback_compressed(self, data):
        np_arr = np.frombuffer(data.data, np.uint8)
        try:
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
        except CvBridgeError as e:
            rospy.logerr(e)

        # Apply CLAHE on the image
        clahe = cv2.createCLAHE(clipLimit=clahe_clip_limit, tileGridSize=clahe_grid_size)
        clahe_image = clahe.apply(cv_image)

        try:
            # self.publisher.publish(self.bridge.cv2_to_imgmsg(cv_image, "mono8"))
            self.publisher.publish(self.bridge.cv2_to_imgmsg(clahe_image, "mono8"))
        except CvBridgeError as e:
            rospy.logerr(e)

if __name__ == '__main__':
    print("starting image subscriber")
    print(f"listening to topic1: {image_topic}")
    print(f"listening to topic2: {image_topic2}")


    rospy.init_node('image_subscriber', anonymous=True)
    image_subscriber = ImageSubscriber()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")