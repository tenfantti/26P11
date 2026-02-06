# Lab rules
- Go through the lab rules [here](https://wiki.aalto.fi/pages/viewpage.action?pageId=238915137&spaceKey=ERL&title=Lab%2BPolicies%2Band%2BProcedures)
## More when working with Stretch
- Don't program the robot's acceleration parameter too high (~0.3)
- Same for the manipulator
- Always put the clamp at the bottom, and flip the power button when something goes wrong
- Please use docker when possible. If not, create a separate workspace and don't touch the default catkin_ws
- Test algorithms in Simulation if possible
- Best practice with battery (Full version [here](https://docs.hello-robot.com/0.2/stretch-hardware-guides/docs/battery_maintenance_guide_re2/)):
	- When charging the robot, use *12 AGM* mode (Press MODE button repeatedly until *12 AGM* indicator lights up)
	- When programming on the robot: use *SUPPLY* mode (Hold MODE button for 3 seconds, then press until *SUPPLY* indicator lights up)
	- When robot is not in used, shut down the computer (`systemctl poweroff`) and power off the robot, leave the charger attached on *12 AGM* mode (it will maintain a 'trickle charge')

# Project Overview
## Tasks
- Build a scene graph with Stretch
	- Use Astra 2 Camera instead of the mounted Realsense camera
		- Might need to use the realsense for manipulation (since they use it in their implementation of funmap)
	- Using ROS bag 
	- Using real data, in real-time (this you will need to connect with your laptop for object detector)
		- alternative: use aruco markers
	- Tip: Try to simplify environment as much as possible
	- REACT (with instance segmentation): https://github.com/aalto-intelligent-robotics/REACT/
		- If your have CUDA GPU, consider using this, deploy using docker
		- Have support for instance segmentation (Ultralytics YOLO + TensorRT support): https://docs.ultralytics.com/tasks/segment/
			- If you only have CPU, consider using **TFLite**, or if you're on a mac check that you have the mps backend (https://developer.apple.com/metal/pytorch/) 
				- I'm too poor to buy a mac so I can't help you fix software issues with it 😢
				- I haven't tried running detection models on TFLite as well
				- If you need a laptop with NVIDIA GPU let me know asap
	- Hydra: https://github.com/MIT-SPARK/Hydra/tree/archive/ros_noetic
		- ROS 1 version of Hydra, no docker, but can be easily set up
		- The framework is written in C++ so a bit difficult to navigate if you're not used to the language (if you are then go for it)
		- Consider using something else for segmentation (since they use semantic segmentation) and be prepared to
- Navigation:
	- https://docs.hello-robot.com/0.2/stretch-tutorials/ros1/navigation_stack/
		- move_base
		- gmapping
		- AMCL
	- Map 2D w. RP LiDAR
	- Localization with built map
		- Easy solution: same starting point when you built the scene graph
		- A bit trickier: Start randomly, move it around a bit, then the robot recalculates the position
	- Hydra has a freespace layer, consider using it for path planning
		- e.g., Build a Voronoi graph like HOV-SG: https://github.com/hovsg/HOV-SG)
		- The 2D map can also be used for navigation but it's not optimal (but could be used as a starting point)
- Grasping an object
	- Follow the documents here: 
	- Start with objects that are easy to grasp first (easy = don't have to analyze what's a good grasp or not, e.g., plushie)
	- FUNMAP: https://github.com/hello-robot/stretch_ros/tree/noetic/stretch_funmap
	- https://github.com/hello-robot/stretch_ros/blob/noetic/stretch_demos/nodes/grasp_object
	- Will most likely take the most programming effort
	- Demo video: https://www.youtube.com/watch?v=2_02YcXkUQU
- Interaction with scene graph:
	- First step: manually select the node to grasp
	- Second step: with LLM:
		- convert graph to json
		- feed 3dsg to some LLM to query
		- ask it: e.g., grasp me something soft -> goes to a plushie
- Simulation (only for navigation):
	- https://version.aalto.fi/gitlab/nguyent137/stretch_docker#
	- Docker for working with Stretch + ROS + Gazebo
		- Only recommended for navigation, grasping doesn't work the same as actual robot (no idea why)
		- Could use this potentially for navigation and processing grasp target with the camera, in case you don't have access to the robot, or are away
	- https://forum.hello-robot.com/t/is-there-a-way-to-run-funmap-on-gazebo-simulation/288/2
	- https://forum.hello-robot.com/t/how-to-make-stretch-robot-grab-an-object-in-gazebo-simulator/956
## Prerequisites
- Linux
	- knows how to work with basic Linux commands
	- ssh
- Docker
	- Nice playlist to get started: https://www.youtube.com/watch?v=XcJzOYe3E6M&list=PLunhqkrRNRhaqt0UfFxxC_oj7jscss2qe
- ROS
	- ROS Noetic: https://wiki.ros.org/ROS/Tutorials
- Git
	- Nice page with visualization to get started: https://learngitbranching.js.org/
- Python
- Some C++ (good to know if you want to change Hydra's code (I can help you a bit if you want to go that route))
- https://docs.hello-robot.com/0.2/
# Progression
## Basic requirements
- Build a scene graph with Stretch
- manually select object to grasp
- robot automatically goes to the object and grasp it
## Keep in mind
- Write **good documentations** of what you did
	- Keep the working repo well-maintained and easy to replicate
	- Write meaningful commits
- Communications
	- Telegram preferred
## A bit more advanced (More points)
- Interactions: LLM (natural language queries), Image-based search
- 3D navigation using freespace layer
- Pick and place: Grasp an object and bring it somewhere (to user, to a table, to a box)
- Update the scene graph after grasping it (move nodes around, connect robot node to object node being grasped).
- Grasp analysis: Grasp more difficult objects (mugs)
- ROS 2 integration (use ROS 1 bridge when necessary, e.g., getting sensor data from the robot since it still uses ROS 1)
- Feel free to propose more "upgrades"
# Practicalities
- **Inform Phuoc early if you need a laptop for this project**
	- For the people working on the scene graph building part this might be necessary for you to use instance segmentation models
- [x] Weekly meeting schedule (1 hour)
	- Fri 6/2/26 14-15
	- Please prepare an agenda
- [x] First robot lab training
	- How to use the Stretch
	- https://wiki.aalto.fi/pages/viewpage.action?spaceKey=IROBOTS&title=%5BUPDATING%5D+Hello+Stretch+2 (Updating, has the essential stuffs, not sure if you'll be able to access it though)
	- https://docs.hello-robot.com/0.2/ (More in-depth, we are using Stretch 2, and ROS Noetic)
		- The ROS 2 version is not stable yet so better not to use it
- [x] Takeout booking: https://takeout.aalto.fi/
- Access to robot lab: asked for it, waiting
