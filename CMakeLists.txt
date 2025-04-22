cmake_minimum_required(VERSION 3.0.2)
project(xe)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  tf
  robot_state_publisher
  gazebo_ros
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

find_package(roslaunch)

# Cài đặt các thư mục như config, launch, meshes, urdf
foreach(dir config launch meshes urdf)
    install(DIRECTORY ${dir}/
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)

# Cài đặt script Python
catkin_install_python(PROGRAMS scripts/diff_drive_controller.py
                      DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

# Kiểm tra các file launch
roslaunch_add_file_check(launch)