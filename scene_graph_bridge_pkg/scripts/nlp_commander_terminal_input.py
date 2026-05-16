#!/usr/bin/env python3

import argparse
import os
import rospy
import requests

import scene_graph_bridge_pkg.scripts.direct_goal_sender as direct_goal_sender


def extract_target_with_ollama(command, model_name, ollama_url):
    prompt = (
        "You are a robotic command parser. "
        "Extract ONLY the core target object from this user command. "
        "If there are multiple objects, reply with just the last one. "
        "Reply with only the object name and nothing else. "
        "Do not use punctuation. "
        f"Command: '{command}'"
    )

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(ollama_url, json=payload, timeout=30)
        response.raise_for_status()

        target = response.json().get("response", "").strip().lower()
        target = target.strip(" .'\"")
        return target

    except requests.exceptions.ConnectionError:
        rospy.logerr("Could not connect to Ollama at %s", ollama_url)
        return None
    except Exception as e:
        rospy.logerr("Ollama API error: %s", str(e))
        return None


def main():
    parser = argparse.ArgumentParser(description="Natural language scene graph commander.")
    parser.add_argument("--scene", type=str, required=True, help="Name of the scene graph folder")
    parser.add_argument("--model", type=str, default="qwen2.5:0.5b", help="Ollama model name")
    parser.add_argument("--frame_id", type=str, default="map", help="Frame of the DSG coordinates")
    parser.add_argument("--dsg_root", type=str, default="/home/ros/dsg_output", help="Root folder for DSG outputs")
    parser.add_argument("--ollama_url", type=str, default="http://localhost:11434/api/generate", help="Ollama API URL")

    args = parser.parse_args()

    rospy.init_node("nlp_commander", anonymous=True)

    filepath = os.path.join(args.dsg_root, args.scene, "backend", "dsg.json")

    print("\n" + "=" * 50)
    print(f"NLP Commander Online")
    print(f"Scene graph: {filepath}")
    print(f"Ollama model: {args.model}")
    print(f"Frame ID: {args.frame_id}")
    print("=" * 50)

    while not rospy.is_shutdown():
        command = input("\nWhere should the robot go? Type 'exit' to quit.\n> ")

        if command.lower() in ["exit", "quit"]:
            print("Shutting down commander...")
            break

        if not command.strip():
            continue

        rospy.loginfo("Parsing command with Ollama...")

        target = extract_target_with_ollama(
            command,
            args.model,
            args.ollama_url
        )

        if not target:
            rospy.logwarn("No target extracted.")
            continue

        rospy.loginfo("Extracted target: '%s'", target)

        position = direct_goal_sender.find_object_in_dsg(filepath, target)

        if position is None:
            rospy.logwarn("Could not find target '%s' in scene graph.", target)
            continue

        direct_goal_sender.send_target_point(
            position,
            frame_id=args.frame_id
        )


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass