import rospy
from std_srvs.srv import *
import std_msgs.msg
import geometry_msgs.msg

running = False
force_loc = False
location = geometry_msgs.msg.Pose2D()
state = std_msgs.msg.String()

def srvcb(req):
    global running
    running = req.data


def loc_pick_cb(req):
    global force_loc, location, state
    force_loc = True
    state.data = ''

    location.x = 0
    location.y = 0
    location.theta = 0


def loc_drop_cb(req):
    pass


def loc_mach_cb(req):
    pass


rospy.init_node('littlepart')
srv_handle = rospy.Service('gen_running', SetBool, srvcb)
srv_handle = rospy.Service('gen_at_mach', Empty, srvcb)
srv_handle = rospy.Service('gen_at_drop', Empty, srvcb)
srv_handle = rospy.Service('gen_at_pick', Empty, srvcb)

pub_loc = rospy.Publisher('robotino_location', geometry_msgs.msg.Pose2D, queue_size=1)
pub_state = rospy.Publisher('robotino_state', std_msgs.msg.String, queue_size=1)

rate = rospy.Rate(20)



while not rospy.is_shutdown():
    rate.sleep()


    state.data = ''

    location.x = 0
    location.y = 0
    location.theta = 0

    pub_loc.publish(location)
    pub_state.publish(state)
