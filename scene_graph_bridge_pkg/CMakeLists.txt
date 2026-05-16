cmake_minimum_required(VERSION 3.0.2)
project(scene_graph_bridge_pkg)

find_package(catkin REQUIRED COMPONENTS
  rospy
  geometry_msgs
)

catkin_package(
  CATKIN_DEPENDS rospy geometry_msgs
)

catkin_install_python(PROGRAMS
  scripts/direct_goal_sender.py
  scripts/nlp_commander_terminal_input.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)