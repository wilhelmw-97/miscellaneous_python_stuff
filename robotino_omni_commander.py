#!/usr/bin/env python
import rospy, std_msgs.msg, geometry_msgs.msg, tf2_ros, tf
import sys, math
import simple_robotino_messages.msg
targetpose = [0,0,0]
currentpose = [0,0,0]
distances = []
def target_callback(data):
    global target
    targetpose = [data.x, data.y, data.theta]
def distances_callback(data):
    global distances
    distances = [data.distance0, data.distance1, data.distance2, data.distance3,
                 data.distance4, data.distance5, data.distance6, data.distance7 ]

rospy.init_node("robotino_omni_commander")
robotino_frame_name = rospy.get_param('~robotino_name','robotino')
rate = rospy.Rate(30)
tfBuffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(tfBuffer)
runawaycount = 70 # if for 70 cycles this does not recieve a command, try to stop the robot
cmd_vel_publication = geometry_msgs.msg.Twist()


rospy.Subscriber('target_location', geometry_msgs.msg.Pose2D, target_callback)
cmd_vel_pub = rospy.Publisher('cmd_vel', geometry_msgs.msg.Twist, queue_size=1)
rospy.Subscriber('distances', simple_robotino_messages.msg.RobotinoDistanceArray, distances_callback)


while not rospy.is_shutdown():
    try:
        trans = tfBuffer.lookup_transform(robotino_frame_name, 'world', rospy.Time())
        n = n + 1
        runawaycount = 70
        currentpose[0] = trans.transform.translation.x
        currentpose[1] = trans.transform.translation.y
        currentpose[2] = (tf.transformations.euler_from_quaternion([trans.transform.rotation.x,trans.transform.rotation.y,
                                                                  trans.transform.rotation.z,trans.transform.rotation.w])[2])* 180 / 3.14


        if n % 10 == 0:
            tfBuffer = tf2_ros.Buffer()
            listener = tf2_ros.TransformListener(tfBuffer)

    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
        print 'ignored: ', e
        runawaycount = runawaycount - 1


    if not (runawaycount == 0):
        diffx = targetpose[0] - currentpose[0]
        diffy = targetpose[1] - currentpose[1]
        difftheta = targetpose[2] - currentpose[2]
        if difftheta > 180:
            difftheta = difftheta - 360
        elif difftheta < -180:
            difftheta = difftheta + 360

    command = geometry_msgs.msg.Twist()
##############################################
    #
    # main speed calculation happens here.
    # given in the original ros package:
    # max linear velocity is 0.2 and min is 0.05
    # mas angular velocity is 1 and min is 0.1
    #
    # notice that we want to change as possible the acceleration but not the speed
    #
###############################################

    ##############################################
    #
    #   case 1: precise navigation: slow and simple
    #
    ##############################################

    command.linear.x = diffx / 10
    if command.linear.x > 0.1: command.linear.x = 0.1
    if command.linear.x < 0.05: command.linear.x = 0.05

    command.linear.y = diffx / 10
    if command.linear.y > 0.1: command.linear.y = 0.1
    if command.linear.y < 0.05: command.linear.y = 0.05

    command.angular.z =  - difftheta / 1000
    if command.angular.z < 0.1: command.angular.z = 0.1
    if command.angular.z > 0.4: command.angular.z = 0.4

    cmd_vel_pub.publish(command)



'''
    ##############################################
    #
    #   case 2: coarse navigation: manipulates acceleration
    #
    ##############################################

##############################################
#
#   step 1: calculate target speed
#
##############################################
    diff_mag_squared = (diffx ** 2 + diffy ** 2)
    v_mag_should = diff_mag_squared / 12
    if v_mag_should > 0.2: v_mag_should = 0.2 # speed maxed at diff_mag = 1.5m

    k = (v_mag_should / diff_mag_squared) ** 0.5

    vx_should = diffx * k # speed maxes at 2m
    vy_should = diffy * k

    omega_should = difftheta / 70
    if omega_should > 1: omega_should = 1

# then, reduce speed in accordance to distance sensors
# seperate plane into 8 parts

    if cmd_vel_publication.linear.y > 0 and cmd_vel_publication.linear.x > cmd_vel_publication.linear.y:
        # part 1
        if distances[0] < 0.3:
            emergencybreak = True
        elif distances[0] < 0.6:
            vx_should = vx_should / 2
        if distances[1] < 0.3:
            emergencybreak = True
        elif distances[1] < 0.6:
            vx_should = vx_should / 1.7
        if distances[7] < 0.3:
            emergencybreak = True
        elif distances[7] < 0.6:
            vx_should = vx_should / 1.7




##############################################
#
#   step 2: calculate acceleration and add to last command
#
##############################################

##############################################

    rate.sleep()
'''