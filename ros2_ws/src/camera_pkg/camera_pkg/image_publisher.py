import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class ImagePublisher(Node):
	def __init__(self):
		super().__init__('image_publisher')
		# 1. 퍼블리셔 생성: 타입은 Image, 토픽명은 'image_raw, 큐 크기는 10
		self.publisher_ = self.create_publisher(Image, 'image_raw', 10)
		# 2. 타이머 설정: 0.1초마다 timer_callback 실행 (10Hz)
		self.timer = self.create_timer(0.1, self.timer_callback)
		# 3. 웹캠 연결 (0번 카메라)
		self.cap = cv2.VideoCapture(0)
		self.bridge = CvBridge()

	def timer_callback(self):
		ret, frame = self.cap.read()
		if ret:
			# OpenCV 이미지를 ROS2 이미지 메시지로 변환하여 퍼블리시
			img_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
			self.publisher_.publish(img_msg)
			self.get_logger().info('이미지 발행 중...')

def main(args=None):
	rclpy.init(args=args)
	node =ImagePublisher()
	try:
		rclpy.spin(node)
	except KeyboardInterrupt:
		pass
	node.destroy_node()
	rclpy.shutdown()
