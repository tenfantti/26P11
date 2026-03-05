#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PointStamped

if __name__ == "__main__":
    rospy.init_node("publish_dummy_target_point")
    pub = rospy.Publisher("/target_point", PointStamped, queue_size=1, latch=True)

    frame = rospy.get_param("~frame", "map")
    x = rospy.get_param("~x", 1.0)
    y = rospy.get_param("~y", 0.0)
    z = rospy.get_param("~z", 0.0)

    msg = PointStamped()
    msg.header.frame_id = frame
    msg.header.stamp = rospy.Time.now()
    msg.point.x = x
    msg.point.y = y
    msg.point.z = z

    rospy.sleep(0.5)
    pub.publish(msg)
    rospy.loginfo(f"Published /target_point in {frame}: ({x}, {y}, {z})")
    rospy.spin()