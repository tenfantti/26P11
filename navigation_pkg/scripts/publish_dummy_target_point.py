#!/usr/bin/env python3

import math
import rospy
from geometry_msgs.msg import PoseStamped, Quaternion
from tf.transformations import quaternion_from_euler


def main():
    rospy.init_node("publish_dummy_target_point")

    topic = rospy.get_param("~topic", "/target_pose")
    frame_id = rospy.get_param("~frame_id", "map")
    x = rospy.get_param("~x", 1.0)
    y = rospy.get_param("~y", 0.5)
    z = rospy.get_param("~z", 0.0)
    yaw_deg = rospy.get_param("~yaw_deg", 0.0)
    delay = rospy.get_param("~delay", 1.0)

    pub = rospy.Publisher(topic, PoseStamped, queue_size=1)

    rospy.sleep(delay)

    yaw_rad = math.radians(yaw_deg)
    q = quaternion_from_euler(0.0, 0.0, yaw_rad)

    msg = PoseStamped()
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = frame_id
    msg.pose.position.x = x
    msg.pose.position.y = y
    msg.pose.position.z = z
    msg.pose.orientation = Quaternion(*q)

    rospy.loginfo(
        "Publishing target pose: frame=%s x=%.3f y=%.3f z=%.3f yaw_deg=%.1f",
        frame_id, x, y, z, yaw_deg
    )
    pub.publish(msg)

    rospy.sleep(0.5)


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass