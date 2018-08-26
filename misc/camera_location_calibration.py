#!/usr/bin/env python
import rospy, tf, tf2_ros, geometry_msgs, sys

'''
usage:
for calibration of coordinates of markers
and for coordination of 2 cameras

1. 2 cameras should report same location for the same marker
2. get the coordinates of waypoints with this node


'''

rospy.init_node('tf2_turtle_broadcaster')
print 'publishing transformations. using this node in a launch file is suggested.'
if len(sys.argv) != 8:
    print 'incorrect number of args. give 8 args:'
    print 'parent frame, child frame, x, y, z, roll, pitch, yaw'


    exit(1)

br = tf2_ros.TransformBroadcaster()

parent_frame_name = sys.argv[1]
child_frame_name = sys.argv[2]
trans_x = sys.argv[3]
trans_y = sys.argv[4]
trans_z = sys.argv[5]
roll = sys.argv[6]
pitch = sys.argv[7]
yaw = sys.argv[8]
rate = rospy.Rate(201)
while not rospy.is_shutdown():
    rate.sleep()
    t = geometry_msgs.msg.TransformStamped()

    t.header.stamp = rospy.Time.now()
    t.header.frame_id = sys.argv[1]
    t.child_frame_id = sys.argv[2]
    t.transform.translation.x = sys.argv[3]
    t.transform.translation.y = sys.argv[4]
    t.transform.translation.z = sys.argv[5]
    q = tf.transformations.quaternion_from_euler(sys.argv[6], sys.argv[7], sys.argv[8])
    t.transform.rotation.x = q[0]
    t.transform.rotation.y = q[1]
    t.transform.rotation.z = q[2]
    t.transform.rotation.w = q[3]

    br.sendTransform(t)


