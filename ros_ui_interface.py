#!/usr/bin/env python

import socket
import rospy, geometry_msgs.msg, std_msgs.msg
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def robloc_cb(data):
    global s
    locx = data.x
    locy = data.y
    loctheta = data.theta
    
    # % send message
    

    for data in[locx,locy,loctheta]:
            s.send(str(data)+'\n')


def robstt_cb(data):

    instr = data.x

    # % send message 


s.connect(('127.0.0.1', 8000))
rospy.init_node('ui_interface')
sub = rospy.Subscriber('robotino_location', geometry_msgs.msg.Pose2D, robloc_cb, queue_size=1)
# sub1 = rospy.Subscriber('robotino_state', std_msgs.msg.String, robstt_cb, queue_size=1)
rospy.spin()
s.close()
