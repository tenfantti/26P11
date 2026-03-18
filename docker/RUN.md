# Stretch2 Navigation — Run Cheatsheet

Prereqs (host)
- One-time per boot to allow GUIs from the container:
  - sudo apt-get install -y x11-xserver-utils
  - xhost +local:
- Copy and edit environment file:
  - cd docker
  - cp .env.example .env
  - Edit .env for your network:
    - Robot master hotspot:
      - ROS_MASTER_URI=http://10.42.0.1:11311
      - ROS_IP=<your_laptop_hotspot_ip>
    - Robot master LAN:
      - ROS_MASTER_URI=http://130.233.123.111:11311
      - ROS_IP=<your_laptop_lan_ip>
    - Local master (dev):
      - ROS_MASTER_URI=http://localhost:11311
      - ROS_HOSTNAME=localhost
- If you’re away from the robot, comment the `devices:` block in docker/compose.yml.

Start the container
- From repo root:
  - cd docker
  - docker compose up --build
- Detached mode:
  - docker compose up --build -d
  - docker exec -it stretch_nav bash
- Stop:
  - Ctrl+C (foreground) or docker compose down

Connectivity tests (robot is ROS master)
- Inside container:
  - echo $ROS_MASTER_URI; echo $ROS_IP
  - ping -c2 <robot_ip>     # e.g., 10.42.0.1 or 130.233.123.111
  - rostopic list           # should show robot topics
  - rosnode list
  - rviz                    # GUI should open on host
- Send a cautious test velocity (watch the robot!):
  - rostopic pub -1 /cmd_vel geometry_msgs/Twist '{angular: {z: 0.1}}'
  - Or if base uses /stretch/cmd_vel:
    - rostopic pub -1 /stretch/cmd_vel geometry_msgs/Twist '{angular: {z: 0.1}}'

Build the catkin workspace (inside container)
- EntryPoint builds automatically. To rebuild manually:
  - cd /catkin_ws && catkin_make
  - source /catkin_ws/devel/setup.bash

RViz (inside container)
- rviz
- In RViz:
  - Set “Fixed Frame” to map (for localization/nav) or odom (for mapping)
  - Add Displays: TF, Map (/map), LaserScan (/scan), PoseArray (/particlecloud), RobotModel, Path

Mapping (build a new map) — real robot
- Terminal A: roscore     # if using local master; skip if robot is master
- Terminal B:
  - roslaunch navigation_pkg mapping.launch base_frame:=base_link scan_topic:=/scan
- Terminal C (teleop):
  - If the base listens to /stretch/cmd_vel:
    - roslaunch stretch_core teleop_twist.launch twist_topic:=/stretch/cmd_vel linear:=0.5 angular:=0.5 teleop_type:=joystick

Save the map
- mkdir -p $(rospack find navigation_pkg)/maps
- rosrun map_server map_saver -f $(rospack find navigation_pkg)/maps/home
- Commit maps/home.yaml and maps/home.pgm to git.

Localization (AMCL) + map_server — real robot
- roslaunch navigation_pkg localization.launch \
    base_frame:=base_link \
    scan_topic:=/scan \
    map:=$(rospack find navigation_pkg)/maps/home.yaml
- In RViz:
  - “2D Pose Estimate” near the robot’s true location
- Verify TF:
  - rosrun tf tf_echo map odom

Navigation (move_base) — real robot
- roslaunch navigation_pkg move_base.launch \
    base_frame:=base_link \
    scan_topic:=/scan
- If your base listens on /stretch/cmd_vel, the launch file remap should handle it. Otherwise edit config/nav_contract_real.yaml.
- Send a goal:
  - In RViz: “2D Nav Goal”
  - Or: rosrun navigation_pkg go_to_pose.py _x:=1.0 _y:=0.0 _yaw:=0.0

Simulation (optional, TurtleBot3; only if sim packages installed)
- Start Gazebo:
  - export TURTLEBOT3_MODEL=burger
  - roslaunch turtlebot3_gazebo turtlebot3_world.launch
- Mapping in sim:
  - roslaunch navigation_pkg mapping.launch sim:=true base_frame:=base_footprint scan_topic:=/scan
- Localization in sim:
  - roslaunch navigation_pkg localization.launch sim:=true map:=$(rospack find navigation_pkg)/maps/sim_world.yaml
- Move base in sim:
  - roslaunch navigation_pkg move_base.launch sim:=true
- RViz as above.

Useful diagnostics
- rostopic hz /scan
- rostopic info /stretch/cmd_vel
- roswtf
- rosrun tf view_frames (generates frames.pdf)
- rqt_graph

Device/permissions notes (real robot)
- Ensure docker/compose.yml has:
  - network_mode: host
  - privileged: true
  - group_add: [dialout, plugdev]
  - devices:
    - ${STRETCH_DEV}:${STRETCH_DEV}   # e.g., /dev/ttyACM0
    - ${LIDAR_DEV}:${LIDAR_DEV}       # e.g., /dev/ttyUSB0
- On host: your user may need dialout group for device access (outside Docker):
  - sudo usermod -aG dialout $USER   # then log out/in
