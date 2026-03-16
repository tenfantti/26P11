#!/usr/bin/env bash
set -e

# Allow X11 from container (run 'xhost +local:' on host once)
echo "Starting container…"
export PS1="(stretch-docker) \u@\h:\w\$ "

# Source ROS
source /opt/ros/noetic/setup.bash

# Sync package into catkin workspace
if [ -d /root/ws/navigation_pkg ]; then
  mkdir -p /catkin_ws/src
  rsync -a --delete /root/ws/navigation_pkg /catkin_ws/src/
fi

# Build workspace if src exists
if [ -d /catkin_ws/src ]; then
  cd /catkin_ws
  catkin_make
  source /catkin_ws/devel/setup.bash
fi

# Drop into an interactive shell
exec bash
