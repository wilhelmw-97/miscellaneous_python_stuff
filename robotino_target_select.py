#!/usr/bin/env python
# this is the node1
# waypoints are changed here

import rospy, tf, tf2_ros, geometry_msgs.msg, std_msgs.msg, std_srvs.srv, time, threading, subprocess
import simple_robotino_messages.srv

subprocess.Popen(['rosrun', 'tf2_ros', 'static_transform_publisher', \
                  0,0,0,0,0,0, 'ar_8_actual', 'robotino_from_ar_8'])

accurate_frames=['robotino_from_ar_8', 'non_existent_frame1', 'non_existent_frame_2']

robotino_state = 'coarse' # may be useful for UI: wait state or not wait state?

#def target_callback(data):
#    global  robotino_state
#    robotino_state = data.data

def interaction_complete_response(data):
    global interaction_complete
    interaction_complete = True

def delayed_wait():
    global robotino_state
    time.sleep(4)
    robotino_state = 'wait'

class Waypoint(object):
    def __init__(self, ix, iy, iomg, is_accurate):
        self.x = ix
        self.y = iy
        self.theta = iomg
        self.isaccurate = is_accurate

    def distance_squared(self, x, y):
        return (self.x - x)** 2 + (self.y - y) ** 2

rospy.init_node("robotino_target_select")
#rospy.Subscriber('robotino_state', std_msgs.msg.String , target_callback)
targetpub = rospy.Publisher('target_location', geometry_msgs.msg.Pose2D, queue_size=1, latch=True)
robotinopub = rospy.Publisher('robotino_location', geometry_msgs.msg.Pose2D, queue_size=1)
rospy.ServiceProxy('interaction_complete', std_srvs.srv.Empty, interaction_complete_response)

tfBuffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(tfBuffer)
robotino_frame_name = rospy.get_param('~robotino_name','robotino')
rate = rospy.Rate(5)
currentpose = []
___succeeded = False


waypoints = [Waypoint(1,1,90,False), Waypoint(3,3,180,True)]



current_wp_index = 0
while not rospy.is_shutdown():
    rate.sleep()

    try:
        trans = tfBuffer.lookup_transform(accurate_frames[0], 'world', rospy.Time())
        ___succeeded = True
    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
        try:
            trans = tfBuffer.lookup_transform(accurate_frames[1], 'world', rospy.Time())
            ___succeeded = True
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            try:
                trans = tfBuffer.lookup_transform(accurate_frames[2], 'world', rospy.Time())
                ___succeeded = True
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
                try:
                    trans = tfBuffer.lookup_transform(robotino_frame_name, 'world', rospy.Time())
                    ___succeeded = True
                except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
                    print 'ignored: ', e
                    runawaycount = runawaycount - 1






    if ___succeeded:
        ___succeeded = False
        n = n + 1
        runawaycount = 35
        currentpose[0] = -trans.transform.translation.x
        currentpose[1] = -trans.transform.translation.y
        currentpose[2] = -(tf.transformations.euler_from_quaternion(
            [trans.transform.rotation.x, trans.transform.rotation.y,
             trans.transform.rotation.z, trans.transform.rotation.w])[2]) * 180 / 3.14

        posemsg = geometry_msgs.msg.Pose2D()
        posemsg.x = currentpose[0]
        posemsg.y = currentpose[1]
        posemsg.theta = currentpose[2]
        robotinopub.publish(posemsg)

        if n % 10 == 0:
            tfBuffer = tf2_ros.Buffer()
            listener = tf2_ros.TransformListener(tfBuffer)



    if runawaycount <= 0: rospy.logerr('node 1 cannot find robotino coordinate!')

    if Waypoint[current_wp_index].isaccurate == False:


            if Waypoint[current_wp_index].distance_squared(currentpose[0], currentpose[1]) < 0.01 \
                    and -10 < Waypoint[current_wp_index].theta - currentpose[2] < 10 :

#                if Waypoint[current_wp_index].isaccurate == False :

                    current_wp_index = current_wp_index + 1

#                else:
                    # process camera selection, etc
                    # actually, camera selection will be done on finding specific markers
                    # here nothing is done
#                   pass
            # also look for accurate markers


    if Waypoint[current_wp_index].isaccurate == True:

        if Waypoint[current_wp_index].distance_squared(currentpose[0], currentpose[1]) < 0.025 \
                and 7 < Waypoint[current_wp_index].theta - currentpose[2] < 7:
            ta = threading.Thread(target=delayed_wait)
            ta.start()



    if robotino_state == 'wait':
        if interaction_complete == True: # % wait for external interactions completion: give new waypoint
            interaction_complete = False
            # robotino_state = 'coarse'
            #

            current_wp_index = current_wp_index + 1
            if current_wp_index > len(waypoints): current_wp_index = 0



    # % publish waypoint here
    if robotino_state != 'wait':
        targetmsg = geometry_msgs.msg.Pose2D()
        targetmsg.x = waypoints[current_wp_index].x
        targetmsg.y = waypoints[current_wp_index].y
        targetmsg.theta = waypoints[current_wp_index].theta
        targetpub.publish()
    # ######



###########################################################
'''
    if robotino_state == 'accu':
        try:
            trans = tfBuffer.lookup_transform(robotino_frame_name, 'world', rospy.Time())
            n = n + 1
            runawaycount = 70
            currentpose[0] = trans.transform.translation.x
            currentpose[1] = trans.transform.translation.y
            #currentpose[2] = (tf.transformations.euler_from_quaternion(
            #    [trans.transform.rotation.x, trans.transform.rotation.y,
            #     trans.transform.rotation.z, trans.transform.rotation.w])[2]) * 180 / 3.14


            if n % 10 == 0:
                tfBuffer = tf2_ros.Buffer()
                listener = tf2_ros.TransformListener(tfBuffer)

        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            print 'ignored: ', e
            runawaycount = runawaycount - 1
'''