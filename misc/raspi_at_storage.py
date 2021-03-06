import rospy
import std_msgs.msg
import time
import threading
import RPi.GPIO as GPIO

# states::
#
# in2out    1
# waitout   2
# out2mech  3
# waitmech  4
# mach2in   5
# waitin    6
# other states are undefined

last_in_call = False
last_out_call = False



def turn_on_in():
    GPIO.output(12, 1)
    rospy.loginfo('button at in pressed')
    time.sleep(2)
    GPIO.output(12, 0)

def turn_on_out():
    GPIO.output(11, 1)
    rospy.loginfo('button at out pressed')
    time.sleep(2)
    GPIO.output(11, 0)


def in_cb(msg):
    global last_in_call, last_out_call
    if msg.data == 6:
        if last_in_call: # rising edge
            last_in_call = True
            # % actuate storage(in)
            aaa = threading.Thread(target=turn_on_in)
            aaa.start()
        if last_in_call == True:
            pass
    else: last_in_call = False

    if msg.data == 2:
        if last_out_call == False: # rising edge
            last_out_call = True
            # % actuate storage(out)
            aaa = threading.Thread(target=turn_on_out)
            aaa.start()
        if last_out_call == True:
            pass
    else: last_out_call = False


state_lis = rospy.Subscriber('robotino_state', std_msgs.msg, in_cb, queue_size=2)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, 0)
rospy.spin()
while not rospy.is_shutdown():
    pass
