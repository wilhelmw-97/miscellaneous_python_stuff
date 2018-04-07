

import rospy, tf2_ros, tf2_msgs.msg, geometry_msgs.msg, tf
import subprocess

t0 = [0, 0, 0, 0, 0, 0] # in meter and degrees!
t1 = [0, 0, 0, 0, 0, 0]
t8 = [0, 0, 0, 0, 0, 0]
tfs = [t0, t1, t8]

subprocess.Popen(['rosrun', 'tf2_ros', 'static_transform_publisher', \
                  str(tfs[0][0]), str(tfs[0][1]), str(tfs[0][2]), str(tfs[0][3]), str(tfs[0][4]), str(tfs[0][5]), \
                  'world', 'ar_8_actual'])


def correct(data):
    if data.transforms[0].child_frame_id == 'ar_marker_8':
#        data.transforms[0].child_frame_id = data.transforms[0].child_frame_id + '_corrected'
#        data.transforms[0].transform.translation.y, data.transforms[0].transform.translation.z = \
#            data.transforms[0].transform.translation.z, -data.transforms[0].transform.translation.y


        t = geometry_msgs.msg.TransformStamped()
        t.header.stamp = rospy.Time.now()
        t.header.frame_id = data.transforms[0].header.frame_id
        t.child_frame_id = data.transforms[0].child_frame_id + '_corrected'
        t.transform.translation.x = t0[0] + data.transforms[0].transform.translation.z # data.transforms[0].transform.translation.x
        t.transform.translation.y = t0[1] - data.transforms[0].transform.translation.x # data.transforms[0].transform.translation.z
        t.transform.translation.z = t0[2] - data.transforms[0].transform.translation.y


        rpy = tf.transformations.euler_from_quaternion(
            [data.transforms[0].transform.rotation.x, data.transforms[0].transform.rotation.y,
             data.transforms[0].transform.rotation.z, data.transforms[0].transform.rotation.w])
        rpy = (t0[3]+ rpy[2], t0[4] - rpy[0] + 3.1415926, t0[5] - rpy[1])
        quat = tf.transformations.quaternion_from_euler(*rpy)
        data.transforms[0].transform.rotation.x, data.transforms[0].transform.rotation.y, data.transforms[
            0].transform.rotation.z, data.transforms[0].transform.rotation.w \
            = quat[0], quat[1], quat[2], quat[3]

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



