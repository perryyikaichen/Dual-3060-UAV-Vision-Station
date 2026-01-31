FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Install system dependencies
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
    tabulate

# Create user 'ardupilot' with passwordless sudo (needed for some internal waf scripts)
RUN useradd -m -s /bin/bash ardupilot && \
    echo "ardupilot ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ardupilot && \
    usermod -aG dialout ardupilot

USER ardupilot
WORKDIR /home/ardupilot

# Clone ArduPilot
RUN git clone --recursive https://github.com/ArduPilot/ardupilot.git

WORKDIR /home/ardupilot/ardupilot

# Setup MAVLink and WAF environment path
ENV PATH="/home/ardupilot/ardupilot/Tools/autotest:${PATH}"
ENV PATH="/home/ardupilot/.local/bin:${PATH}"

# Default entrypoint
CMD ["/bin/bash"]
