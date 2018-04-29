#!/usr/bin/env python
import rospy, threading
from smach import State, StateMachine
from std_msgs.msg import String

import time
import std_srvs.srv, std_msgs.msg

flagin = False
state = 'in2out'
tray_flag = 0
def robotino_tray_cb(data):
    global state, tray_flag
    if state == 'waitout':
        if tray_flag < 10: tray_flag += 1
        else:
            tray_flag = 0
            state = 'out2mech'

def write_w():
    w_writer.publish(1)


def waitin_delayed_transition():
    global flagin, state
    time.sleep(5)
    if state == 'waitin':
        state == 'in2out'
        write_w()
    else: rospy.logerr('error! 21')


def waitmech_timeout():
    global state
    time.sleep(6)
    if state == 'waitmech':
        state = 'mech2in'
        write_w()


def waitmech_cb(request):  # waitmech->mech2in
    global state
    if state == 'waitmech' and request.data:
        state = 'mech2in'
        write_w()
    else: rospy.logerr('waitmech_cb called at wrong time')



def l_cb(request): # main loop!
    global state
    if state == 'mech2in': # mech2in->waitin
        state = 'waitin'
        # % ...
        #  the work is transferred into raspi_at_storage.py

        subrt = threading.Thread(target=waitin_delayed_transition) # waitin->in2out
        subrt.start()

    if state == 'in2out': # in2out->waitout
        state = 'waitout'
        # % ...
        # the work is transferred into raspi_at_storage.py
        subrt = threading.Thread(target=waitmech_timeout)
        subrt.start()

    if state == 'out2mech': # out2mech->waitmech
        state = 'waitmech'
        # % ...
        # here we should power the gripper
        # but right now nothing is done
    else:
        rospy.logerr('l_cb recieved at state: %s' % state)


# mech2in in2out out2mech waitmech waitin waitout


# raspi_listener = rospy.Subscriber('raspi_pseudo_service', String, set_service_callback)
# raspi_publisher = rospy.Publisher('robotino_pseudo_service', String, queue_size=10)

# interaction_srv = rospy.Service('interaction_complete', std_srvs.srv.Empty, interaction_cb)
l_srv = rospy.Service('l_recieved', std_srvs.srv.Empty, l_cb)
w_writer = rospy.Publisher('raspi_w', std_msgs.msg.UInt16, queue_size=2)

# pub = rospy.Publisher("arduino_states", std_msgs.msg.String, queue_size=1)
state_pub = rospy.Publisher('robotino_state', std_msgs.msg.UInt16, queue_size=1)
robotino_tray_listener = rospy.Subscriber('robotino_tray', std_msgs.msg.Bool,callback=robotino_tray_cb, queue_size=1)

waitmech_sub = rospy.Subscriber('mech_interaction_over', std_msgs.msg.Bool, callback=waitmech_cb)

#
# states::
#
# in2out    1
# waitout   2
# out2mech  3
# waitmech  4
# mach2in   5
# waitin    6
# other states are undefined

rate = rospy.Rate(4)


while not rospy.is_shutdown():
    rate.sleep()
    if state == 'in2out':
        state_pub.publish(1)
    elif state == 'waitout':
        state_pub.publish(2)
    elif state == 'out2mech':
        state_pub.publish(3)
    elif state == 'waitmech':
        state_pub.publish(4)
    elif state == 'mech2in':
        state_pub.publish(5)
    elif state == 'waitin':
        state_pub.publish(6)
    else: rospy.logerr(('current state undefined: ' + state))




