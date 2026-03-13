FROM osrf/ros:noetic-desktop-full

SHELL ["/bin/bash", "-c"]

# Base tools and ROS utilities
RUN apt-get update && apt-get install -y \
    git \
    curl \
    nano \
    rsync \
    python3-pip \
    python3-catkin-tools \
    python3-rosdep \
    python3-vcstool \
    ros-noetic-rqt \
    ros-noetic-rqt-graph \
    ros-noetic-tf \
    ros-noetic-tf2-tools \
    ros-noetic-robot-state-publisher \
    && rm -rf /var/lib/apt/lists/*

# Navigation stack and mapping/localization (real robot)   
RUN apt-get update && apt-get install -y \
    ros-noetic-navigation \
    ros-noetic-slam-gmapping \
    ros-noetic-amcl \
    ros-noetic-map-server \
    ros-noetic-teleop-twist-keyboard \
    ros-noetic-topic-tools \
    ros-noetic-rplidar-ros \
    && rm -rf /var/lib/apt/lists/*

# Simulation extras (Gazebo + TurtleBot3)
# desktop-full already includes Gazebo; add TB3 for quick sim testing
RUN apt-get update && apt-get install -y \
    ros-noetic-turtlebot3 \
    ros-noetic-turtlebot3-simulations \
    && rm -rf /var/lib/apt/lists/*

# Python libs for scripts/utilities
RUN pip3 install --no-cache-dir \
    numpy \
    pyyaml

# Create catkin workspace
ENV CATKIN_WS=/catkin_ws
RUN mkdir -p ${CATKIN_WS}/src

# Source ROS and workspace in every new shell
RUN echo "source /opt/ros/noetic/setup.bash" >> /root/.bashrc \
 && echo "source ${CATKIN_WS}/devel/setup.bash || true" >> /root/.bashrc

# Entrypoint builds the workspace and opens an interactive shell
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR ${CATKIN_WS}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]