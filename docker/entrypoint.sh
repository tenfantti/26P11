#!/usr/bin/env bash
set -e

source /opt/ros/noetic/setup.bash

if [ -d "/catkin_ws/src/project" ]; then
  cd /catkin_ws
  if [ ! -f "/catkin_ws/devel/setup.bash" ]; then
    echo "[entrypoint] Building catkin workspace..."
    catkin_make
  fi
  source /catkin_ws/devel/setup.bash || true
fi

exec "$@"