#!/usr/bin/env python3

import rospy
import json
import argparse
import os
from geometry_msgs.msg import PointStamped


def find_object_in_dsg(filepath, target_name):
    if not os.path.exists(filepath):
        rospy.logerr("Cannot find Scene Graph file at: %s", filepath)
        return None

    with open(filepath, "r") as f:
        data = json.load(f)

    nodes = data.get("nodes", [])

    for node in nodes:
        attributes = node.get("attributes", {})
        name = attributes.get("name", "").lower()

        if target_name.lower() in name:
            position = attributes.get("position")
            rospy.loginfo("Found '%s' at coordinates: %s", target_name, position)
            return position

    rospy.logwarn("Object '%s' not found in the Scene Graph!", target_name)
    return None


def send_target_point(position, frame_id="map"):
    pub = rospy.Publisher("/target_point", PointStamped, queue_size=10)
    rospy.sleep(1.0)

    if position is None or len(position) < 2:
        rospy.logerr("Invalid position: %s", position)
        return

    msg = PointStamped()
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = frame_id

    msg.point.x = float(position[0])
    msg.point.y = float(position[1])
    msg.point.z = float(position[2]) if len(position) > 2 else 0.0

    rospy.loginfo(
        "Publishing /target_point: frame=%s x=%.3f y=%.3f z=%.3f",
        frame_id,
        msg.point.x,
        msg.point.y,
        msg.point.z
    )

    pub.publish(msg)
    rospy.sleep(0.5)


def main():
    parser = argparse.ArgumentParser(description="Send scene graph object target to WP2 navigation.")
    parser.add_argument("--scene", type=str, required=True, help="Name of the scene graph folder")
    parser.add_argument("--target", type=str, required=True, help="Name of the object to find")
    parser.add_argument("--frame_id", type=str, default="map", help="Frame of the DSG coordinates")
    parser.add_argument(
        "--dsg_root",
        type=str,
        default="/home/ros/dsg_output",
        help="Root folder containing DSG outputs"
    )

    args = parser.parse_args()

    rospy.init_node("direct_semantic_navigator", anonymous=True)

    filepath = os.path.join(args.dsg_root, args.scene, "backend", "dsg.json")

    position = find_object_in_dsg(filepath, args.target)

    if position is not None:
        send_target_point(position, frame_id=args.frame_id)


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass