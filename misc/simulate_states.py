import rospy, geometry_msgs.msg, std_msgs.msg


rospy.init_node('simulated_robotino')
publoc = rospy.Publisher('robotino_location', geometry_msgs.msg.Pose2D, queue_size=1)
pubst = rospy.Publisher('robotino_state', std_msgs.msg.String, queue_size=1)

lower_right = (300, 450)
current_loc = [0,0,0]
current_direction = 'x+'

rate = rospy.Rate(100)

while not rospy.is_shutdown():
    rate.sleep()

    if current_direction == 'x+':
        if current_loc[0] >= lower_right[0]:
            current_direction = 'y+'
        else: current_loc[0] += 1

    if current_direction == 'y+':
        if current_loc[1] >= lower_right[1]:
            current_direction = 'x-'
        else: current_loc[1] += 1

    if current_direction == 'x-':
        if current_loc[0] <= 0:
            current_direction = 'y-'
        else: current_loc[0] -= 1

    if current_direction == 'y-':
        if current_loc[1] <= 0:
            current_direction = 'x+'
        else:
            current_loc[1] -= 1

    if current_loc[2] >= 360:
        current_loc[2] = 0
    else: current_loc[2] += 1

    msg = geometry_msgs.msg.Pose2D()
    msg.x = current_loc[0]
    msg.y = current_loc[1]
    msg.theta = current_loc[2]
    publoc.publish(msg)
    pubst.publish(current_direction)


