#!/usr/bin/env python
# -*-

import rospy, std_msgs.msg, geometry_msgs.msg, tf2_ros, tf
import sys, math, simple_robotino_messages.msg, math
targetpose = [0,0,0]
currentpose = [0,0,0]
#distances = []
def target_callback(data):
    global target
    targetpose = [data.x, data.y, data.theta]

def robloc_callback(data):
    global currentpose
    currentpose = [-data.x, -data.y, -data.theta]


#def distances_callback(data):
#    global distances
#    distances = [data.distance0, data.distance1, data.distance2, data.distance3,
#                 data.distance4, data.distance5, data.distance6, data.distance7 ]

rospy.init_node("robotino_omni_commander")
robotino_frame_name = rospy.get_param('~robotino_name','robotino')
rate = rospy.Rate(30)
tfBuffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(tfBuffer)
runawaycount = 70 # if for 70 cycles this does not recieve a command, try to stop the robot
cmd_vel_publication = geometry_msgs.msg.Twist()


rospy.Subscriber('target_location', geometry_msgs.msg.Pose2D, target_callback)
rospy.Subscriber('robotino_location', geometry_msgs.msg.Pose2D, robloc_callback)
cmd_vel_pub = rospy.Publisher('cmd_vel', geometry_msgs.msg.Twist, queue_size=1)
# rospy.Subscriber('distances', simple_robotino_messages.msg.RobotinoDistanceArray, distances_callback)


while not rospy.is_shutdown():
    rate.sleep()
    try:
        pass



    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
        print  e
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

# diffx, diffy, difftheta(in degrees)
#

    Jcount = 50

    if (out1 == 0):
        rout = difftheta
        if (difftheta < 1):
            Jcount = Jcount - 1
        if (Jcount == 0):
            out1 = 1
            Jcount = 50
    elif (out1 == 1):
        'r = rd?'
        xout = diffx
        if (xout < 1):
            Jcount = Jcount - 1
        if (Jcount == 0):
            out1 = 2
            Jcount = 50
    elif (out1 == 2):
        'r = rd?'
        xout = 0
        yout = diffy
        if (yout < 1):
            Jcount = Jcount - 1
        if (Jcount == 0):
            out1 = 3
            Jcount = 50
    if (out1 == 3):
        complete = 1
        out1 = 0



    command.linear.x = xout
    command.linear.y = yout
    command.angular.z = rout



    cmd_vel_pub.publish(command)

