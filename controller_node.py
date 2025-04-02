#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
import sys
import select
import tty
import termios

class RobotController:
    def __init__(self):
        rospy.init_node('robot_controller', anonymous=True)
        
        # Các publisher cho từng khớp
        self.pub_tt = rospy.Publisher('/cuoiky/tt_velocity_controller/command', Float64, queue_size=10)
        self.pub_tp = rospy.Publisher('/cuoiky/tp_velocity_controller/command', Float64, queue_size=10)
        self.pub_sp = rospy.Publisher('/cuoiky/sp_velocity_controller/command', Float64, queue_size=10)
        self.pub_st = rospy.Publisher('/cuoiky/st_velocity_controller/command', Float64, queue_size=10)
        
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(10)

        self.msg = """
        Điều khiển robot từ bàn phím:
        ---------------------------
        w : Tiến về phía trước
        s : Lùi về phía sau
        a : Quay trái
        d : Quay phải
        x : Dừng robot
        CTRL+C : Thoát
        ---------------------------
        """

        print(self.msg)

    def getKey(self):
        settings = termios.tcgetattr(sys.stdin)  # Lưu cài đặt terminal hiện tại
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)  # Khôi phục cài đặt terminal
        return key

    def control_robot(self):
        key = self.getKey()

        cmd = Twist()
        
        # Các giá trị tốc độ mặc định
        tt_speed = 0.0
        tp_speed = 0.0
        sp_speed = 0.0
        st_speed = 0.0

        if key == 'w':  # Tiến về phía trước
            cmd.linear.x = 1.0
            cmd.angular.z = 0.0
            tt_speed = 1.0
            tp_speed = 1.0
            sp_speed = 1.0
            st_speed = 1.0
        elif key == 's':  # Lùi về phía sau
            cmd.linear.x = -1.0
            cmd.angular.z = 0.0
            tt_speed = -1.0
            tp_speed = -1.0
            sp_speed = -1.0
            st_speed = -1.0
        elif key == 'a':  # Quay trái
            cmd.linear.x = 0.0
            cmd.angular.z = 1.0
            tt_speed = 1.0
            tp_speed = -1.0
            sp_speed = 1.0
            st_speed = -1.0
        elif key == 'd':  # Quay phải
            cmd.linear.x = 0.0
            cmd.angular.z = -1.0
            tt_speed = -1.0
            tp_speed = 1.0
            sp_speed = -1.0
            st_speed = 1.0
        elif key == 'x':  # Dừng robot
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            tt_speed = 0.0
            tp_speed = 0.0
            sp_speed = 0.0
            st_speed = 0.0
        elif key == '\x03':  # Ctrl+C để thoát
            rospy.signal_shutdown("Shutting down")
            return None

        # Xuất bản các lệnh điều khiển khớp
        self.pub_tt.publish(tt_speed)
        self.pub_tp.publish(tp_speed)
        self.pub_sp.publish(sp_speed)
        self.pub_st.publish(st_speed)

        # Xuất bản lệnh cmd_vel nếu cần
        self.cmd_pub.publish(cmd)
        
        return True

    def run(self):
        rospy.loginfo("Robot controller is running...")
        while not rospy.is_shutdown():
            if not self.control_robot():
                break
            self.rate.sleep()

if __name__ == '__main__':
    try:
        controller = RobotController()
        controller.run()
    except rospy.ROSInterruptException:
        pass
