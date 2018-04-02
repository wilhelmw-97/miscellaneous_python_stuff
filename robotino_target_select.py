import rospy, tf, tf2_ros, geometry_msgs.msg, std_msgs.msg

robotino_state = None

def target_callback(data):
    global  robotino_state
    robotino_state = data.data
    pass


rospy.init_node("robotino_target_select")
rospy.Subscriber('robotino_state', std_msgs.msg.String , target_callback)
rospy.Publisher('target_location', geometry_msgs.msg.Pose2D)


tfBuffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(tfBuffer)
robotino_frame_name = rospy.get_param('~robotino_name','robotino')
rate = rospy.Rate(2)


while not rospy.is_shutdown():
    if robotino_state == 'accu':
        try:
            trans = tfBuffer.lookup_transform(robotino_frame_name, 'world', rospy.Time())
            n = n + 1
            runawaycount = 70
            currentpose[0] = trans.transform.translation.x
            currentpose[1] = trans.transform.translation.y
            currentpose[2] = (tf.transformations.euler_from_quaternion(
                [trans.transform.rotation.x, trans.transform.rotation.y,
                 trans.transform.rotation.z, trans.transform.rotation.w])[2]) * 180 / 3.14

            if n % 10 == 0:
                tfBuffer = tf2_ros.Buffer()
                listener = tf2_ros.TransformListener(tfBuffer)

        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            print 'ignored: ', e
            runawaycount = runawaycount - 1