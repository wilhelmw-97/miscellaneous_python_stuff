import rospy, subprocess, simple_robotino_messages.srv

#
#
# obsolete!
#
#

subprocesshandle = None

def srvcb(request):
    global subprocesshandle
    if not request.process == '...': return False
    if request.value == True:
        subprocesshandle = subprocess.Popen(['roslaunch', '...'])
        return True
    else:
        subprocesshandle.terminate() # ctrl+c
        # subprocesshandle.kill() # forces exit
        return True


rospy.init_node('process_coordinator', anonymous=True)
service = rospy.Service('execute_process', simple_robotino_messages, srvcb)
rospy.spin()


