import rospy, tf, tf2_ros, std_msgs.msg, geometry_msgs.msg, std_srvs.srv

ar_state = 'nf' #not found or found

rospy.init_node("robotino_target_select")
rospy.Subscriber('robotino_state', std_msgs.msg.String , target_callback)
targetpub = rospy.Publisher('target_location', geometry_msgs.msg.Pose2D)
rospy.ServiceProxy('interaction_complete', std_srvs.srv.Empty, interaction_complete_response)

tfBuffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(tfBuffer)
robotino_frame_name = rospy.get_param('~robotino_name','robotino')
rate = rospy.Rate(5)
currentpose = []


while not rospy.is_shutdown():
    rate.sleep()
    try:
        trans = tfBuffer.lookup_transform(robotino_frame_name, 'world', rospy.Time())
        n = n + 1
        runawaycount = 35
        currentpose[0] = trans.transform.translation.x
        currentpose[1] = trans.transform.translation.y
        currentpose[2] = (tf.transformations.euler_from_quaternion(
            [trans.transform.rotation.x, trans.transform.rotation.y,
             trans.transform.rotation.z, trans.transform.rotation.w])[2]) * 180 / 3.14

        if n % 10 == 0:
            tfBuffer = tf2_ros.Buffer()
            listener = tf2_ros.TransformListener(tfBuffer)