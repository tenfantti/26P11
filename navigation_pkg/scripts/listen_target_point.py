#!/usr/bin/env python3
import math
import rospy

from geometry_msgs.msg import PointStamped
from navigation_pkg.go_to_pose import GoToPose

class TargetPointListener:
    def __init__(self):
        rospy.init_node("listen_target_point")

        self.target_topic = rospy.get_param("~target_topic", "/target_point")
        self.default_frame = rospy.get_param("~default_frame", "map")
        self.default_yaw = rospy.get_param("~default_yaw", 0.0)
        self.wait_for_result = rospy.get_param("~wait_for_result", False)
        self.result_timeout = rospy.get_param("~result_timeout", 120.0)
        self.min_goal_distance_change = rospy.get_param("~min_goal_distance_change", 0.05)

        self.navigator = GoToPose()

        self.last_goal_x = None
        self.last_goal_y = None

        self.sub = rospy.Subscriber(
            self.target_topic,
            PointStamped,
            self.target_callback,
            queue_size=1
        )

        rospy.loginfo("Listening for target points on %s", self.target_topic)

    def is_duplicate_goal(self, x, y):
        if self.last_goal_x is None or self.last_goal_y is None:
            return False

        distance = math.hypot(x - self.last_goal_x, y - self.last_goal_y)
        return distance < self.min_goal_distance_change

    def target_callback(self, msg):
        frame_id = msg.header.frame_id if msg.header.frame_id else self.default_frame
        x = msg.point.x
        y = msg.point.y

        if not math.isfinite(x) or not math.isfinite(y):
            rospy.logwarn("Received invalid target point: x=%s y=%s", str(x), str(y))
            return

        rospy.loginfo(
            "Received target point: frame=%s x=%.3f y=%.3f z=%.3f",
            frame_id, msg.point.x, msg.point.y, msg.point.z
        )

        if self.is_duplicate_goal(x, y):
            rospy.loginfo("Target is very close to previous goal. Ignoring duplicate.")
            return

        yaw = self.default_yaw

        try:
            self.navigator.send_goal(x=x, y=y, yaw=yaw, frame_id=frame_id)
            self.last_goal_x = x
            self.last_goal_y = y
        except Exception as e:
            rospy.logerr("Failed to send navigation goal: %s", str(e))
            return

        if self.wait_for_result:
            state = self.navigator.wait_for_result(timeout=self.result_timeout)
            if state is None:
                rospy.logwarn("Navigation did not finish before timeout.")
            else:
                rospy.loginfo(
                    "Navigation finished with state: %s",
                    self.navigator.state_to_string(state)
                )


if __name__ == "__main__":
    try:
        node = TargetPointListener()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass