import rospy, tf2_ros, tf2_msgs.msg, geometry_msgs.msg, tf






def correct(data):
    if data.transforms[0].child_frame_id.startswith('ar_mark') and not \
         data.transforms[0].child_frame_id.endswith('cted'):
#        data.transforms[0].child_frame_id = data.transforms[0].child_frame_id + '_corrected'
#        data.transforms[0].transform.translation.y, data.transforms[0].transform.translation.z = \
#            data.transforms[0].transform.translation.z, -data.transforms[0].transform.translation.y
        rpy = tf.transformations.euler_from_quaternion(
            [data.transforms[0].transform.rotation.x, data.transforms[0].transform.rotation.y,
             data.transforms[0].transform.rotation.z, data.transforms[0].transform.rotation.w])
        rpy = (rpy[0], rpy[2], -rpy[1])
        quat = tf.transformations.quaternion_from_euler(*rpy)
        data.transforms[0].transform.rotation.x,data.transforms[0].transform.rotation.y,data.transforms[0].transform.rotation.z,data.transforms[0].transform.rotation.w \
         = quat[0], quat[1], quat[2], quat[3]


        t = geometry_msgs.msg.TransformStamped()
        t.header.stamp = rospy.Time.now()
        t.header.frame_id = data.transforms[0].header.frame_id
        t.child_frame_id = data.transforms[0].child_frame_id + '_corrected'
        t.transform.translation.x = data.transforms[0].transform.translation.x
        t.transform.translation.y = data.transforms[0].transform.translation.z
        t.transform.translation.z = - data.transforms[0].transform.translation.y

        t.transform.rotation.x = quat[0]
        t.transform.rotation.y = quat[1]
        t.transform.rotation.z = quat[2]
        t.transform.rotation.w = quat[3]

        br.sendTransform(t)



rospy.init_node("tf2_correction")
#pub = rospy.Publisher('/tf', )
#a = rospy.Time
br = tf2_ros.TransformBroadcaster()

lis_tf = rospy.Subscriber('/tf', tf2_msgs.msg.TFMessage, correct, queue_size=100)


rospy.spin()


