import rospy, geometry_msgs.msg

rospy.init_node('aaaaaa')

pub = rospy.Publisher('/cmd_vel', geometry_msgs.msg.Twist, queue_size= 1)

msg = geometry_msgs.msg.Twist()
rate = rospy.Rate(1)
while not rospy.is_shutdown():
    msg.linear.x = 0
    msg.linear.y = 0
    msg.angular.z = -0.05

    pub.publish(msg)

    rate.sleep()
