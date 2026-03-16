#!/usr/bin/env bash
# Run mapping on real robot (build a map with gmapping)
# Adjust base_frame and scan_topic if needed.
docker exec -it stretch_nav bash -lc \
  "roslaunch navigation_pkg mapping.launch base_frame:=base_link scan_topic:=/scan"
