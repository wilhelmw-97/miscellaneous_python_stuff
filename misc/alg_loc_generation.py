import math, rospy, geometry_msgs.msg, std_msgs.msg
import random
PointA = [400, 0]
PointAA = [400, -70]

point = [400, 0]

PointB = [210, 0]
PointBB = [210, -70]

PointC = [0, 225]

ang = 90

Status = 0

CircleCount = 50

TurningCount = 90


#D6.get = d7
#D7.get
#D8.get // jiting
#W.

D6, D7, D8, W = 0,0,0,0
# last_subd6cb = 0
last_wcb = 0d

############
''
def subd6cb(data):
    global D6, D7, D8 #, last_subd6cb
    # if rospy.get_time() - last_subd6cb <= 1000: return
    # last_subd6cb = rospy.get_time()
    print(data.data)

#    if str(data.data)[-1] == '1':
#        D8 = 1
#    else: D8 = 0
#    if str(data.data)[-2] == '1':

#        D6, D7 = 1, 1
#    else: D6, D7 = 0, 0
    D6, D7 = 1,1
def wcb(data):
    global last_wcb
    if rospy.get_time() - last_wcb <= 0.8: return
    last_wcb = rospy.get_time()
    global W
    W = 1

rospy.init_node('loc_generation')
pub = rospy.Publisher('robotino_location', geometry_msgs.msg.Pose2D, queue_size=1)
subd6 = rospy.Subscriber('trace_generation_aux', std_msgs.msg.UInt16, subd6cb)
subw = rospy.Subscriber('w_aux', std_msgs.msg.Bool, wcb)

rate = rospy.Rate(10)
while not rospy.is_shutdown():
    rate.sleep()
    print 'D6: ', D6, 'W: ', W, 'S: ', Status, 'A: ', ang
    #if (D6 == 1):
    D6 = 1
    #if (D7 == 1):
    D7 = 1

    breaked = D8
    if (breaked == 1):
        pass

    elif (Status == 0) and (D6 == 1):
        TurningCount -= 9
        ang -= 9
        if (TurningCount == 0):
            TurningCount = 90
            Status = 0.1
            D6 = 0
            D7 = 0

    elif (Status == 0.1):
        if not (point[1] == PointAA[1]):
            point[1] -= 1
        elif (W == 1):
            Status = 1
            W = 0

    elif (Status == 1):
        point[1] += 1
        if (point[1] == 0):
            Status = 1.05

    elif (Status == 1.05):
        TurningCount -= 9
        ang += 9
        if (TurningCount == 0):
            TurningCount = 180
            Status = 1.1

    elif (Status == 1.1) and (D6 == 1):
        point[0] -= 1
        if (point[0] == 50):
            Status = 1.2
            D6 = 0
            D7 = 0
    elif (Status == 1.2):
        point[0] -= 1
        point[1] = 50 - 50 * math.cos(math.radians(90 - point[0] * 90 / 50.0))
        ang = - math.degrees(math.asin((point[0] + 0.0) / 50.0)) + 180.0
        CircleCount -= 1

        if (point[0] == 0):
            Status = 1.3
            CircleCount = 50

    elif (Status == 1.3):
        ang = 180
        if not (point[1] >= PointC[1]):
            point[1] += 1
        elif (W == 1):
            Status = 2.0
            W = 0

    elif (Status == 2.0):
        point[1] -= 0.25
        if (point[1] <= PointC[1] - 18):
            Status = 2.1

    elif (Status == 2.1):
        TurningCount -= 18
        ang -=18
        if (TurningCount == 0):
            TurningCount = 90
            Status = 2.2
###63+180/18
    elif (Status == 2.2) and (D6 == 1):
        point[1] -= 1
        if (point[1] == 50):
            Status = 2.3
            D6 = 0
            D7 = 0
    elif (Status == 2.3):
        point[1] -= 1
        point[0] = 50 - 50 * math.cos(math.radians(90 - point[1] * 90 / 50))
        ang = math.degrees(math.asin((point[1] + 0.0) / 50.0)) - 90
        CircleCount -= 1

        if (point[1] == 0):
            Status = 2.4
            CircleCount = 50

    elif (Status == 2.4):
        point[0] += 1
        if (point[0] == PointB[0]):
            Status = 2.5

    elif (Status == 2.5) and (D7 == 1):
        TurningCount -= 9
        ang += 9
        if (TurningCount == 0):
            TurningCount = 90
            Status = 2.6
            D7 = 0
            D6 = 0

    elif (Status == 2.6):
        if not (point[1] == PointBB[1]):
            point[1] -= 1
        elif (point[1] == PointBB[1]) and (W == 1):
            Status = 3.0
            W = 0

    elif (Status == 3.0):
        point[1] += 1
        if (point[1] == 0):
            Status = 3.1

    elif (Status == 3.1):
        TurningCount -= 9
        ang -= 9
        if (TurningCount == 0):
            TurningCount = 90
            Status = 3.2

    elif (Status == 3.2) and (D6 == 1):
        point[0] += 1
        if (point[0] == PointA[0]):
            Status = 3.3
            D6 = 0
            D7 = 0

    elif (Status == 3.3) and (D6 == 1):
        TurningCount -= 9
        ang += 9
        if (TurningCount == 0):
            TurningCount = 90
            Status = 3.4
            D6 = 0
            D7 = 0

    elif (Status == 3.4):
        if not (point[1] == PointAA[1]):
            point[1] -= 1
        elif (W == 1):
            Status = 1
            W = 0

    my_msg = geometry_msgs.msg.Pose2D()
    my_msg.theta = ang+random.random()/10
    my_msg.x = point[0]+100+random.random() * 2

    my_msg.y = point[1]+100+random.random() * 2
    pub.publish(my_msg)
