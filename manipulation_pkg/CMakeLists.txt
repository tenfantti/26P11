cmake_minimum_required(VERSION 3.0.2)
project(manipulation_pkg)

find_package(catkin REQUIRED COMPONENTS
  actionlib
  actionlib_msgs
  control_msgs
  geometry_msgs
  nav_msgs
  rospy
  sensor_msgs
  std_msgs
  std_srvs
  tf
  tf2_ros
  trajectory_msgs
  hello_helpers
  stretch_funmap
)

catkin_python_setup()

catkin_package(
  CATKIN_DEPENDS
    actionlib
    actionlib_msgs
    control_msgs
    geometry_msgs
    nav_msgs
    rospy
    sensor_msgs
    std_msgs
    std_srvs
    tf
    tf2_ros
    trajectory_msgs
    hello_helpers
    stretch_funmap
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  scripts/grasp_object.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)