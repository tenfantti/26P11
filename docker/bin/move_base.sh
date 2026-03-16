#!/usr/bin/env bash
# Run move_base (includes localization) on real robot
docker exec -it stretch_nav bash -lc \
  "roslaunch navigation_pkg move_base.launch base_frame:=base_link scan_topic:=/scan cmd_vel_out:=/stretch/cmd_vel"
