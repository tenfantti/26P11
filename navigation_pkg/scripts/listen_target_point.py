#!/usr/bin/env python3

import math
import rospy
import tf2_ros

from geometry_msgs.msg import PointStamped, PoseStamped
from navigation_pkg.go_to_pose import GoToPose
from tf.transformations import euler_from_quaternion


class TargetListener:
    def __init__(self):
        rospy.init_node("listen_target_point")

        self.target_point_topic = rospy.get_param("~target_point_topic", "/target_point")
        self.target_pose_topic = rospy.get_param("~target_pose_topic", "/target_pose")
        self.default_frame = rospy.get_param("~default_frame", "map")
        self.robot_frame = rospy.get_param("~robot_frame", "base_link")
        self.wait_for_result = rospy.get_param("~wait_for_result", False)
        self.result_timeout = rospy.get_param("~result_timeout", 120.0)
        self.min_goal_distance_change = rospy.get_param("~min_goal_distance_change", 0.05)
        self.standoff_distance = rospy.get_param("~standoff_distance", 0.5)
        self.use_standoff_for_points = rospy.get_param("~use_standoff_for_points", True)
        self.default_yaw_deg = rospy.get_param("~default_yaw_deg", 0.0)

        self.navigator = GoToPose()

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)

        self.last_goal_x = None
        self.last_goal_y = None
        self.last_goal_yaw = None

        self.point_sub = rospy.Subscriber(
            self.target_point_topic,
            PointStamped,
            self.point_callback,
            queue_size=1
        )

        self.pose_sub = rospy.Subscriber(
            self.target_pose_topic,
            PoseStamped,
            self.pose_callback,
            queue_size=1
        )

        rospy.loginfo("Listening for target points on %s", self.target_point_topic)
        rospy.loginfo("Listening for target poses on %s", self.target_pose_topic)

    def is_duplicate_goal(self, x, y, yaw=None):
        if self.last_goal_x is None or self.last_goal_y is None:
            return False

        distance = math.hypot(x - self.last_goal_x, y - self.last_goal_y)
        if distance >= self.min_goal_distance_change:
            return False

        if yaw is not None and self.last_goal_yaw is not None:
            yaw_diff = abs(self.normalize_angle(yaw - self.last_goal_yaw))
            if yaw_diff > math.radians(5.0):
                return False

        return True

    def get_robot_pose_in_map(self):
        try:
            transform = self.tf_buffer.lookup_transform(
                self.default_frame,
                self.robot_frame,
                rospy.Time(0),
                rospy.Duration(1.0)
            )
            x = transform.transform.translation.x
            y = transform.transform.translation.y

            q = transform.transform.rotation
            quaternion = [q.x, q.y, q.z, q.w]
            _, _, yaw = euler_from_quaternion(quaternion)

            return x, y, yaw

        except (tf2_ros.LookupException,
                tf2_ros.ConnectivityException,
                tf2_ros.ExtrapolationException) as e:
            rospy.logwarn("Could not get robot pose from TF: %s", str(e))
            return None

    @staticmethod
    def normalize_angle(angle):
        return math.atan2(math.sin(angle), math.cos(angle))

    def compute_standoff_goal(self, target_x, target_y):
        robot_pose = self.get_robot_pose_in_map()
        if robot_pose is None:
            return None

        robot_x, robot_y, _ = robot_pose

        dx = target_x - robot_x
        dy = target_y - robot_y
        distance = math.hypot(dx, dy)

        if distance < 1e-6:
            rospy.logwarn("Target is extremely close to robot pose. Cannot compute approach direction.")
            return None

        approach_yaw = math.atan2(dy, dx)

        if distance <= self.standoff_distance:
            rospy.logwarn(
                "Target is closer than standoff distance (distance=%.3f, standoff=%.3f). "
                "Using target point directly.",
                distance, self.standoff_distance
            )
            goal_x = target_x
            goal_y = target_y
        else:
            goal_x = target_x - self.standoff_distance * math.cos(approach_yaw)
            goal_y = target_y - self.standoff_distance * math.sin(approach_yaw)

        return goal_x, goal_y, approach_yaw

    def send_navigation_goal(self, x, y, yaw, frame_id, source):
        if not math.isfinite(x) or not math.isfinite(y) or not math.isfinite(yaw):
            rospy.logwarn("Received invalid goal values from %s.", source)
            return

        if frame_id != self.default_frame:
            rospy.logwarn(
                "Expected frame '%s' but received '%s'. Proceeding anyway.",
                self.default_frame, frame_id
            )

        if self.is_duplicate_goal(x, y, yaw):
            rospy.loginfo("Goal from %s is very close to previous goal. Ignoring duplicate.", source)
            return

        rospy.loginfo(
            "Sending goal from %s: frame=%s x=%.3f y=%.3f yaw=%.3f rad",
            source, frame_id, x, y, yaw
        )

        try:
            self.navigator.send_goal(x=x, y=y, yaw=yaw, frame_id=frame_id)
            self.last_goal_x = x
            self.last_goal_y = y
            self.last_goal_yaw = yaw
        except Exception as e:
            rospy.logerr("Failed to send navigation goal from %s: %s", source, str(e))
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

    def point_callback(self, msg):
        frame_id = msg.header.frame_id if msg.header.frame_id else self.default_frame
        target_x = msg.point.x
        target_y = msg.point.y
        target_z = msg.point.z

        if not math.isfinite(target_x) or not math.isfinite(target_y):
            rospy.logwarn("Received invalid PointStamped target.")
            return

        rospy.loginfo(
            "Received target point: frame=%s x=%.3f y=%.3f z=%.3f",
            frame_id, target_x, target_y, target_z
        )

        if self.use_standoff_for_points:
            result = self.compute_standoff_goal(target_x, target_y)
            if result is None:
                rospy.logwarn("Could not compute standoff goal for target point.")
                return

            goal_x, goal_y, goal_yaw = result

            rospy.loginfo(
                "Computed standoff goal: x=%.3f y=%.3f yaw=%.3f rad (standoff=%.3f m)",
                goal_x, goal_y, goal_yaw, self.standoff_distance
            )

            self.send_navigation_goal(goal_x, goal_y, goal_yaw, frame_id, source="PointStamped")
        else:
            yaw = math.radians(self.default_yaw_deg)
            rospy.loginfo("Using default yaw %.1f deg for PointStamped target.", self.default_yaw_deg)
            self.send_navigation_goal(target_x, target_y, yaw, frame_id, source="PointStamped")

    def pose_callback(self, msg):
        frame_id = msg.header.frame_id if msg.header.frame_id else self.default_frame
        x = msg.pose.position.x
        y = msg.pose.position.y
        z = msg.pose.position.z

        q = msg.pose.orientation
        quaternion = [q.x, q.y, q.z, q.w]
        _, _, yaw = euler_from_quaternion(quaternion)

        if not math.isfinite(x) or not math.isfinite(y) or not math.isfinite(yaw):
            rospy.logwarn("Received invalid PoseStamped target.")
            return

        rospy.loginfo(
            "Received target pose: frame=%s x=%.3f y=%.3f z=%.3f yaw=%.3f rad",
            frame_id, x, y, z, yaw
        )

        self.send_navigation_goal(x, y, yaw, frame_id, source="PoseStamped")


if __name__ == "__main__":
    try:
        node = TargetListener()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass