import rospy, tf, tf2_ros, geometry_msgs, sys


parent_frame_name = sys.argv[1]
parent_trans_x = sys.argv[2]
parent_trans_y = sys.argv[3]
parent_trans_z = sys.argv[4]
parent_rot_roll = sys.argv[5]
parent_rot_pitch = sys.argv[6]
parent_rot_yaw = sys.argv[7]
child_frame_name = sys.argv[8]
child_trans_x = sys.argv[9]
child_trans_y = sys.argv[10]
child_trans_z = sys.argv[11]
child_rot_roll = sys.argv[12]
child_rot_pitch = sys.argv[13]
child_rot_yaw = sys.argv[14]

if len(sys.argv) != 15:
    print 'incorrect number of args.'

    exit(1)

br = tf2_ros.TransformBroadcaster()




def handle_turtle_pose(msg, turtlename):

    t = geometry_msgs.msg.TransformStamped()

    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "world"
    t.child_frame_id = turtlename
    t.transform.translation.x = msg.x
    t.transform.translation.y = msg.y
    t.transform.translation.z = 0.0
    q = tf.transformations.quaternion_from_euler(0, 0, msg.theta)
    t.transform.rotation.x = q[0]
    t.transform.rotation.y = q[1]
    t.transform.rotation.z = q[2]
    t.transform.rotation.w = q[3]

    br.sendTransform(t)

if __name__ == '__main__':
    rospy.init_node('tf2_turtle_broadcaster')
    turtlename = rospy.get_param('~turtle')
    rospy.Subscriber('/%s/pose' % turtlename,
                     turtlesim.msg.Pose,
                     handle_turtle_pose,
                     turtlename)
    rospy.spin()