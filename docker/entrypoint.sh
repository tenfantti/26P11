#!/usr/bin/env bash
set -e

# Allow X11 from container (run 'xhost +local:' on host once)
echo "Starting container…"
export PS1="(stretch-docker) \u@\h:\w\$ "

# Source ROS
source /opt/ros/noetic/setup.bash

# Sync package into catkin workspace
mkdir -p /catkin_ws/src
if [ -d /root/ws/navigation_pkg ]; then
  echo "Syncing navigation_pkg into /catkin_ws/src…"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete /root/ws/navigation_pkg /catkin_ws/src/
  else
    echo "Warning: rsync not found, using cp -r fallback"
    rm -rf /catkin_ws/src/navigation_pkg
    cp -r /root/ws/navigation_pkg /catkin_ws/src/
  fi
else
  echo "Note: /root/ws/navigation_pkg not found. Is the repo mounted (../:/root/ws) in compose.yml?"
fi


# Build workspace if src exists
if [ -d /catkin_ws/src ]; then
  cd /catkin_ws
  catkin_make
  source /catkin_ws/devel/setup.bash
fi

# Drop into an interactive shell
exec bash
