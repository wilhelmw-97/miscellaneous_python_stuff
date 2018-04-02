#!/usr/bin/env python  
import rospy

import math
import tf2_ros
import geometry_msgs.msg
import turtlesim.srv

if __name__ == '__main__':
    base = raw_input("look up tf from parent frame:")
    if len(base) == 0: a = 'world'
    child = raw_input("to child frame:")
    if len(child) == 0: b = 'ar_marker_1'

    rospy.init_node('tf2_listener')

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)
    n = 0

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            trans = tfBuffer.lookup_transform(child, base, rospy.Time())
            n = n + 1
            print n, ': trans.x: ', trans.transform.translation.x, 'trans.y: ', trans.transform.translation.y, 'trans.z: ', trans.transform.translation.z
            if n % 10 == 0:
# second approach
                tfBuffer.clear()

#             tfBuffer = tf2_ros.Buffer()
#             listener = tf2_ros.TransformListener(tfBuffer)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            print e
            rate.sleep()
            continue



        rate.sleep()