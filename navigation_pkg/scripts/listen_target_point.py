#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PointStamped

def cb(msg: PointStamped):
    rospy.loginfo(f"Received /target_point frame={msg.header.frame_id} x={msg.point.x:.2f} y={msg.point.y:.2f} z={msg.point.z:.2f}")

if __name__ == "__main__":
    rospy.init_node("listen_target_point")
    rospy.Subscriber("/target_point", PointStamped, cb, queue_size=1)
    rospy.loginfo("Listening to /target_point ...")
    rospy.spin()