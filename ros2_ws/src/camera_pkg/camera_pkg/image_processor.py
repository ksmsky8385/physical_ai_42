import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_srvs.srv import Trigger
import cv2
from cv_bridge import CvBridge

class ImageProcessor(Node):
	def __init__(self):
		super().__init__('image_processor')
		self.bridge = CvBridge()
		# 1. 서브스크라이버 생성: 'image_raw' 토픽 구독
		self.subscription = self.create_subscription(
			Image, 'image_raw', self.image_callback, 10)
		# 2. 서비스 서버 생성: 'capture_snapshot' 서비스 제공
		self.srv = self.create_service(
			Trigger, 'capture_snapshot', self.capture_callback)

	def image_callback(self, msg):
		# ROS2 메시지를 OpenCV 이미지로 변환
		self.current_frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
		cv2.imshow("Camera View", self.current_frame)
		cv2.waitKey(1) # 화면 갱신을 위해 필수

	def capture_callback(self, request, response):
		if self.current_frame is not None:
			cv2.imwrite('snapshot.jpg', self.current_frame)
			response.success = True
			response.message = "스냅샷이 snapshot.jpg로 저장되었습니다!"
		else:
			response.success = False
			response.message = "이미지가 아직 수신되지 않았습니다."
		return response

def main(args=None):
	rclpy.init(args=args)
	node = ImageProcessor()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()
