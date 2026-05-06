#!/usr/bin/env python3
import json
import rospy
from geometry_msgs.msg import PointStamped


def find_target(objects, target_label):
    for obj in objects:
        if obj.get("label") == target_label:
            return obj
    return None


def main():
    rospy.init_node("publish_target_from_json")

    json_path = rospy.get_param("~json_path")
    target_label = rospy.get_param("~target_label", "cup")
    default_frame = rospy.get_param("~frame_id", "map")
    topic = rospy.get_param("~topic", "/target_point")

    pub = rospy.Publisher(topic, PointStamped, queue_size=10)

    with open(json_path, "r") as f:
        data = json.load(f)

    objects = data.get("objects", [])
    target = find_target(objects, target_label)

    if target is None:
        rospy.logerr("Target label '%s' not found in JSON.", target_label)
        return

    frame_id = target.get("frame_id", data.get("frame_id", default_frame))

    msg = PointStamped()
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = frame_id
    msg.point.x = float(target["x"])
    msg.point.y = float(target["y"])
    msg.point.z = float(target.get("z", 0.0))

    rospy.sleep(1.0)
    pub.publish(msg)

    rospy.loginfo(
        "Published /target_point from JSON: label=%s frame=%s x=%.3f y=%.3f z=%.3f",
        target_label, frame_id, msg.point.x, msg.point.y, msg.point.z
    )

    rospy.sleep(0.5)


if __name__ == "__main__":
    main()