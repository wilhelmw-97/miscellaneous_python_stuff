#!/usr/bin/env python
import rospy, subprocess, std_msgs.msg

global camhandle

def cam_callback(data):
    global camhandle
    if data.data == False:
        camhandle = subprocess.Popen(['roslaunch', '....'])
    else:
        try:
            camhandle.kill()
        except:
            pass


rospy.init_node('passive_camera_daemon', anonymous=True)
rospy.wait_for_message('accurate_cameras_on', std_msgs.msg.Bool)
rospy.Subscriber('accurate_cameras_on', std_msgs.msg.Bool , cam_callback)
rospy.spin()

