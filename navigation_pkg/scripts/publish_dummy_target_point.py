#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PointStamped

def main():
    rospy.init_node("publish_dummy_target_point")

    topic = rospy.get_param("~topic", "/target_point")
    frame_id = rospy.get_param("~frame_id", "map")
    x = rospy.get_param("~x", 1.0)
    y = rospy.get_param("~y", 0.5)
    z = rospy.get_param("~z", 0.0)
    delay = rospy.get_param("~delay", 1.0)

    pub = rospy.Publisher(topic, PointStamped, queue_size=1)

    rospy.loginfo("Waiting %.2f seconds before publishing test target...", delay)
    rospy.sleep(delay)

    msg = PointStamped()
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = frame_id
    msg.point.x = x
    msg.point.y = y
    msg.point.z = z

    rospy.loginfo(
        "Publishing dummy target on %s: frame=%s x=%.3f y=%.3f z=%.3f",
        topic, frame_id, x, y, z
    )
    pub.publish(msg)

    rospy.sleep(0.5)


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass