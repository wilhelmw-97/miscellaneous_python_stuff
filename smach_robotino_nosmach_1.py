#!/usr/bin/env python
import rospy
from smach import State, StateMachine
from std_msgs.msg import String

from threading import Lock
import time
import std_srvs.srv, std_msgs.msg

def write_w():
    # % ...
    pass

def interaction_cb(request):
    global state
    if state == 'waitmech':
        state = 'mech2in'
        write_w()
    elif state == 'waitin':
        state == 'in2out'
        write_w()
    elif state == 'waitout':
        write_w()
        state = 'out2mech'
    else:
        rospy.logerr('interation_cb recieved at state: %s' % state)

def l_cb(request):
    global state
    if state == 'mech2in':
        state = 'waitin'
        # % ... notify external
    if state == 'in2out':
        state = 'waitout'
        # % ...
    if state == 'out2mech':
        state = 'waitmech'
        # % ...
    else:
        rospy.logerr('l_cb recieved at state: %s' % state)


# mech2in in2out out2mech waitmech waitin waitout

state = 'waitout'

raspi_listener = rospy.Subscriber('raspi_pseudo_service', String, set_service_callback)
raspi_publisher = rospy.Publisher('robotino_pseudo_service', String, queue_size=10)

interaction_srv = rospy.Service('interaction_complete', std_srvs.srv.Empty, interaction_cb)
l_srv = rospy.Service('l_recieved', std_srvs.srv.Empty, l_cb)

rate = rospy.Rate(35)

while not rospy.is_shutdown():
    rate.sleep()
    if state == 'walk_in_v':
        #print "execute: walk in view"
        pass
    if state == 'ar':
        pass
        #print "execute: ar_code localization"

    if state == 'ar_completed':
        state = 'wait_interaction'
        #print "execute: wait for interactions"

    if state == 'wait_interaction':
        pass

    if state == 'interaction_completed':
        state = 'walk_v'