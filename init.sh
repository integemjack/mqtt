# install ros

sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

sudo apt install curl -y
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -

sudo apt update
sudo apt install ros-melodic-desktop-full -y

echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
source ~/.bashrc

sudo apt install python-rosdep python-rosinstall python-rosinstall-generator python-wstool build-essential -y
sudo apt install python-rosdep -y
sudo apt install ros-melodic-image-transport ros-melodic-vision-msgs -y

sudo rosdep init
rosdep update


# install imagenet

cd ~
sudo apt-get install git cmake -y
git clone --recursive https://github.com/dusty-nv/jetson-inference
cd jetson-inference
mkdir build
cd build
cmake ../
make -j$(nproc)
sudo make install
sudo ldconfig


# test ros
mkdir -p ~/ros_workspace/src
git clone https://github.com/dusty-nv/ros_deep_learning ~/ros_workspace/src/ros_deep_learning
cd ~/ros_workspace
sudo apt install python-catkin-tools -y
catkin_make
cd ~/ros_workspace/devel
source ./setup.bash

# 如果catkin_make 不存在时
# sudo apt install python-catkin-tools