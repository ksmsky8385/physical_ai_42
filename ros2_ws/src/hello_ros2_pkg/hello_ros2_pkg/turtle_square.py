import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class TurtleSquare(Node):
    def __init__(self):
        super().__init__('turtle_square')

        self.publisher_ = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.timer = self.create_timer(0.1, self.timer_callback)

        self.step = 0
        self.tick = 0

        # 0.1초 주기이므로 10번 발행하면 1초
        self.ticks_per_second = 10

        self.get_logger().info('Turtle square node started')

    def timer_callback(self):
        msg = Twist()

        # step 구조:
        # 0: 전진
        # 1: 회전
        # 2: 전진
        # 3: 회전
        # ...
        # 7까지 하면 전진/회전 4회 완료
        if self.step >= 8:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.publisher_.publish(msg)
            self.get_logger().info('Square completed')
            self.timer.cancel()
            return

        if self.step % 2 == 0:
            # 1초 전진
            msg.linear.x = 1.0
            msg.angular.z = 0.0
            action = 'forward'
        else:
            # 1초 동안 제자리 회전
            # angular.z = pi/2 rad/s 이므로 1초 동안 90도 회전
            msg.linear.x = 0.0
            msg.angular.z = math.pi / 2
            action = 'turn'

        self.publisher_.publish(msg)

        self.tick += 1

        if self.tick >= self.ticks_per_second:
            self.get_logger().info(f'{action} done, step={self.step}')
            self.tick = 0
            self.step += 1


def main(args=None):
    rclpy.init(args=args)

    node = TurtleSquare()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()