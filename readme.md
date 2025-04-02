**killall \-9 gzserver**  
**killall \-9 gzclient**  
**cd \~/catkin\_ws**  
**catkin\_make**  
**source devel/setup.bash**  
 **roscore**

 **roslaunch cuoiky gazebo.launch**

**Dieu khien xe**  
**rosrun cuoiky controller\_node.py**  
**rostopic echo /cmd\_vel**  
**Dieu khien tay may**  
**rosrun cuoiky link\_controller.py**  
**rostopic echo  /tien\_link/cmd\_vel**  
**rostopic echo  /xoay\_link/cmd\_vel**  
**encoder**  
**rostopic echo /st\_joint/encoder**  
**rostopic echo /sp\_joint/encode**

**rosrun rviz rviz**

