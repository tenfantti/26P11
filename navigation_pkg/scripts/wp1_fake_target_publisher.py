#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PointStamped


def main():
    rospy.init_node("wp1_fake_target_publisher")

    pub = rospy.Publisher("/target_point", PointStamped, queue_size=10)

    frame_id = rospy.get_param("~frame_id", "map")
    x = rospy.get_param("~x", 1.0)
    y = rospy.get_param("~y", 0.0)
    z = rospy.get_param("~z", 0.0)

    rospy.sleep(1.0)

    msg = PointStamped()
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = frame_id
    msg.point.x = x
    msg.point.y = y
    msg.point.z = z

    rospy.loginfo(
        "Publishing fake WP1 /target_point: frame=%s x=%.3f y=%.3f z=%.3f",
        frame_id, x, y, z
    )

    pub.publish(msg)
    rospy.sleep(0.5)


if __name__ == "__main__":
    main()