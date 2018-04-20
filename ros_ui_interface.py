import rospy, geometry_msgs.msg, std_msgs.msg

def robloc_cb(data):

    locx = data.x
    locy = data.y
    loctheta = data.theta
    # % send message

def robstt_cb(data):

    instr = data.x

    # % send message


rospy.init_node('ui_interface')
sub = rospy.Subscriber('robotino_location', geometry_msgs.msg.Pose2D, robloc_cb, queue_size=1)
sub1 = rospy.Subscriber('robotino_state', std_msgs.msg.String, robstt_cb, queue_size=1)