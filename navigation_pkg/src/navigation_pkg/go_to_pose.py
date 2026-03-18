#!/usr/bin/env python3
import rospy
import actionlib

from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Quaternion
from tf.transformations import quaternion_from_euler

class GoToPose:
    def __init__(self, action_name="move_base", timeout=10.0):
        self.action_name = action_name
        self.client = actionlib.SimpleActionClient(self.action_name, MoveBaseAction)

        rospy.loginfo("Waiting for %s action server...", self.action_name)
        server_ready = self.client.wait_for_server(rospy.Duration(timeout))

        if not server_ready:
            rospy.logerr("Could not connect to %s action server.", self.action_name)
            raise rospy.ROSException("move_base action server not available")

        rospy.loginfo("Connected to %s action server.", self.action_name)

    def send_goal(self, x, y, yaw=0.0, frame_id="map"):
        goal = MoveBaseGoal()
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.header.frame_id = frame_id

        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.position.z = 0.0

        q = quaternion_from_euler(0.0, 0.0, yaw)
        goal.target_pose.pose.orientation = Quaternion(*q)

        rospy.loginfo(
            "Sending goal to %s: frame=%s x=%.3f y=%.3f yaw=%.3f",
            self.action_name, frame_id, x, y, yaw
        )
        self.client.send_goal(goal)

    def wait_for_result(self, timeout=None):
        if timeout is None:
            finished = self.client.wait_for_result()
        else:
            finished = self.client.wait_for_result(rospy.Duration(timeout))

        if not finished:
            rospy.logwarn("Timed out while waiting for navigation result.")
            return None

        return self.client.get_state()

    def cancel_goal(self):
        rospy.loginfo("Cancelling current goal.")
        self.client.cancel_goal()

    def get_state(self):
        return self.client.get_state()

    @staticmethod
    def state_to_string(state):
        state_map = {
            GoalStatus.PENDING: "PENDING",
            GoalStatus.ACTIVE: "ACTIVE",
            GoalStatus.PREEMPTED: "PREEMPTED",
            GoalStatus.SUCCEEDED: "SUCCEEDED",
            GoalStatus.ABORTED: "ABORTED",
            GoalStatus.REJECTED: "REJECTED",
            GoalStatus.PREEMPTING: "PREEMPTING",
            GoalStatus.RECALLING: "RECALLING",
            GoalStatus.RECALLED: "RECALLED",
            GoalStatus.LOST: "LOST",
        }
        return state_map.get(state, "UNKNOWN")