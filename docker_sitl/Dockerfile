FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV GZ_VERSION=garden

# Install system dependencies
# Added: gazebo, libgazebo-dev, libopencv-dev, libxcb dependencies for QGC/Gazebo
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    g++ \
    gawk \
    genromfs \
    libc6-i386 \
    libxml2-dev \
    libxslt1-dev \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    sudo \
    wget \
    rsync \
    curl \
    lsb-release \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Install Gazebo Garden (Official Repo) and Graphical Dependencies
RUN curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" > /etc/apt/sources.list.d/gazebo-stable.list && \
    apt-get update && apt-get install -y \
    gz-garden \
    libgz-sim7-dev \
    libgz-transport12-dev \
    libgz-math7-dev \
    libgz-msgs9-dev \
    pkg-config \
    libopencv-dev \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    rapidjson-dev \
    libxcb-xinerama0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shm0 \
    libxcb-util1 \
    libxcb-xfixes0 \
    libxkbcommon-x11-0 \
    && rm -rf /var/lib/apt/lists/*

# ... (omitted lines)

# Setup Environment Variables
ENV PATH="/home/ardupilot/ardupilot/Tools/autotest:${PATH}"
ENV PATH="/home/ardupilot/.local/bin:${PATH}"
ENV GZ_SIM_SYSTEM_PLUGIN_PATH="/home/ardupilot/ardupilot_gazebo/build"
ENV GZ_SIM_RESOURCE_PATH="/home/ardupilot/ardupilot_gazebo/models:/home/ardupilot/ardupilot_gazebo/worlds"

# Install Python dependencies for ArduPilot SITL
RUN python3 -m pip install -U \
    pymavlink \
    MAVProxy \
    pexpect \
    future \
    lxml \
    pyserial \
    geocoder \
    empy==3.3.4 \
    ptyprocess \
    dronecan \
    flake8 \
    junitparser \
    wsproto \
    tabulate \
    opencv-python

# Create user 'ardupilot' with passwordless sudo
RUN useradd -m -s /bin/bash ardupilot && \
    echo "ardupilot ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ardupilot && \
    usermod -aG dialout ardupilot

USER ardupilot
WORKDIR /home/ardupilot

# Clone ArduPilot (Shallow clone to prevent timeouts)
RUN git clone --depth 1 --recursive https://github.com/ArduPilot/ardupilot.git

# Clone and Build ArduPilot Gazebo Plugin
RUN git clone --depth 1 https://github.com/ArduPilot/ardupilot_gazebo.git && \
    cd ardupilot_gazebo && \
    mkdir build && \
    cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo && \
    make -j4 && \
    sudo make install

WORKDIR /home/ardupilot/ardupilot

# Setup Environment Variables
ENV PATH="/home/ardupilot/ardupilot/Tools/autotest:${PATH}"
ENV PATH="/home/ardupilot/.local/bin:${PATH}"
ENV GZ_SIM_SYSTEM_PLUGIN_PATH="/home/ardupilot/ardupilot_gazebo/build:${GZ_SIM_SYSTEM_PLUGIN_PATH}"
ENV GZ_SIM_RESOURCE_PATH="/home/ardupilot/ardupilot_gazebo/models:/home/ardupilot/ardupilot_gazebo/worlds:${GZ_SIM_RESOURCE_PATH}"

# Default entrypoint
CMD ["/bin/bash"]
