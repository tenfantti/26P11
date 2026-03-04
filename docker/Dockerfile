FROM osrf/ros:noetic-desktop-full

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y \
    git \
    curl \
    nano \
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

RUN apt-get update && apt-get install -y \
    ros-noetic-navigation \
    ros-noetic-slam-gmapping \
    ros-noetic-amcl \
    ros-noetic-map-server \
    ros-noetic-teleop-twist-keyboard \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
    numpy \
    pyyaml

ENV CATKIN_WS=/catkin_ws
RUN mkdir -p ${CATKIN_WS}/src

RUN echo "source /opt/ros/noetic/setup.bash" >> /root/.bashrc \
 && echo "source ${CATKIN_WS}/devel/setup.bash || true" >> /root/.bashrc

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR ${CATKIN_WS}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]