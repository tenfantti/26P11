#!/usr/bin/env python3
import rospy
import actionlib
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import tf.transformations as tft

def make_goal(x, y, yaw, frame="map"):
    goal = MoveBaseGoal()
    goal.target_pose = PoseStamped()
    goal.target_pose.header.frame_id = frame
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    q = tft.quaternion_from_euler(0.0, 0.0, yaw)
    goal.target_pose.pose.orientation.x = q[0]
    goal.target_pose.pose.orientation.y = q[1]
    goal.target_pose.pose.orientation.z = q[2]
    goal.target_pose.pose.orientation.w = q[3]
    return goal

if __name__ == "__main__":
    rospy.init_node("go_to_pose")

    x = rospy.get_param("~x", 1.0)
    y = rospy.get_param("~y", 0.0)
    yaw = rospy.get_param("~yaw", 0.0)
    frame = rospy.get_param("~frame", "map")
    timeout_s = rospy.get_param("~timeout_s", 120.0)

    client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
    rospy.loginfo("Waiting for move_base...")
    if not client.wait_for_server(rospy.Duration(10.0)):
        rospy.logerr("move_base action server not available.")
        raise SystemExit(1)

    client.send_goal(make_goal(x, y, yaw, frame))
    rospy.loginfo(f"Sent goal: ({x}, {y}) yaw={yaw} frame={frame}")

    if not client.wait_for_result(rospy.Duration(timeout_s)):
        rospy.logwarn("Timed out; cancelling goal.")
        client.cancel_goal()
        raise SystemExit(2)

    rospy.loginfo(f"Done. State={client.get_state()}")