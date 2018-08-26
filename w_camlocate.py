#!/usr/bin/env python

"""
This node locates the position of the robotino if ar_marker is stationary
when the camera is mounted in the front of the robotino

Change Txxx_xxx when necessasry
There are also parameters that are to be changed in launch1.launch

Steps to tracking a stationary marker ar_markerN:
1. determine the transformation matrix to the origin and define Ts_arN
2. look up the transform from camera_robotino to ar_markerN: TarN_cam
3. calculate reduce(np.dot, (Ts_arN, TarN_cam, Tcam_body))
4. obtain from matrix rotation and translational values of robotino in the stationary reference frame
---
or use the function lookup_robotino_from_ar and plug in the marker and Ts_arN
as shown in the code, the two approaches yield the same result.

"""
import numpy as np

# configuration of ar7 relative to origin(s)
Ts_ar7 = np.array([
    [0,0,1,0],
    [1,0,0,0],
    [0,1,0,0],
    [0,0,0,1]
])

# configuration of robotino body relative to robotino camera
Tcam_body = np.array([
    [0,-1,0,0],
    [0,0,-1,0],
    [1,0,0,0],
    [0,0,0,1]
])
import rospy
import tf.transformations as tft
import tf2_ros
import geometry_msgs.msg
import modern_robotics as mr


def quat_to_mat(q0,q1,q2,q3, t0=0,t1=0,t2=0):
    return np.array([
            [q0**2+q1**2-q2**2-q3**2, 2*(q1*q2-q0*q3), 2*(q0*q2+q1*q3), t0],
            [2*(q0*q3+q1*q2), q0**2-q1**2+q2**2-q3**2, 2*(q2*q3-q0*q1), t1],
            [2*(q1*q3-q0*q2), 2*(q0*q1+q2*q3), q0**2-q1**2-q2**2+q3**2, t2],
            [0,0,0,1]
        ])

def quat_to_mat1(qx, qy, qz, qw, tx=0, ty=0, tz=0):
    return np.array([
        [1 - 2 * qy**2 - 2 * qz**2, 2 * qx * qy - 2 * qz * qw, 2 * qx * qz + 2 * qy * qw, tx],
        [2 * qx * qy + 2 * qz * qw, 1 - 2 * qx**2 - 2 * qz**2, 2 * qy * qz - 2 * qx * qw, ty],
        [2 * qx * qz - 2 * qy * qw, 2 * qy * qz + 2 * qx * qw, 1 - 2 * qx**2 - 2 * qy**2, tz],
        [0,0,0,1]
    ])


def lookup_robotino_from_ar(marker, Ts_arN):
    global tfBuffer, Tcam_body
    t = tfBuffer.lookup_transform('camera_robotino', 'ar_marker_' + str(marker), rospy.Time())
    t0 = t.transform.translation.x
    t1 = t.transform.translation.y
    t2 = t.transform.translation.z
    q1 = t.transform.rotation.x
    q2 = t.transform.rotation.y
    q3 = t.transform.rotation.z
    q0 = t.transform.rotation.w
    TarN_cam = quat_to_mat(q0, q1, q2, q3, t0, t1, t2)
    Ts_body = reduce(np.dot, (Ts_arN, TarN_cam, Tcam_body))
    return Ts_body


# for mat to quat use quaternion_from_matrix

# data:





rospy.init_node('cam_locator')
rate = rospy.Rate(20)
np.set_printoptions(precision=3, suppress=True)
tfBuffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(tfBuffer)
publisher = tf2_ros.TransformBroadcaster()
while not rospy.is_shutdown():


    try:
        t = tfBuffer.lookup_transform('camera_robotino','ar_marker_7',rospy.Time())
        t0=t.transform.translation.x
        t1=t.transform.translation.y
        t2=t.transform.translation.z
        q1=t.transform.rotation.x
        q2=t.transform.rotation.y
        q3=t.transform.rotation.z
        q0=t.transform.rotation.w
        Tar7_cam = quat_to_mat(q0, q1, q2, q3, t0, t1, t2)
        Ts_body = reduce(np.dot, (Ts_ar7, Tar7_cam, Tcam_body))

        Ts1_body = lookup_robotino_from_ar(marker=7, Ts_arN=Ts_ar7)
        print 'rotation matrix Ts_body:'
        print Ts_body
        print 'or'
        print Ts1_body
        print 'translational values:'
        print np.transpose(Ts_body[0:3, 3])
        # axis of screw from orotation matrix
        print 'screw axis:'
        screw = mr.so3ToVec(mr.MatrixLog6(Ts_body)[0:3, 0:3])
        if screw[2] < 0:
            screw = -screw
        print screw
        print 'angle:'
        screw_normalized = mr.Normalize(mr.so3ToVec(mr.MatrixLog6(Ts_body)[0:3, 0:3]))
        for i in range(3):
            if mr.NearZero(screw[i]):
                continue
            screwangle = screw[i]/screw_normalized[i]

        print screwangle * 180 / 3.1415926
        rate.sleep()

    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:

        pass

    except KeyboardInterrupt:
        break


"""

def publish_tf_array(publisher, nparr, fromid, toid):
    t = geometry_msgs.msg.TransformStamped()
    t.header.stamp = rospy.Time.now()
    t.header.frame_id = fromid
    t.child_frame_id = toid

    t.transform.translation.x = nparr[0, 3]
    t.transform.translation.y = nparr[1, 3]
    t.transform.translation.z = nparr[2, 3]
    quat = tft.quaternion_from_matrix(nparr)
    t.transform.rotation.x = quat[0]
    t.transform.rotation.y = quat[1]
    t.transform.rotation.z = quat[2]
    t.transform.rotation.w = quat[3]

    publisher.sendTransform(t)

"""