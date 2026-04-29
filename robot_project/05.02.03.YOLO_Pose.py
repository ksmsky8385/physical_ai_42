import datetime
import cv2
import random
import signal
import sys
import numpy as np
import time
from ultralytics import YOLO

# 설정 값
CONFIDENCE_THRESHOLD = 0.6
MASK_ALPHA = 0.3  # 마스크 투명도
TARGET_FPS = 30  # 목표 FPS
FRAME_DELAY = 1.0 / TARGET_FPS  # 프레임 간격
COLORS = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(80)]  # 클래스별 색상


# 종료 처리 함수
def signal_handler(sig, frame):
    print("\n프로그램 종료 중...")
    cap.release()
    cv2.destroyAllWindows()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# 클래스 목록 로드
try:
    with open('./coco128.txt', 'r', encoding='utf-8') as f:
        class_list = f.read().splitlines()
except FileNotFoundError:
    print("Error: coco128.txt 파일을 찾을 수 없습니다.")
    sys.exit(1)

# 세그멘테이션 모델 로드 (YOLOv8-seg)
model = YOLO('./yolov8n-seg.pt')  # 세그멘테이션 전용 모델

# 카메라 설정
cap = cv2.VideoCapture('/dev/video0')  # 기본 장치
if not cap.isOpened():
    print("카메라 연결 오류: 다른 장치를 시도합니다.")
    cap = cv2.VideoCapture(1)  # 두 번째 카메라 시도
    if not cap.isOpened():
        print("모든 카메라 연결 실패. 프로그램 종료.")
        sys.exit(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, TARGET_FPS)  # FPS 설정

try:
    while True:
        start_time = datetime.datetime.now()

        ret, frame = cap.read()
        if not ret:
            print("프레임 읽기 실패")
            break

        # 좌우 반전 (카메라의 거울 효과 방지)
        frame = cv2.flip(frame, 1)

        # 세그멘테이션 수행
        results = model(frame)[0]
        overlay = frame.copy()

        for data in results:
            masks = data.masks
            boxes = data.boxes

            for i, (box, mask) in enumerate(zip(boxes, masks)):
                confidence = box.conf[0].item()
                if confidence < CONFIDENCE_THRESHOLD:
                    continue

                class_id = int(box.cls[0].item())
                color = COLORS[class_id % len(COLORS)]

                xmin, ymin, xmax, ymax = map(int, box.xyxy[0].tolist())
                mask_points = mask.xy[0].astype(np.int32)

                cv2.fillPoly(overlay, [mask_points], color)
                cv2.polylines(frame, [mask_points], True, color, 2)
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
                text = f"{class_list[class_id]} {confidence * 100:.1f}%"
                cv2.putText(frame, text, (xmin, ymin - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        frame = cv2.addWeighted(overlay, MASK_ALPHA, frame, 1 - MASK_ALPHA, 0)

        # FPS 계산 및 유지
        processing_time = (datetime.datetime.now() - start_time).total_seconds()
        fps = f"FPS: {1 / processing_time:.2f}"
        cv2.putText(frame, fps, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow('Segmentation', frame)

        elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
        time.sleep(max(0, FRAME_DELAY - elapsed_time))  # FPS 유지

        if cv2.waitKey(1) == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()