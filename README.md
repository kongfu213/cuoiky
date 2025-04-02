killall -9 gzserver
killall -9 gzclient
cd ~/catkin_ws
catkin_make
source devel/setup.bash
 roscore

 roslaunch cuoiky gazebo.launch

Dieu khien xe
rosrun cuoiky controller_node.py
rostopic echo /cmd_vel
Dieu khien tay may
rosrun cuoiky link_controller.py
rostopic echo  /tien_link/cmd_vel
rostopic echo  /xoay_link/cmd_vel
encoder
rostopic echo /st_joint/encoder
rostopic echo /sp_joint/encode


rosrun rviz rviz









