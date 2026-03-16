#!/usr/bin/env bash
# Run localization (map_server + AMCL) on real robot
# Update the map path if your map file name differs.
MAP_FILE=\$(rospack find navigation_pkg)/maps/home.yaml
docker exec -it stretch_nav bash -lc \
  "roslaunch navigation_pkg localization.launch base_frame:=base_link scan_topic:=/scan map:=\$MAP_FILE"
