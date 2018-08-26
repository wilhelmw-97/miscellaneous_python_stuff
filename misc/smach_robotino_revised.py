#!/usr/bin/env python
import rospy
from smach import State, StateMachine
from std_msgs.msg import String
from threading import Lock
import time


class RobotinoData():
    def __init__(self, pubto_ard_zy, listen_ard_rpi, pubto_ard_rpi):
        self.zy_ard_signal_recieved = False
        self.L_2to3 = False
        self.L_3to1 = False
        self.conveyor_tray_recieved = False
        self.L_1to2 = False

        self.pubto_zy = pubto_ard_zy
        self.listen_rpi = listen_ard_rpi
        self.pubto_rpi = pubto_ard_rpi
    def clear(self):
        self.zy_ard_signal_recieved = False
        self.L_2to3 = False
        self.L_3to1 = False
        self.conveyor_tray_recieved = False
        self.L_1to2 = False
       # self.currentState = 0



def set_service_callback(data):
    global robotinoData
    print('service_callback: %s', data.data)
    if(data.data == 'gotL'):

        if robotinoData.L_1to2 == False:
            robotinoData.L_1to2 = True
        elif robotinoData.L_2to3 == False:
            robotinoData.L_2to3 = True
        elif robotinoData.L_3to1 == False:
            robotinoData.L_3to1 = True
        else: rospy.logerr('unable to set state at set_L_cb')
    elif(data.data == 'gotT'):
        robotinoData.conveyor_tray_recieved = True
    elif(data.data == '2go1'):
        robotinoData.zy_ard_signal_recieved = True
        rospy.logdebug('zy_ard signal is recieved')
    else: rospy.logerr("invalid input at set_L_cb")


#---------------------------------
# clean up these later!
def push_tray_at_3():
#is actually "start to push"
    global robotinoData
    robotinoData.pubto_rpi.publish('uuuu')
    rospy.logdebug('sending to onboard arduino "pushT"')


def pickup_tray_at_1():
    #is actually "start to pick". dont block!
    global robotinoData
    robotinoData.pubto_rpi.publish('iiii')
    rospy.logdebug('sending to onboard arduino "pickT"')


def send_w_at_2():
    global robotinoData
    robotinoData.pubto_rpi.publish('tttt')
    rospy.logdebug('sending to onboard arduino "2to3"')


def send_w_at_3():
    global robotinoData
    robotinoData.pubto_rpi.publish('tttt')
    rospy.logdebug('sending to onboard arduino "3to1"')

def send_w_at_1():
    global robotinoData
    
    robotinoData.pubto_rpi.publish('tttt')
    rospy.loginfo('send_w_at_1 called(buggy?)')

def send_zy_imback():
    global robotinoData
    robotinoData.pubto_zy.publish('allow')
    rospy.logdebug('sending to zy arduino "allow"')

def send_zy_imgone():
    global robotinoData
    robotinoData.pubto_zy.publish('no')
    rospy.logdebug('sending to zy arduino "no"')

class Standby_loc2(State):
    global robotinoData
    def __init__(self):
        self.rate = rospy.Rate(5)
        State.__init__(self, outcomes=['success'])
    def execute(self, ud):

        rospy.loginfo('smach state -> standby_loc2 using time.slep')
#        while robotinoData.zy_ard_signal_recieved == False:
#            self.rate.sleep()
        time.sleep(6)
        send_zy_imgone()
        send_w_at_2()
        return 'success'

class Move_2to3(State):
    global robotinoData
    def __init__(self):
        self.rate = rospy.Rate(5)
        State.__init__(self, outcomes=['success'])
    def execute(self, ud):
        rospy.loginfo('smach state -> move2to3')

        while robotinoData.L_2to3 == False:
            self.rate.sleep()
#        push_tray_at_3()
        return 'success'

class Arriving_at_3(State):
    global robotinoData
    def __init__(self):

        State.__init__(self, outcomes=['success'])
    def execute(self, ud):

        rospy.loginfo('smach state -> arrive_at_3 using time.slep')
        time.sleep(6) # this time should be changed!!
        send_w_at_3()
        return 'success'

class Move_3to1(State):
    global robotinoData
    def __init__(self):
        self.rate = rospy.Rate(5)
        State.__init__(self, outcomes=['success'])
    def execute(self, ud):
        rospy.loginfo('smach state -> move_3to1')
        while robotinoData.L_3to1 == False:

            self.rate.sleep()
#        pickup_tray_at_1()
        return 'success'

class Standby_loc1(State):
    global robotinoData
    def __init__(self):
        self.rate = rospy.Rate(5)
        State.__init__(self, outcomes=['success'])
    def execute(self, ud):
        rospy.loginfo('smach state -> standby_loc1 using time.slep')
#        while robotinoData.conveyor_tray_recieved == False:
#            self.rate.sleep()
#        
        time.sleep(5)
        send_w_at_1()
        robotinoData.clear()
        return 'success'

class Move_1to2(State):
    global robotinoData
    def __init__(self):
        self.rate = rospy.Rate(5)
        State.__init__(self, outcomes=['success'])
    def execute(self, ud):
        rospy.loginfo('smach state -> move_1to2')
        while robotinoData.L_1to2 == False:
            self.rate.sleep()
        send_zy_imback()
        return 'success'

class initstate(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
    def execute(self, ud):
        time.sleep(3)

        send_w_at_1()
        return('success')
#-----------------------------------

if __name__ == '__main__':
    rospy.init_node('raspi')



#    zy_ard_listener = rospy.Subscriber('/tray_placement_state', String, set_zy_ard_callback(), 2)
    zy_ard_publisher = rospy.Publisher('zyt_pseudo_service', String, queue_size=10)
    raspi_listener = rospy.Subscriber('raspi_pseudo_service', String, set_service_callback)
    #sm_announcer = rospy.Publisher('robotino_state', String, queue_size= 1)
    raspi_publisher = rospy.Publisher('robotino_pseudo_service', String, queue_size=10)

    while not rospy.is_shutdown():
        robotinoData = RobotinoData(zy_ard_publisher, raspi_listener, raspi_publisher)
        sm = StateMachine(outcomes=['success'])
        with sm:
            StateMachine.add('INIT', initstate(), transitions={'success': 'MOVE_1to2'})
            StateMachine.add('MOVE_1to2', Move_1to2(), transitions={'success':'STANDBY_2'})
            StateMachine.add('STANDBY_1', Standby_loc1(), transitions={'success':'MOVE_1to2'})
            StateMachine.add('STANDBY_2', Standby_loc2(), transitions={'success':'MOVE_2to3'})
            StateMachine.add('MOVE_2to3', Move_2to3(), transitions={'success':'STANDBY_3'})
            StateMachine.add('STANDBY_3', Arriving_at_3(), transitions={'success':'MOVE_3to1'})
            StateMachine.add('MOVE_3to1', Move_3to1(), transitions={'success':'STANDBY_1'})

        sm.execute()
        rospy.loginfo("! sm finished executing a round.")
        del sm
        del robotinoData
