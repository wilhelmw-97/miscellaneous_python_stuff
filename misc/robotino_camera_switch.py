#!/usr/bin/env python
import rospy, tf, tf2_ros, geometry_msgs.msg, std_msgs.msg

accurate_ar_marker_names = ['ar_marker_0']
accurate_ar_marker_names_count = [0]
lookup_fail_count = 0
lookup_fail_count2 = 0 # count of passes in which no accurate marker is found

tfBuffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(tfBuffer)

rate = rospy.Rate(30)
internal_false_suppress = 0
if internal_false_suppress > 12:
    internal_false_suppress = 0
    accurate_ar_marker_names_count = [0] * len(accurate_ar_marker_names)

accu_cam = rospy.Publisher("accurate_cameras_on", std_msgs.msg.Bool, latch=True, queue_size=1)
accu_cam.publish(False)
cam_state = 'coarse'
# coar_cam = rospy.Publisher("coarse_cameras", std_msgs.msg.Bool, latch=True, queue_size=1)

while not rospy.is_shutdown():


    rate.sleep()
    lookup_fail_count = 0
    if internal_false_suppress > 20:
        internal_false_suppress = 0
        lookup_fail_count2 = 0
    for i in range(len(accurate_ar_marker_names)):
        try:
            trans = tfBuffer.lookup_transform(accurate_ar_marker_names[i], 'world', rospy.Time())
            print accurate_ar_marker_names[i], 'detected'
            accurate_ar_marker_names_count[i] = accurate_ar_marker_names_count[i] + 1
            if False: #if already in accurate:
                lookup_fail_count = 0
                lookup_fail_count2 = 0
            if accurate_ar_marker_names_count[i] > 8:
                # % handle change to accurate
                accu_cam.publish(True)


                pass
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            lookup_fail_count = lookup_fail_count + 1

    if lookup_fail_count == accurate_ar_marker_names_count:
        lookup_fail_count2 = lookup_fail_count2 + 1

    if lookup_fail_count2 > 10:
        #% handle change to coarse
        accu_cam.publish(False)

