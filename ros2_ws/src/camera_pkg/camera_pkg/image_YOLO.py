import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge


class ImageYOLO(Node):
    def __init__(self):
        super().__init__('image_yolo')
        self.bridge = CvBridge()
        self.current_frame = None

        # /image_raw 구독
        self.subscription = self.create_subscription(
            Image, 'image_raw', self.image_callback, 10)

        # 미션 1: YOLO 박스가 그려진 이미지 퍼블리셔
        self.yolo_publisher = self.create_publisher(Image, 'image_yolo', 10)

        # 미션 2: Canny 엣지 퍼블리셔
        self.edge_publisher = self.create_publisher(Image, 'image_edge', 10)

    def image_callback(self, msg):
        self.current_frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        frame = self.current_frame.copy()

        # 미션 1: YOLO 결과 시뮬레이션 - 프레임 중앙에 탐지 박스 그리기
        h, w = frame.shape[:2]
        x1, y1 = w // 4, h // 4
        x2, y2 = w * 3 // 4, h * 3 // 4
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, 'YOLO: object', (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        img_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        self.yolo_publisher.publish(img_msg)

        # 미션 2: Canny 엣지 처리 후 /image_edge 토픽으로 퍼블리시
        edge = cv2.Canny(self.current_frame, 100, 200)
        self.edge_publisher.publish(self.bridge.cv2_to_imgmsg(edge, 'mono8'))


def main(args=None):
    rclpy.init(args=args)
    node = ImageYOLO()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
