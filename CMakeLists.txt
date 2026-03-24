cmake_minimum_required(VERSION 3.0.2)
project(so100_urdf)

## Compile as C++11 (supported in ROS Melodic)
add_compile_options(-std=c++11)

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  roslaunch
  robot_state_publisher
  joint_state_publisher
  joint_state_publisher_gui
  gazebo_ros
  gazebo_ros_control
  gazebo_plugins
  rviz
  xacro
)

## System dependencies are found with CMake's conventions
find_package(gazebo REQUIRED)

## Uncomment if package has a message or service
# add_message_files()
# add_service_files()

## Generate added messages and services with any dependencies listed
# generate_messages()

## Declare a catkin package
catkin_package(
  CATKIN_DEPENDS 
    roslaunch 
    robot_state_publisher 
    joint_state_publisher 
    joint_state_publisher_gui
    gazebo_ros
    gazebo_ros_control
    gazebo_plugins
    rviz
    xacro
  DEPENDS gazebo
)

## Include directories
include_directories(
  ${catkin_INCLUDE_DIRS}
  ${GAZEBO_INCLUDE_DIRS}
)

## Link directories
link_directories(
  ${GAZEBO_LIBRARY_DIRS}
)

## Install URDF files
install(DIRECTORY assets/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/assets
)

install(DIRECTORY launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)

install(DIRECTORY rviz/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/rviz
)

install(DIRECTORY worlds/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/worlds
)

install(FILES so100.urdf so100_gazebo.urdf
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/urdf
)

## Gazebo plugin (if needed in future)
# add_library(my_gazebo_plugin src/my_gazebo_plugin.cpp)
# target_link_libraries(my_gazebo_plugin ${GAZEBO_LIBRARIES})