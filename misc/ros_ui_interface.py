#!/usr/bin/env python

import socket
import rospy, geometry_msgs.msg, std_msgs.msg
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
robotino_loc = 0

def robloc_cb(data):
    global s, robotino_loc
    locx = data.x
    locy = data.y
    loctheta = data.theta
  
    #b send message
    for data in[locx,locy,loctheta,robotino_loc]:
            s.send(str(data)+'\n')

def robstt_cb(data):
    global robotino_loc
    robotino_loc = data.data
    # % send message 

s.connect(('127.0.0.1', 8000))
rospy.init_node('ui_interface')
sub = rospy.Subscriber('robotino_location', geometry_msgs.msg.Pose2D, robloc_cb, queue_size=1)
sub1 = rospy.Subscriber('robotino_state', std_msgs.msg.String, robstt_cb, queue_size=1)
rospy.spin()
s.close()
