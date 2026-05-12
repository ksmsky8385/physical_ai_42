import sys
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import AddTwoInts

class AddTwoIntsClient(Node):
    def __init__(self):
        super().__init__('add_two_ints_client')
        self.client = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('서비스 대기 중...')

    def send_request(self, a, b):
        req = AddTwoInts.Request()
        req.a = a
        req.b = b
        self.future = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    client = AddTwoIntsClient()
    a, b = 7, 3
    response = client.send_request(a, b)
    if response is not None:
        client.get_logger().info(f'결과 수신: {a} + {b} = {response.sum}')
    else:
        client.get_logger().error('서비스 호출 실패')
    client.destroy_node()
    rclpy.shutdown()
