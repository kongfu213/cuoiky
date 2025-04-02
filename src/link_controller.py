#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import sys
import select
import tty
import termios

class LinkController:
    def __init__(self):
        rospy.init_node('link_controller', anonymous=True)
        
        # Publisher cho từng link riêng biệt
        self.pub_tien = rospy.Publisher('/tien_link/cmd_vel', Twist, queue_size=10)
        self.pub_xoay = rospy.Publisher('/xoay_link/cmd_vel', Twist, queue_size=10)
        
        self.rate = rospy.Rate(10)
        
        self.msg = """
        Điều khiển các link:
        ---------------------------
        w : Tiến về phía trước (tien_link)
        s : Lùi về phía sau (tien_link)
        a : Quay trái (xoay_link)
        d : Quay phải (xoay_link)
        x : Dừng
        CTRL+C : Thoát
        ---------------------------
        """
        print(self.msg)

    def getKey(self):
        settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

    def control_links(self):
        key = self.getKey()
        
        # Tạo lệnh điều khiển cho từng link
        cmd_tien = Twist()
        cmd_xoay = Twist()

        if key == 'w':  # Tiến về phía trước (tien_link)
            cmd_tien.linear.x = 1.0
        elif key == 's':  # Lùi về phía sau (tien_link)
            cmd_tien.linear.x = -1.0
        elif key == 'a':  # Quay trái (xoay_link)
            cmd_xoay.angular.z = 1.0
        elif key == 'd':  # Quay phải (xoay_link)
            cmd_xoay.angular.z = -1.0
        elif key == 'x':  # Dừng (tien_link và xoay_link)
            cmd_tien.linear.x = 0.0
            cmd_xoay.angular.z = 0.0
        elif key == '\x03':  # Ctrl+C để thoát
            rospy.signal_shutdown("Shutting down")
            return None

        # Xuất bản lệnh cho từng link
        self.pub_tien.publish(cmd_tien)
        self.pub_xoay.publish(cmd_xoay)
        
        return True

    def run(self):
        rospy.loginfo("Link controller is running...")
        while not rospy.is_shutdown():
            if not self.control_links():
                break
            self.rate.sleep()

if __name__ == '__main__':
    try:
        controller = LinkController()
        controller.run()
    except rospy.ROSInterruptException:
        pass
