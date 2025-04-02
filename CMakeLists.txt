cmake_minimum_required(VERSION 2.8.3)

project(cuoiky)

# Tìm các gói ROS cần thiết
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  sensor_msgs
  geometry_msgs
  tf
  gazebo_ros
)

# Khai báo package ROS
catkin_package(
  CATKIN_DEPENDS roscpp rospy sensor_msgs geometry_msgs tf gazebo_ros
)

# Tìm Gazebo
find_package(gazebo REQUIRED)
find_package(roscpp REQUIRED)
find_package(std_msgs REQUIRED)

include_directories(${GAZEBO_INCLUDE_DIRS} ${catkin_INCLUDE_DIRS})
link_directories(${GAZEBO_LIBRARY_DIRS})
add_definitions(${GAZEBO_CXX_FLAGS})

# Liên kết các thư viện Gazebo
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
link_libraries(${GAZEBO_LIBRARIES} ${catkin_LIBRARIES})


# Install Python scripts
catkin_install_python(PROGRAMS src/controller_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

# Cài đặt các thư mục tài nguyên (config, launch, meshes, urdf)
foreach(dir config launch meshes urdf)
  install(DIRECTORY ${dir}/
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach()
