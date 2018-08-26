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

state = 'off'
rate = rospy.Rate(40)
counter = 0
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN)
pub = rospy.Publisher("proudlink", std_msgs.msg.String, queue_size=1)

while not rospy.is_shutdown():
    pinmode = GPIO.input(12)
    if state == 'off':
        if pinmode == 1:
            counter += 1
            if counter > 4:
                state == 'on'
        else:
            counter = 0

    if state == 'on':
        if pinmode == 0:
            counter += 1
            if counter > 4:
                state == 'off'
        else:
            counter = 0

    rospy.loginfo("recieved: " + str(pinmode))
    pub.publish(state)