#!/usr/bin/env python
import rospy, threading

from std_msgs.msg import String

import time
import std_srvs.srv, std_msgs.msg



flagin = False
state = 'in2out'
tray_flag = 0
last_l_cb = 0
flag_wait_mech_and_out = [0, 0, 0]


def write_w(num = 0):
    global w_writer
    rospy.loginfo('writeW@'+num)
    w_writer.publish(1)
    w_writer.publish(1)
    w_writer.publish(1)
    time.sleep(0.001)
    w_writer.publish(1)
    w_aux_pub.publish(True)
    w_aux_pub.publish(True)


def waitout_delayed_transition(flag_in_2):
    global state
    time.sleep(5)
    if state == 'waitout':
        write_w('62')
        flag_in_2[2] = 1
    else: rospy.logerr('error! 64')


def robotino_tray_cb(data):
    global state, tray_flag

    if data.data == False: return
    rospy.loginfo('tray_cb_called')
    if state == 'waitout':
        if tray_flag < 6:
            tray_flag += 1
            rospy.loginfo('flag is now: ' + str(tray_flag))
            sub = threading.Thread(target=waitout_delayed_transition, args=(flag_wait_mech_and_out,))
            sub.start()
        else:

            rospy.loginfo('goto out2mech(3)')
            tray_flag = 0


    else:
        rospy.loginfo('but exited due to state: ' + state)





def waitin_delayed_transition(flag_in_1):
    global flagin, state
    rospy.loginfo('subrt started. in 5 secs go to in2out')
    rospy.loginfo('current state:' + str(state))
    time.sleep(5)
    if state == 'waitin':

        write_w('54')
        flag_in_1[1] = 1
    else: rospy.logerr('error! 21')



def waitmech_timeout():
#    global state
#    rospy.loginfo('subrt started. in 6 secs go to mech2in')
#    time.sleep(6)
#    if state == 'waitmech':
#        state = 'mech2in'
#        write_w()
#    rospy.loginfo('subrt ended.')
#    rospy.loginfo('state: ' + state)
    pass

def waitmech_cb(request):  # waitmech->mech2in
    global state
    if state == 'waitmech' and request.data:
        state = 'mech2in'
        write_w('74')
    else: rospy.logerr('waitmech_cb called at wrong time')



def l_cb(request): # main loop!

    global state
    global last_l_cb
    rospy.loginfo('l_cb recieved at state: %s' % state)
    this_l_cb = rospy.get_time()
    if this_l_cb - last_l_cb < 0.6:
        last_l_cb = this_l_cb
        return
    last_l_cb = this_l_cb
    if state == 'mech2in': # mech2in->waitin
        state = 'waitin'
        # % ...
        #  the work is transferred into raspi_at_storage.py

        subrt = threading.Thread(target=waitin_delayed_transition, args=(flag_wait_mech_and_out,)) # waitin->in2out
        subrt.start()

    if state == 'in2out': # in2out->waitout

        rospy.loginfo('goto waitout and start sub')
        # % ...
        # the work is transferred into raspi_at_storage.py
        subrt = threading.Thread(target=waitmech_timeout)
        subrt.start()
        state = 'waitout'

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
rospy.init_node('robotino')
# interaction_srv = rospy.Service('interaction_complete', std_srvs.srv.Empty, interaction_cb)
l_srv = rospy.Subscriber('l_recieved', std_msgs.msg.Bool, callback=l_cb)
w_writer = rospy.Publisher('raspi_w', std_msgs.msg.UInt16, queue_size=2)

# pub = rospy.Publisher("arduino_states", std_msgs.msg.String, queue_size=1)
state_pub = rospy.Publisher('robotino_state', std_msgs.msg.UInt16, queue_size=1)
robotino_tray_listener = rospy.Subscriber('robotino_tray', std_msgs.msg.Bool,callback=robotino_tray_cb, queue_size=1)

waitmech_sub = rospy.Subscriber('mech_interaction_over', std_msgs.msg.Bool, callback=waitmech_cb)
w_aux_pub = rospy.Publisher('w_aux', std_msgs.msg.Bool, queue_size=2)

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

    if flag_wait_mech_and_out[1] == 1:
        if state == 'waitin':
            state = 'in2out'
            flag_wait_mech_and_out[1] = 0
        else:
            rospy.logerr('162, state = ' + state)

    if flag_wait_mech_and_out[2] == 1:
        if state == 'waitout':
            state = 'out2mech'
            flag_wait_mech_and_out[2] = 0
            write_w('179')
        else:
            rospy.logerr('180, state = ' + state)


